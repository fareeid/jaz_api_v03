from datetime import datetime, timedelta
from typing import Any, Union

from dateutil import parser
# from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from . import crud as quotes_crud
from . import schemas as quote_schemas
from .vendors_api import schemas as vendor_schemas
from ..auth import schemas as user_schemas
from ..auth import services as user_services
from ..core.dependencies import get_non_async_oracle_session, get_oracle_session_sim  # noqa: F401


def parse_datetime(date_string: str, default: Union[datetime | None] = None) -> Any:
    try:
        return parser.parse(date_string, dayfirst=True)
    except (ValueError, TypeError):
        return default


def parse_float(float_string: str, default: Union[float | None] = 0) -> Any:
    try:
        return float(float_string)
    except (ValueError, TypeError):
        return default


def create_covers_list(
    payload_in: vendor_schemas.QuoteMarineCreate,
) -> list[quote_schemas.ProposalCoverCreate]:
    covers_list = []
    proposal_cover_obj = quote_schemas.ProposalCoverCreate(
        cvr_sr_no=1,
        prc_code="3301",
        prc_rate=1.75,
        prc_rate_per=1000,
        prc_si_curr_code="KES",
        prc_prem_curr_code="KES",
        prc_si_fc=parse_float(payload_in.MCI_Cargo_invoiceamount),
        prc_prem_fc=parse_float(payload_in.MCI_MPESAAmount),
    )
    covers_list.append(proposal_cover_obj)
    return covers_list


def create_smis_list(
    payload_in: vendor_schemas.QuoteMarineCreate,
) -> list[quote_schemas.ProposalSMICreate]:
    smis_list = []
    proposal_smi_obj = quote_schemas.ProposalSMICreate(
        smi_sr_no=1,
        prs_smi_code="23001",
        prs_rate=1.75,
        prs_rate_per=1000,
        prs_si_fc=parse_float(payload_in.MCI_Cargo_invoiceamount),
        prs_prem_fc=parse_float(payload_in.MCI_MPESAAmount),
        prs_smi_desc="Finished Products",
    )
    smis_list.append(proposal_smi_obj)
    return smis_list


def create_risks_list(
    payload_in: vendor_schemas.QuoteMarineCreate,
    covers_list: list[quote_schemas.ProposalCoverCreate],
    smis_list: list[quote_schemas.ProposalSMICreate],
) -> list[quote_schemas.ProposalRiskCreate]:
    risks_list = []
    flexi_dict = {}
    flexi_dict["transit_type"] = {"prai_code_07": payload_in.MCI_Cargo_ModeofTransport}
    flexi_dict["goods_desc"] = {"prai_remarks_06": payload_in.MCI_Cargo_Description}
    flexi_dict["vessel_name"] = {"prai_data_04": payload_in.MCI_Vessel_Name}
    flexi_dict["port_from_code"] = {"prai_code_02": payload_in.MCI_Cargo_originport}
    flexi_dict["port_to_code"] = {"prai_code_08": payload_in.MCI_Cargo_destinationport}
    flexi_dict["final_dest"] = {"prai_data_01": payload_in.MCI_Cargo_destinationport}
    flexi_dict["voyage_desc"] = {"prai_data_05": "ENTIRE VOYAGE"}
    flexi_dict["cargo_value"] = {"prai_num_01": str(payload_in.MCI_Cargo_invoiceamount)}
    flexi_dict["shipment_mode_code"] = {
        "prai_code_01": payload_in.MCI_Cargo_ModeofTransport
    }
    flexi_dict["valuation_basis_code"] = {"prai_code_04": "001"}
    flexi_dict["shipment_si"] = {"prai_num_07": str(payload_in.MCI_Cargo_invoiceamount)}
    flexi_dict["cargo_type_code"] = {"prai_code_03": "300"}
    flexi_dict["idf_number"] = {"prai_data_06": payload_in.MCI_Cargo_IDF}
    proposal_risk_obj = quote_schemas.ProposalRiskCreate(
        risk_sr_no=1,
        prai_flexi=flexi_dict,
        proposalcovers=covers_list,
        proposalsmis=smis_list,
    )
    risks_list.append(proposal_risk_obj)
    return risks_list


def create_sections_list(
    risks_list: list[quote_schemas.ProposalRiskCreate],
) -> list[quote_schemas.ProposalSectionCreate]:
    sections_list = []
    proposal_section_obj = quote_schemas.ProposalSectionCreate(
        sec_sr_no=1, psec_sec_code="300302", proposalrisks=risks_list
    )
    sections_list.append(proposal_section_obj)
    return sections_list


