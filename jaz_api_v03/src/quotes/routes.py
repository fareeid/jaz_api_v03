import json
from base64 import b64decode, b64encode
from datetime import datetime, timedelta
from typing import Any

from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import text  # , func  # Column, Integer, MetaData, String, Table, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

# from . import crud
from . import crud as quotes_crud
from . import (  # noqa: F401
    models,
    schemas,
    schemas_,
    vendors_api,  # noqa: F401
)
from . import services as quote_services
from .models import Quote
from .vendors_api import schemas as vendor_schemas
from ..auth import dependencies as auth_dependencies
from ..auth import models as user_models
from ..auth import schemas as user_schemas
from ..auth import services as user_services
from ..core.dependencies import (  # , orcl_base
    aes_decrypt,
    aes_encrypt,
    get_non_async_oracle_session,
    get_oracle_session_sim,
    get_session,
)
from ..customer import crud as customers_crud
from ..external_apis import crud as external_apis_crud
from ..masters import crud as masters_crud
from ..premia import models as premia_models
from ..premia import services as premia_services
from ..premia.schemas import PolicyCreate, PolicyChargeCreate, PolicyCoverCreate, PolicyRiskCreate, PolicySectionCreate, \
    PolicyCurrencyCreate, ReceiptStagingCreate, PolicyHypothecationCreate
from ..reports import schemas as report_schemas

router = APIRouter()


# @router.get("/branch", response_model=schemas.Branch)

@router.post("/check_veh_status", response_model=dict[str, Any])
async def check_veh_status(
        *,
        async_db: AsyncSession = Depends(get_session),
        non_async_oracle_db: Session = Depends(get_non_async_oracle_session),  # Real Premia
        search_criteria: dict[str, Any],
        current_user: user_models.User = Depends(auth_dependencies.get_current_user),
) -> Any:
    veh_status = premia_services.validate_vehicle_json(non_async_oracle_db, search_criteria)
    return json.loads(veh_status)


@router.post("/report", response_model=list[dict[str, Any]])
async def report(
        *,
        async_db: AsyncSession = Depends(get_session),
        non_async_oracle_db: Session = Depends(get_non_async_oracle_session),  # Real Premia
        report_params: report_schemas.ReportParams,
        current_user: user_models.User = Depends(auth_dependencies.get_current_user),
) -> Any:
    if not current_user.is_superuser:
        report_params.search_criteria.cust_code = current_user.cust_code
    premia_report = premia_services.run_report(non_async_oracle_db, report_params)
    return premia_report


@router.post("/quote", response_model=dict[str, Any])  # schemas.Quote
async def quote(
        *,
        async_db: AsyncSession = Depends(get_session),
        non_async_oracle_db: Session = Depends(get_non_async_oracle_session),  # Real Premia
        # non_async_oracle_db: Session = Depends(get_oracle_session_sim),  # Simulation Premia
        payload_in: schemas.QuoteCreate,
        current_user: user_models.User = Depends(auth_dependencies.get_current_user),
) -> Any:
    policy_process_dict = await process_quote(async_db, current_user, non_async_oracle_db, payload_in)

    return policy_process_dict
    # return quotation
    # return {"test_key": "test_value"}


