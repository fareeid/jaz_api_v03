from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy import text  # Column, Integer, MetaData, String, Table, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from ..core.dependencies import get_oracle_session, get_session
from . import crud, models, schemas, schemas_  # noqa: F401

# from . import schemas, schemas_

router = APIRouter()


def create_covers_list(
    payload_in: schemas_.PartnerTransBase,
) -> list[schemas.ProposalCoverCreate]:
    covers_list = []
    proposal_cover_obj = schemas.ProposalCoverCreate(
        cvr_sr_no=1,
        prc_code="3553",
        prc_rate=1.75,
        prc_rate_per=1000,
        prc_si_curr_code="KES",
        prc_prem_curr_code="KES",
        prc_si_fc=payload_in.items_total_cost,
        prc_prem_fc=payload_in.premium.basic_prem,
    )
    covers_list.append(proposal_cover_obj)
    return covers_list


def create_smis_list(
    payload_in: schemas_.PartnerTransBase,
) -> list[schemas.ProposalSMICreate]:
    items = payload_in.items
    smis_list = []
    for item in enumerate(items, 1):
        sr_no, smi = item
        proposal_smi_obj = schemas.ProposalSMICreate(
            smi_sr_no=sr_no,
            prs_smi_code=smi.item_code,
            prs_rate=1.75,
            prs_rate_per=100,
            prs_si_fc=smi.item_cost,
            prs_prem_fc=smi.item_prem,
            prs_smi_desc=f"Details(name={smi.item_name!r}, make={smi.item_make!r}, model={smi.item_model!r}, serial_num={smi.item_serial_num!r})",  # noqa: E501
        )
        smis_list.append(proposal_smi_obj)
    return smis_list


def create_risks_list(
    covers_list: list[schemas.ProposalCoverCreate],
    smis_list: list[schemas.ProposalSMICreate],
) -> list[schemas.ProposalRiskCreate]:
    risks_list = []
    proposal_risk_obj = schemas.ProposalRiskCreate(
        risk_sr_no=1,
        prai_data_18="Kenya",
        prai_code_03="503",
        prai_desc_09="Residential",
        proposalcovers=covers_list,
        proposalsmis=smis_list,
    )
    risks_list.append(proposal_risk_obj)
    return risks_list


def create_sections_list(
    risks_list: list[schemas.ProposalRiskCreate],
) -> list[schemas.ProposalSectionCreate]:
    sections_list = []
    proposal_section_obj = schemas.ProposalSectionCreate(
        sec_sr_no=1, psec_sec_code="500601", proposalrisks=risks_list
    )
    sections_list.append(proposal_section_obj)
    return sections_list


def create_charges_list(
    payload_in: schemas_.PartnerTransBase,
) -> list[schemas.ProposalChargeCreate]:
    premium_items = payload_in.premium
    charges_list = []
    stamp_duty_obj = schemas.ProposalChargeCreate(
        chg_sr_no=1,
        pchg_code="stamp_duty",
        pchg_type="stamp_duty",
        pchg_perc=100,
        pchg_chg_fc=premium_items.stamp_duty,
        pchg_prem_curr_code="KES",
        pchg_rate_per=100,
    )
    pcf_obj = schemas.ProposalChargeCreate(
        chg_sr_no=1,
        pchg_code="pcf",
        pchg_type="pcf",
        pchg_perc=0.25,
        pchg_chg_fc=premium_items.pcf,
        pchg_prem_curr_code="KES",
        pchg_rate_per=100,
    )
    itl_obj = schemas.ProposalChargeCreate(
        chg_sr_no=1,
        pchg_code="itl",
        pchg_type="itl",
        pchg_perc=0.20,
        pchg_chg_fc=premium_items.itl,
        pchg_prem_curr_code="KES",
        pchg_rate_per=100,
    )
    charges_list.append(stamp_duty_obj)
    charges_list.append(pcf_obj)
    charges_list.append(itl_obj)
    return charges_list


def create_proposals_list(
    payload_in: schemas_.PartnerTransBase,
    sections_list: list[schemas.ProposalSectionCreate],
    charges_list: list[schemas.ProposalChargeCreate],
) -> list[schemas.ProposalCreate]:
    proposals_list = []
    proposal_obj = schemas.ProposalCreate(
        prop_sr_no=1,
        prop_paymt_ref=payload_in.prem_payment_ref,
        prop_paymt_date=payload_in.prem_payment_date,
        pol_quot_no=payload_in.trans_ref,
        pol_comp_code="001",
        pol_divn_code="101",
        pol_prod_code="5006",
        pol_type="5006",
        pol_cust_code="K21006439",
        pol_assr_code="K99999999",
        pol_fm_dt=payload_in.start_date,
        pol_to_dt=payload_in.end_date,
        pol_prem_curr_code="KES",
        pol_dflt_si_curr_code="KES",
        proposalsections=sections_list,
        proposalcharges=charges_list,
    )
    proposals_list.append(proposal_obj)
    return proposals_list


@router.post("/mfs_payload", response_model=schemas.Quote)  # dict[str, Any]
async def send_payload(
    *,
    async_db: AsyncSession = Depends(get_session),
    payload_in: schemas_.PartnerTransBase,
    # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    # 1. Search and/or create customer details in premia

    covers_list = create_covers_list(payload_in)
    smis_list = create_smis_list(payload_in)
    risks_list = create_risks_list(covers_list, smis_list)
    sections_list = create_sections_list(risks_list)
    charges_list = create_charges_list(payload_in)
    proposals_list = create_proposals_list(payload_in, sections_list, charges_list)

    # 8. Create quote
    quote_obj = schemas.QuoteCreate(
        quot_ref=payload_in.trans_ref,
        quot_paymt_ref=payload_in.prem_payment_ref,
        quot_paymt_date=payload_in.prem_payment_date,
        proposals=proposals_list,
    )
    # return quote_obj.dict()
    quote = await crud.quote.create_v1(async_db, obj_in=quote_obj)

    # user = await crud.user.get_by_email(async_db, email=payload_in.customer_email)
    # return {"test_key": "test_value"}
    return quote


@router.post("/quote", response_model=dict[str, Any])  # schemas.Quote
async def quote(
    *,
    async_db: AsyncSession = Depends(get_session),
    payload_in: schemas.QuoteCreate,
    # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    return {"test_key": "test_value"}


@router.post("/test_ora_conn")  # dict[str, Any] , response_model=schemas.Quote
def test_oracle(
    *,
    oracle_db: Session = Depends(get_oracle_session),
    payload_in: schemas_.PartnerTransBase,
    # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    result = oracle_db.execute(text("select * from jick_t where rownum<=6"))
    return result.scalars().all()