def create_charges_list(
    payload_in: vendor_schemas.QuoteMarineCreate,
) -> list[quote_schemas.ProposalChargeCreate]:
    charges_list = []
    stamp_duty_obj = quote_schemas.ProposalChargeCreate(
        chg_sr_no=1,
        pchg_code="2003",
        pchg_type="002",
        pchg_perc=0.05,
        pchg_chg_fc=parse_float(payload_in.MCI_Cargo_invoiceamount) * 0.05 / 100,
        pchg_prem_curr_code="KES",
        pchg_rate_per=100,
    )
    pcf_obj = quote_schemas.ProposalChargeCreate(
        chg_sr_no=1,
        pchg_code="1004",
        pchg_type="005",
        pchg_perc=0.25,
        pchg_chg_fc=parse_float(payload_in.MCI_MPESAAmount) * 0.25 / 100,
        pchg_prem_curr_code="KES",
        pchg_rate_per=100,
    )
    itl_obj = quote_schemas.ProposalChargeCreate(
        chg_sr_no=1,
        pchg_code="2004",
        pchg_type="002",
        pchg_perc=0.20,
        pchg_chg_fc=parse_float(payload_in.MCI_MPESAAmount) * 0.2 / 100,
        pchg_prem_curr_code="KES",
        pchg_rate_per=100,
    )
    charges_list.append(stamp_duty_obj)
    charges_list.append(pcf_obj)
    charges_list.append(itl_obj)
    return charges_list


def create_proposals_list(
    payload_in: vendor_schemas.QuoteMarineCreate,
    sections_list: list[quote_schemas.ProposalSectionCreate],
    charges_list: list[quote_schemas.ProposalChargeCreate],
) -> list[quote_schemas.ProposalCreate]:
    proposals_list = []
    proposal_obj = quote_schemas.ProposalCreate(
        prop_sr_no=1,
        prop_paymt_ref=payload_in.MCI_MPESAReference,
        # prop_paymt_date=datetime.strptime(
        #     payload_in.MCI_MPESAPayDate, "%Y-%m-%d %H:%M:%S"
        # ),
        prop_paymt_date=parse_datetime(payload_in.MCI_MPESAPayDate),
        pol_quot_no=payload_in.Reference,
        pol_comp_code="001",
        pol_divn_code="101",
        pol_dept_code="30",
        pol_prod_code="3001",
        pol_type="5006",
        pol_cust_code="200396",
        pol_assr_code="K99999999",
        # pol_fm_dt=datetime.strptime(payload_in.MCI_Cargo_loadingdate, "%d/%m/%Y"),
        # pol_to_dt=datetime.strptime(payload_in.MCI_Cargo_dischargedate, "%d/%m/%Y"),
        pol_fm_dt=parse_datetime(payload_in.MCI_MPESAPayDate),
        pol_to_dt=parse_datetime(payload_in.MCI_MPESAPayDate)
        + timedelta(days=int(payload_in.MCI_Cargo_InsuranceCoverPeriodDays)),
        pol_prem_curr_code="KES",
        pol_dflt_si_curr_code="KES",
        proposalsections=sections_list,
        proposalcharges=charges_list,
    )
    proposals_list.append(proposal_obj)
    return proposals_list


# def get_cust_by_pin(
#     *,
#     # oracle_db: Session = Depends(get_oracle_session),
#     oracle_db: Session = Depends(get_oracle_session_sim),
#     pin: str,
#     # current_user: models.User = Depends(deps.get_current_active_superuser),
# ) -> Any:
#     # customer = customers_crud.get_customer("152917")  # noqa: F841
#     policy = premia_crud.customer.get_cust_by_pin(oracle_db, pin="A016034508E")
#     return policy
#     # return {"test_key": "test_value"}
#     pass


async def create_quote(
    async_db: AsyncSession,
    oracle_db: Session,
    payload_in: vendor_schemas.QuoteMarineCreate,
) -> Any:
    quote_marine_dict = jsonable_encoder(  # noqa: F841
        payload_in.model_dump(exclude_unset=True)
    )

    # 1.  Create/Search User
    user_obj = user_schemas.UserCreate(
        first_name=payload_in.MCI_Cargo_ImporterName,
        name=payload_in.MCI_Cargo_ImporterName,
        email=payload_in.MCI_CAEmail,
        # username=payload_in.MCI_CAEmail,
        pin=payload_in.MCI_Cargo_ImporterPIN,
    )

    user = await user_services.get_user(async_db, user_obj)

    # TO DO: Create/Fetch customer in/from Premia based on user
    # customer = premia_services.get_cust_by_pin(  # noqa: F841
    #     oracle_db, payload_in.MCI_Cargo_ImporterPIN
    # )

    covers_list = create_covers_list(payload_in)
    smis_list = create_smis_list(payload_in)
    risks_list = create_risks_list(payload_in, covers_list, smis_list)
    sections_list = create_sections_list(risks_list)
    charges_list = create_charges_list(payload_in)
    proposals_list = create_proposals_list(payload_in, sections_list, charges_list)

    quote_obj = quote_schemas.QuoteCreate(
        quot_ref=payload_in.Reference,
        quot_paymt_ref=payload_in.MCI_MPESAReference,
        # quot_paymt_date=datetime.strptime(
        #     payload_in.MCI_MPESAPayDate, "%Y-%m-%d %H:%M:%S"
        # ),
        quot_paymt_date=parse_datetime(payload_in.MCI_MPESAPayDate),
        quot_assr_id=user.id,
        proposals=proposals_list,
    )

    quote = await quotes_crud.quote.create_v1(async_db, obj_in=quote_obj)
    return quote

    # 2. Create quote payload
    # covers_list =
