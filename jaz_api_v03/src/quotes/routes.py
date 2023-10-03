from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy import text  # Column, Integer, MetaData, String, Table, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from ..core.dependencies import get_oracle_session, get_session
from . import crud, schemas, schemas_

# from . import schemas, schemas_

router = APIRouter()


@router.post("/send_payload", response_model=schemas.Quote)  # dict[str, Any]
async def send_payload(
    *,
    async_db: AsyncSession = Depends(get_session),
    payload_in: schemas_.PartnerTransBase,
    # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    # 1. Search and/or create customer details in premia

    # 2. create list of proposal covers
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

    # 3. create list of proposal smis
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

    # 4. Create list of proposal risks
    risks_list = []
    proposal_risk_obj = schemas.ProposalRiskCreate(
        risk_sr_no=1,
        prai_data_18="Kenya",
        prai_code_03="503",
        prai_desc_09="Residential",
        covers=covers_list,
        smis=smis_list,
    )
    risks_list.append(proposal_risk_obj)

    # 5. create section
    sections_list = []
    proposal_section_obj = schemas.ProposalSectionCreate(
        sec_sr_no=1, psec_sec_code="500601", risks=risks_list
    )
    sections_list.append(proposal_section_obj)

    # 6. create proposal
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
        pol_fm_dt=payload_in.start_date,
        pol_to_dt=payload_in.end_date,
        pol_prem_curr_code="KES",
        pol_dflt_si_curr_code="KES",
    )
    proposals_list.append(proposal_obj)

    # 8. Create quote
    quote_obj = schemas.QuoteCreate(
        quot_ref=payload_in.trans_ref,
        quot_paymt_ref=payload_in.prem_payment_ref,
        quot_paymt_date=payload_in.prem_payment_date,
        proposals=proposals_list,
    )
    # quote_obj.dict()
    quote = await crud.quote.create(async_db, obj_in=quote_obj)

    # 7. create cover
    # 8. create charges

    # user = await crud.user.get_by_email(async_db, email=payload_in.customer_email)
    # return {"test_key": "test_value"}
    return quote


@router.post("/test_ora_conn")  # dict[str, Any] , response_model=schemas.Quote
def test_oracle(
    *,
    oracle_db: Session = Depends(get_oracle_session),
    payload_in: schemas_.PartnerTransBase,
    # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    result = oracle_db.execute(text("select * from jick_t where rownum<=5"))
    return result.scalars().all()
    # list(result.scalars().all())
    # list(result.scalars().all())