async def process_quote(async_db, current_user, non_async_oracle_db, payload_in):
    data = {
        "external_party": "jazk-web",
        "transaction_type": "Quote",
        "notification": "json",
        "payload": jsonable_encoder(payload_in.model_dump(exclude_unset=True))
    }
    payload = await external_apis_crud.external_payload.create_v2(
        async_db, obj_in=data
    )

    for proposal in payload_in.proposals:
        for section in proposal.proposalsections:
            for risk in section.proposalrisks:
                vehicle_reg_no = risk.prai_flexi["vehicle_reg_no"]["prai_data_03"]
                vehicle_chassis_no = risk.prai_flexi["vehicle_chassis_no"]["prai_data_01"]
                vehicle_engine_no = risk.prai_flexi["vehicle_engine_no"]["prai_data_02"]
                # search_criteria = {"vehicle_reg_no": "KDD 990Z","vehicle_chassis_no": "CHASSIS 001", "vehicle_engine_no": "ENGINE 001"}
                search_criteria = {
                    "vehicle_reg_no": vehicle_reg_no,
                    "vehicle_chassis_no": vehicle_chassis_no,
                    "vehicle_engine_no": vehicle_engine_no
                }
                veh_status = premia_services.validate_vehicle_json(non_async_oracle_db, search_criteria)
                if json.loads(veh_status)["Info"] == "Error":
                    raise HTTPException(status_code=400, detail="Vehicle found in active policy. You cannot proceed")

    if current_user.cust_cc_code in ['01','10']:
        if payload_in.quot_assr_email != current_user.email or payload_in.quot_assr_pin != current_user.pin:
            raise HTTPException(status_code=400, detail="This customer is only authorised to transact for self")
        user = current_user
    else:
        user_obj = user_schemas.UserCreate(
            first_name=payload_in.quot_assr_name,
            name=payload_in.quot_assr_name,
            email=payload_in.quot_assr_email,
            phone=payload_in.quot_assr_phone,
            nic=payload_in.quot_assr_nic,
            lic_no=payload_in.quot_assr_lic,
            pin=payload_in.quot_assr_pin,
            gender=payload_in.quot_assr_gender,
            dob=payload_in.quot_assr_dob.isoformat(),
            user_flexi=payload_in.quot_assr_flexi,
        )
        new, user = await user_services.get_user(async_db, user_obj)
    customer_model = await premia_services.sync_user_to_premia_cust(non_async_oracle_db, user)
    #################
    #################
    payload_in.quot_assr_id = user.id
    for proposal in payload_in.proposals:
        proposal.pol_assr_code = customer_model.cust_code
        proposal.pol_flexi.update({"quot_assr_addr": user.user_flexi["quot_assr_addr"]})
    # TODO Refactor to use quote services
    quotation: Quote = await quotes_crud.quote.create_v1(async_db, obj_in=payload_in)
    quote_data = jsonable_encoder(quotation, by_alias=True, exclude_unset=True, exclude_defaults=True, exclude=None,
                                  exclude_none=True)
    for proposal in quote_data["proposals"]:
        proposal["pol_prd_sys_id"] = proposal["prop_sys_id"]
    policy_quote_data = quote_to_policy(quote_data)
    # premia_policy_data = []
    pgit_policy_list_db = []
    for proposal in policy_quote_data:
        prop = await quotes_crud.proposal.get_proposal(async_db, proposal["pol_prd_sys_id"])

        policy_template_charges_list = await masters_crud.product.get_charges_by_product(async_db, prod_code=proposal[
            "pol_prod_code"])
        policy_template_sections_list = await masters_crud.product.get_sections_by_product(async_db, prod_code=proposal[
            "pol_prod_code"])
        policy_template_all_risks_list = await masters_crud.product.get_risks_by_product(async_db, prod_code=proposal[
            "pol_prod_code"])
        policy_template_risks_list = [d for d in policy_template_all_risks_list if d.get('prai_remarks_10') == 'risk']
        policy_template_certs_list = [d for d in policy_template_all_risks_list if d.get('prai_remarks_10') == 'cert']
        # policy_template_certs_list = await masters_crud.product.get_risks_by_product(async_db, prod_code='1002', risk_code='motor_cert')
        policy_template_covers_list = await masters_crud.product.get_covers_by_product(async_db, prod_code=proposal[
            "pol_prod_code"])

        pgit_policy_template = await masters_crud.product.get_product(async_db, prod_code=proposal["pol_prod_code"])

        policy_template_dict = {
            "pgit_policy_template": {k: v for k, v in pgit_policy_template[0].items() if v != ''},
            "pgit_pol_charge_template": [{k: v for k, v in charge.items() if v != ''} for charge in
                                         policy_template_charges_list if charge],
            "pgit_pol_section": [{k: v for k, v in section.items() if v != ''} for section in
                                 policy_template_sections_list if section],
            "pgit_pol_risk_addl_info_template": [{k: v for k, v in risk.items() if v != ''} for risk in
                                                 policy_template_risks_list if risk],
            "pgit_pol_risk_cert_info_template": [{k: v for k, v in risk.items() if v != ''} for risk in
                                                 policy_template_certs_list if risk],
            "pgit_pol_risk_cover_template": [{k: v for k, v in cover.items() if v != ''} for cover in
                                             policy_template_covers_list if cover]
        }

        pol_sys_id = premia_services.get_sys_id(non_async_oracle_db, "pgi_pol_sys_id")
        quote_charges_list = proposal.pop("proposalcharges", None)
        # policy_template_charges_list = pgit_policy_template["charges"]
        pgit_pol_charge_data = merge_lists_by_key("pchg_code", policy_template_dict["pgit_pol_charge_template"],
                                                  quote_charges_list)
        pgit_pol_charge_list_db = []
        for charge in pgit_pol_charge_data:
            pchg_sys_id = premia_services.get_sys_id(non_async_oracle_db, "pgi_pchg_sys_id")
            charge["pchg_sys_id"] = pchg_sys_id
            charge["pchg_pol_sys_id"] = pol_sys_id
            charge["pchg_prod_code"] = proposal["pol_prod_code"]
            charge["pchg_dept_code"] = proposal["pol_dept_code"]
            charge["pchg_cr_uid"] = "PORTAL-REG"
            charge["pchg_cr_dt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            pgit_pol_charge_data_pydantic = PolicyChargeCreate(**charge)
            pgit_pol_charge_list_db.append(premia_models.PolicyCharge(
                **pgit_pol_charge_data_pydantic.model_dump(exclude_none=True, exclude_unset=True)))

        pgit_pol_hypothecation_list_db = []
        if proposal["pol_hypothecation_yn"] == "1":
            phpo_sys_id = premia_services.get_sys_id(non_async_oracle_db, "pgi_phpo_sys_id")
            pgit_pol_hypothecation_data = {
                "phpo_sys_id": phpo_sys_id,
                "phpo_pol_sys_id": pol_sys_id,
                "phpo_end_no_idx": 0,
                "phpo_end_sr_no": 0,
                "phpo_cust_code": prop.prop_hypothecation["prop_bank_cust_code"],
                "phpo_hypo_type": "2",
                "phpo_rec_type": "I",
                "phpo_ds_type": "2",
                "phpo_cr_uid": "PORTAL-REG",
                "phpo_cr_dt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "phpo_bank_name": prop.prop_hypothecation["prop_bank_cust_name"],
            }
            pgit_pol_hypothecation_data_pydantic = PolicyHypothecationCreate(**pgit_pol_hypothecation_data)
            pgit_pol_hypothecation_db = premia_models.PolicyHypothecation(
                **pgit_pol_hypothecation_data_pydantic.model_dump(exclude_none=True, exclude_unset=True)
            )
            pgit_pol_hypothecation_list_db.append(pgit_pol_hypothecation_db)

        pgit_pol_appl_curr_list_db = []
        pac_sys_id = premia_services.get_sys_id(non_async_oracle_db, "pgi_pac_sys_id")
        pgit_pol_appl_curr_data = {
            # **policy_template_dict["pgit_pol_appl_curr"][0],
            # **quote_section,
            "pac_sys_id": pac_sys_id,
            "pac_pol_sys_id": pol_sys_id,
            "pac_end_no_idx": 0,
            "pac_end_sr_no": 0,
            "pac_curr_code": proposal["pol_prem_curr_code"],
            "pac_curr_rate_type": "B",
            "pac_curr_rate_1": 1,
            "pac_curr_rate_2": 1,
            "pac_curr_rate_3": 1,
            "pac_rec_type": "I",
            "pac_comp_code": "001",
            "pac_divn_code": "118",
            "pac_dept_code": proposal["pol_dept_code"],
            "pac_prod_code": proposal["pol_prod_code"],
            "pac_ds_type": policy_template_dict['pgit_policy_template']['pol_ds_type'],  # "2",
            "pac_cr_uid": "PORTAL-REG",
            "pac_cr_dt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        pgit_pol_appl_curr_data_pydantic = PolicyCurrencyCreate(**pgit_pol_appl_curr_data)
        pgit_pol_appl_curr_db = premia_models.PolicyCurrency(
            **pgit_pol_appl_curr_data_pydantic.model_dump(exclude_none=True, exclude_unset=True))
        pgit_pol_appl_curr_list_db.append(pgit_pol_appl_curr_db)

        quote_sections_list = proposal.pop("proposalsections", None)
        pgit_pol_section_list_db = []
        for quote_section in quote_sections_list:
            psec_sys_id = premia_services.get_sys_id(non_async_oracle_db, "pgi_psec_sys_id")
            quote_risks_list = quote_section.pop("proposalrisks")
            pgit_pol_risk_addl_info_list_db = []
            for quote_risk in quote_risks_list:
                prai_sys_id = premia_services.get_sys_id(non_async_oracle_db, "pgi_prai_sys_id")
                quote_covers_list = quote_risk.pop("proposalcovers", None)

                pgit_pol_risk_cover_data = merge_lists_by_key("prc_code",
                                                              policy_template_dict["pgit_pol_risk_cover_template"],
                                                              quote_covers_list)
                pgit_pol_risk_cover_list_db = []
                for cover in pgit_pol_risk_cover_data:
                    cover["prc_sys_id"] = premia_services.get_sys_id(non_async_oracle_db, "pgi_prc_sys_id")
                    cover["prc_pol_sys_id"] = pol_sys_id
                    cover["prc_psec_sys_id"] = psec_sys_id
                    cover["prc_sec_code"] = quote_section["psec_sec_code"]
                    cover["prc_lvl1_sys_id"] = prai_sys_id
                    cover["prc_eff_fm_dt"] = proposal["pol_fm_dt"]
                    cover["prc_eff_to_dt"] = proposal["pol_to_dt"]
                    cover["prc_prod_code"] = proposal["pol_prod_code"]
                    cover["prc_dept_code"] = proposal["pol_dept_code"]
                    # cover["prc_peril_class_code"] = "PC-MOT-1002"
                    cover["prc_cr_uid"] = "PORTAL-REG"
                    cover["prc_cr_dt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    pgit_pol_risk_cover_data_pydantic = PolicyCoverCreate(**cover)
                    pgit_pol_risk_cover_list_db.append(premia_models.PolicyCover(
                        **pgit_pol_risk_cover_data_pydantic.model_dump(exclude_none=True, exclude_unset=True)))

                # Motor Risk details
                pgit_pol_risk_addl_info_data = {
                    **policy_template_dict["pgit_pol_risk_addl_info_template"][0],
                    **quote_risk,
                    "policycover_collection": pgit_pol_risk_cover_list_db,
                    "prai_sys_id": prai_sys_id,
                    "prai_pol_sys_id": pol_sys_id,
                    "prai_psec_sys_id": psec_sys_id,
                    "prai_lvl1_sys_id": prai_sys_id,
                    "prai_eff_fm_dt": proposal["pol_fm_dt"],
                    "prai_eff_to_dt": proposal["pol_to_dt"],
                    "prai_period": 365,  # TODO: Calculate from dates
                    "prai_prod_code": proposal["pol_prod_code"],
                    "prai_dept_code": proposal["pol_dept_code"],
                    "prai_risk_ref_no": quote_risk["prai_risk_id"],
                    "prai_cr_uid": "PORTAL-REG",
                    "prai_cr_dt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                pgit_pol_risk_addl_info_data_pydantic = PolicyRiskCreate(**pgit_pol_risk_addl_info_data)
                pgit_pol_risk_addl_info_db = premia_models.PolicyRisk(
                    **pgit_pol_risk_addl_info_data_pydantic.model_dump(exclude_none=True, exclude_unset=True))
                pgit_pol_risk_addl_info_list_db.append(pgit_pol_risk_addl_info_db)

                # Motor Cert Details
                quote_certs_list = quote_risk.pop("proposalmotorcerts", None)
                prai_cert_sys_id = premia_services.get_sys_id(non_async_oracle_db, "pgi_prai_sys_id")
                pgit_pol_risk_cert_info_data = {
                    **policy_template_dict["pgit_pol_risk_cert_info_template"][0],
                    **quote_certs_list[0],
                    "prai_sys_id": prai_cert_sys_id,
                    "prai_pol_sys_id": pol_sys_id,
                    "prai_psec_sys_id": psec_sys_id,
                    "prai_lvl1_sys_id": prai_sys_id,
                    "prai_lvl2_sys_id": prai_cert_sys_id,
                    "prai_eff_fm_dt": proposal["pol_fm_dt"],
                    "prai_eff_to_dt": proposal["pol_to_dt"],
                    "prai_prod_code": proposal["pol_prod_code"],
                    "prai_dept_code": proposal["pol_dept_code"],
                    "prai_period": 365,  # TODO: Calculate from dates
                    # "prai_risk_id": "2",  # TODO: Should be 3.
                    # # "prai_risk_sr_no": 1,  # TODO: Calculate from number of risks. But check
                    "prai_cr_uid": "PORTAL-REG",
                    "prai_cr_dt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                pgit_pol_risk_cert_info_data_pydantic = PolicyRiskCreate(**pgit_pol_risk_cert_info_data)
                pgit_pol_risk_cert_info_db = premia_models.PolicyRisk(
                    **pgit_pol_risk_cert_info_data_pydantic.model_dump(exclude_none=True, exclude_unset=True))
                pgit_pol_risk_addl_info_list_db.append(pgit_pol_risk_cert_info_db)

            pgit_pol_section_data = {
                **policy_template_dict["pgit_pol_section"][0],
                **quote_section,
                "policyrisk_collection": pgit_pol_risk_addl_info_list_db,
                "psec_sys_id": psec_sys_id,
                "psec_pol_sys_id": pol_sys_id,
                "psec_eff_fm_dt": proposal["pol_fm_dt"],
                "psec_eff_to_dt": proposal["pol_to_dt"],
                "psec_prod_code": proposal["pol_prod_code"],
                "psec_dept_code": proposal["pol_dept_code"],
                "psec_cr_uid": "PORTAL-REG",
                "psec_cr_dt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            pgit_pol_section_data_pydantic = PolicySectionCreate(**pgit_pol_section_data)
            pgit_pol_section_db = premia_models.PolicySection(
                **pgit_pol_section_data_pydantic.model_dump(exclude_none=True, exclude_unset=True))
            pgit_pol_section_list_db.append(pgit_pol_section_db)

        pgit_policy_data = {
            **policy_template_dict["pgit_policy_template"],
            **proposal,
            "policycharge_collection": pgit_pol_charge_list_db,
            "policysection_collection": pgit_pol_section_list_db,
            "policycurrency_collection": pgit_pol_appl_curr_list_db,
            "policyhypothecation_collection": pgit_pol_hypothecation_list_db,
            "pol_sys_id": pol_sys_id,
            "pol_no": str(pol_sys_id),
            "pol_uw_year": datetime.now().year,
            "pol_cal_yr": datetime.now().year,
            "pol_cust_code": current_user.cust_code,
            # "pol_src_code": proposal["pol_cust_code"], # current_user.cust_code,
            "pol_src_type": "1" if current_user.cust_cc_code in ['01', '10'] else "2",
            "pol_src_code": "" if current_user.cust_cc_code in ['01', '10'] else current_user.cust_code,
            "pol_assr_name": quote_data["quot_assr_name"],
            "pol_issue_dt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "pol_period": 365,  # TODO: Calculate based on the period
            "pol_no_risk": 1,  # TODO: Calculate from number of risks
            "pol_no_section": 1,  # TODO: Calculate from number of sections
            "pol_city": "NAIROBI",  # TODO: Get from quote
            "pol_civil_id": quote_data["quot_assr_pin"],
            "pol_ref_no": quote_data["quot_assr_nic"],
            "pol_email_id": quote_data["quot_assr_email"],
            "pol_quot_recvd_dt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "pol_cr_uid": "PORTAL-REG",
            "pol_cr_dt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        pgit_policy_data_pydantic = PolicyCreate(**pgit_policy_data)
        pgit_policy_db = premia_models.Policy(**pgit_policy_data)
        pgit_policy_list_db.append(pgit_policy_db)

        policy = premia_services.create_policy(non_async_oracle_db, pgit_policy_data_pydantic)
        policy_process_json = premia_services.policy_process_json(non_async_oracle_db, policy)
        policy = premia_services.get_policy(non_async_oracle_db, policy)
        policy_process_dict = json.loads(policy_process_json)
        r_sys_id = premia_services.get_sys_id(non_async_oracle_db, "jaz_r_sys_id")
        fw_receipt_stage_data = {
            "r_sys_id": r_sys_id,
            "r_comp_code": "001",
            "r_tran_code": "RVCGP100",
            "r_doc_dt": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
            "r_divn_code": "",
            "r_dept_code": "",  # TODO: Get from quote
            "r_rcpt_option": "1",
            "r_rcpt_mode": "M-pesa",
            "r_rcvd_from": "2",
            "r_party_code": current_user.cust_code,
            "r_curr_code": "KES",
            "r_fc_amt": quote_data["quot_paymt_amt"],
            "r_lc_amt": quote_data["quot_paymt_amt"],
            "r_remarks": policy_process_dict["PR_POL_CONFIRM"]["P_POL_NO"],
            "r_cust_ref": quote_data["quot_paymt_ref"],
            "r_our_ref": quote_data["quot_paymt_ref"],
            "r_bank_code": "",
            "r_bank_acnt_no": "",
            "r_chq_no": quote_data["quot_paymt_ref"],
            "r_chq_dt": quote_data["quot_paymt_date"],
            "r_o_main_acnt_code": "151011",
            "r_o_sub_acnt_code": current_user.cust_code,
            "r_o_remarks": policy_process_dict["PR_POL_CONFIRM"]["P_POL_NO"],
            "r_o_fc_amt": quote_data["quot_paymt_amt"],
            "r_cr_dt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "r_cr_uid": "PORTAL-REG"
        }
        fw_receipt_data_pydantic = ReceiptStagingCreate(**fw_receipt_stage_data)
        receipt_stage = premia_services.create_receipt_stage(non_async_oracle_db, fw_receipt_data_pydantic)
        # receipt_process_json = premia_services.receipt_process_json(non_async_oracle_db, receipt_stage)
        # receipt_process_dict = json.loads(receipt_process_json)
        policy_process_dict['AUTO_RECEIPT'] = {}  # receipt_process_dict
    # TODO: Approve policy, Close RI
    # TODO: Return policy details and update quote
    # policy_process_dict = json.loads(policy_process_json)
    return policy_process_dict


def merge_lists_by_key(unique_key: str, dest_list: list[dict[str, Any]], update_list: list[dict[str, Any]]) -> list[
    dict[str, Any]]:
    # Extract the set of valid unique keys from list2
    valid_keys: set[Any] = {item[unique_key] for item in update_list}

    # Filter dest_list to keep items that are also represented in valid_keys
    filtered_dest_list = [item for item in dest_list if item[unique_key] in valid_keys]

    # Create a dictionary from update_list keyed by unique_key for easy lookup
    lookup_dict = {item[unique_key]: item for item in update_list}

    # Merge and update filtered_list1 with values from list2
    merged_list = [
        {**item, **lookup_dict.get(item[unique_key], {})} for item in filtered_dest_list
    ]

    return merged_list


def merge_dict_data_by_key(unique_key: str, dest_list: list[dict[str, Any]], update_dict: dict[str, Any]) -> list[
    dict[str, Any]]:
    # Extract the set of valid unique keys from list2
    valid_keys: set[Any] = {item[unique_key] for item in update_dict}

    # Filter dest_list to keep items that are also represented in valid_keys
    filtered_dest_list = [item for item in dest_list if item[unique_key] in valid_keys]

    # Create a dictionary from update_list keyed by unique_key for easy lookup
    lookup_dict = {item[unique_key]: item for item in update_dict}

    # Merge and update filtered_list1 with values from list2
    merged_list = [
        {**item, **lookup_dict.get(item[unique_key], {})} for item in filtered_dest_list
    ]

    return merged_list


def flatten_flexi(flexi):
    result = {}
    for outer_key, inner_dict in flexi.items():
        if isinstance(inner_dict, dict):
            result.update(inner_dict)
    return result


def validate_prefix(input_data, valid_prefixes):
    result = {}

    for key, value in input_data.items():
        # Check if the key starts with any of the valid prefixes
        if any(key.startswith(prefix) for prefix in valid_prefixes):
            if isinstance(value, dict):
                # Recursively validate nested dictionaries
                # nested_result = validate_prefix(value, valid_prefixes)
                nested_result = flatten_flexi(value)
                result.update(nested_result)
            else:
                # Add the field if the prefix is valid
                result[key] = value

    return result


def quote_to_policy(data):
    transformed = []

    # Define the valid prefixes for each section
    proposal_prefixes = ['pol_']
    section_prefixes = ['psec_']
    risk_prefixes = ['prai_']
    cert_prefixes = ['prai_']
    cover_prefixes = ['prc_']
    charge_prefixes = ['pchg_']

    for proposal in data["proposals"]:
        # Validate proposal level keys
        proposal_valid = validate_prefix(proposal, proposal_prefixes)

        # Process proposal sections
        proposal_valid['proposalsections'] = []
        for section in proposal["proposalsections"]:
            section_valid = validate_prefix(section, section_prefixes)

            # Process proposal risks
            section_valid['proposalrisks'] = []
            for risk in section["proposalrisks"]:
                risk_valid = validate_prefix(risk, risk_prefixes)

                # Process proposal covers
                risk_valid['proposalcovers'] = []
                for cover in risk["proposalcovers"]:
                    cover_valid = validate_prefix(cover, cover_prefixes)
                    risk_valid['proposalcovers'].append(cover_valid)

                # Process proposal certs
                risk_valid['proposalmotorcerts'] = []
                for cert in risk["proposalmotorcerts"]:
                    cert_valid = validate_prefix(cert, cert_prefixes)
                    risk_valid['proposalmotorcerts'].append(cert_valid)

                section_valid['proposalrisks'].append(risk_valid)

            proposal_valid['proposalsections'].append(section_valid)

        # Process proposal charges
        proposal_valid['proposalcharges'] = []
        for charge in proposal["proposalcharges"]:
            charge_valid = validate_prefix(charge, charge_prefixes)
            proposal_valid['proposalcharges'].append(charge_valid)

        transformed.append(proposal_valid)

    return transformed


# Function to flatten a single Proposal object
def flatten_proposal(proposal: models.Proposal) -> dict:
    # Extract the basic fields from the model and convert them to a dictionary
    proposal_dict = {
        "pol_quot_sys_id": proposal.pol_quot_sys_id,
        "pol_quot_no": proposal.pol_quot_no,
        "pol_comp_code": proposal.pol_comp_code,
        "pol_divn_code": proposal.pol_divn_code,
        "pol_dept_code": proposal.pol_dept_code,
        "pol_prod_code": proposal.pol_prod_code,
        "pol_type": proposal.pol_type,
        "pol_cust_code": proposal.pol_cust_code,
        "pol_assr_code": proposal.pol_assr_code,
        "pol_fm_dt": proposal.pol_fm_dt.isoformat(),  # Convert datetime to ISO format
        "pol_to_dt": proposal.pol_to_dt.isoformat(),  # Convert datetime to ISO format
        "pol_uw_year": proposal.pol_fm_dt.year,
        "pol_dflt_si_curr_code": proposal.pol_dflt_si_curr_code,
        "pol_prem_curr_code": proposal.pol_prem_curr_code,
        "pol_cr_uid": "PORTAL-REG",
        "pol_cr_dt": proposal.created_at.strftime("%Y-%m-%d %H:%M:%S"),
    }

    # Flatten the pol_flexi (JSONB) field if it exists
    if proposal.pol_flexi:
        for outer_key, inner_dict in proposal.pol_flexi.items():
            if isinstance(inner_dict, dict):
                proposal_dict.update(inner_dict)

    return proposal_dict


# Function to flatten a list of Proposal objects
def flatten_proposals(proposals: list[models.Proposal]) -> list[dict]:
    # Use list comprehension to flatten each proposal
    return [flatten_proposal(proposal) for proposal in proposals]


@router.post("/dyn_marine_payload", response_model=str)
async def dyn_marine_payload(
        *,
        current_user: user_models.User = Depends(auth_dependencies.get_current_user),
        async_db: AsyncSession = Depends(get_session),
        oracle_db: Session = Depends(get_oracle_session_sim),
        payload_in: vendor_schemas.QuoteMarineEncCreate,
) -> Any:
    # obj_in = {"pl_data": payload_in}
    payload = await quotes_crud.payload.create_v2(  # noqa: F841
        async_db, obj_in=payload_in
    )

    data = aes_decrypt(payload_in.MCINotification)
    data_dict = json.loads(data)

    payload_updated = await quotes_crud.payload.update(  # noqa: F841
        async_db, db_obj=payload, obj_in={"payload": data_dict}
    )

    data_schema = vendor_schemas.QuoteMarineCreate(**data_dict)

    # noinspection PyShadowingNames
    quote: Quote = await quote_services.create_quote(  # noqa: F841
        async_db, oracle_db, data_schema
    )

    resp = '{"status": "00", "reference":"' + data_dict["Reference"] + '"}'
    # resp_json = json.dumps(resp)

    return aes_encrypt(resp)
    pass


@router.post("/test_encrypt", response_model=str)
async def test_encrypt(payload_in: str) -> Any:
    # Encrypting...
    data = payload_in.encode()
    # key = b"abcdefghijk23456"  # get_random_bytes(16)
    key = b"gr9lj7i1f4vpck1a"  # livewire
    cipher = AES.new(key, AES.MODE_ECB)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    # ct_bytes = cipher.encrypt(data)
    # iv = b64encode(cipher.iv).decode("utf-8")
    ct = b64encode(ct_bytes).decode("utf-8")
    # ct = ct_bytes.decode("utf-8")
    # enc_result = json.dumps({"ciphertext": ct})
    # print(enc_result)
    return ct


@router.post("/test_decrypt", response_model=dict[str, Any])
async def test_decrypt(payload_in: str) -> Any:
    # Decrypting...
    # key = b"abcdefghijk23456"  # get_random_bytes(16)
    key = b"gr9lj7i1f4vpck1a"  # livewire
    # b64 = json.loads(payload_in)
    # iv = b64decode(b64['iv'])
    ct = b64decode(payload_in.encode())
    cipher = AES.new(key, AES.MODE_ECB)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    # pt = cipher.decrypt(ct)
    pt_str = "".join(c for c in pt.decode() if c.isprintable())
    # print(pt_str)

    # return {"The payload is": pt.decode().rstrip()}
    # return pt.decode().replace("\n", "")
    # return pt.decode().replace("\n", "").strip()
    return json.loads(pt_str)


@router.post("/quote_cust")  # dict[str, Any] , response_model=schemas.Quote
async def quote_cust(
        *,
        oracle_db: Session = Depends(get_non_async_oracle_session),
        payload_in: schemas.QuoteCreate,
        # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    # customer = customers_crud.get_customer("152917x")  # noqa: F841
    # return customer
    policy = customers_crud.get_tables()
    return policy
    # return {"test_key": "test_value"}


@router.post("/test_reflection")  # dict[str, Any] , response_model=schemas.Quote
async def test_reflection(
        *,
        oracle_db: Session = Depends(get_non_async_oracle_session),
        async_db: AsyncSession = Depends(get_session),
        payload_in: schemas.QuoteCreate,
        # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    proposal_table = customers_crud.get_proposal_table()  # noqa: F841
    # Policy = orcl_base.classes.pgit_policy
    # quote = await quotes_crud.quote.create_v1(async_db, obj_in=payload_in)

    return proposal_table.columns._all_columns
    # return {"test_key": "test_value"}


@router.post("/test_ora_conn")  # dict[str, Any] , response_model=schemas.Quote
def test_oracle(
        *,
        oracle_db: Session = Depends(get_non_async_oracle_session),
        # payload_in: schemas_.PartnerTransBase,
        # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    result = oracle_db.execute(text("select * from jick_t where rownum<=6"))
    return result.scalars().all()

    # ################################################################################
    # ################################################
    # # print("Before product template")
    # policy_template = await masters_crud.product.get_product_by_id(async_db, prod_code='1002')
    # # print("After product template")
    # ###########
    # pgit_policy_template = {k: v for k, v in policy_template.pol_trans_dflt.items() if v != ''}
    # policy_template_charges_list = [{k: v for k, v in charge.chg_trans_dflt.items() if v != ''} for charge in
    #                                 policy_template.charges]
    #
    # # This gives a flatenned policy template
    # policy_template_dict = {"pgit_policy_template": pgit_policy_template,
    #                         "pgit_pol_charge_template": policy_template_charges_list}
    # policy_template_sections_list = []
    # for quote_section in policy_template.sections:
    #     if quote_section.sec_trans_dflt is not None:
    #         pgit_pol_section_template = {k: v for k, v in quote_section.sec_trans_dflt.items() if v != ''}
    #         policy_template_sections_list.append(pgit_pol_section_template)
    # policy_template_dict["pgit_pol_section"] = policy_template_sections_list
    #
    # policy_template_risks_list = []
    # for quote_section in policy_template.sections:
    #     if quote_section.sec_trans_dflt is not None:
    #         for risk in quote_section.section.risks:
    #             if risk.risk_trans_dflt is not None:
    #                 pgit_pol_risk_addl_info_template = {k: v for k, v in risk.risk_trans_dflt.items() if v != ''}
    #                 policy_template_risks_list.append(pgit_pol_risk_addl_info_template)
    # policy_template_dict["pgit_pol_risk_addl_info_template"] = policy_template_risks_list
    #
    # policy_template_covers_list = []
    # for quote_section in policy_template.sections:
    #     if quote_section.sec_trans_dflt is not None:
    #         for risk in quote_section.section.risks:
    #             if risk.risk_trans_dflt is not None:
    #                 for cover in risk.risk.covers:
    #                     if cover.cvr_trans_dflt is not None:
    #                         policy_template_covers_list.append(
    #                             {k: v for k, v in cover.cvr_trans_dflt.items() if v != ''})
    # policy_template_dict["pgit_pol_risk_cover_template"] = policy_template_covers_list
    # ################################################################################
