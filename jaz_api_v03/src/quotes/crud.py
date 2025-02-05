# from typing import Any
from typing import Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# from ..quotes.models import (
#     Quote, ProposalCharge, ProposalCover, ProposalRisk, ProposalSection, ProposalSMI,
# )
from . import models, schemas
from .vendors_api import models as vendor_models
from .vendors_api import schemas as vendor_schemas
from ..db.crud_base import CRUDBase


# from .schemas import QuoteCreate, QuoteUpdate


class CRUDPayload(
    CRUDBase[
        vendor_models.Payload,
        vendor_schemas.QuoteMarineEncCreate,
        vendor_schemas.QuoteMarineUpdate,
    ]
):
    async def create_v2(
            self, async_db: AsyncSession, *, obj_in: vendor_schemas.QuoteMarineEncCreate
    ) -> vendor_models.Payload:
        quote_marine_dict = jsonable_encoder(obj_in.model_dump(exclude_unset=True))
        # quote_marine_db = vendor_models.Payload(**quote_marine_dict)

        return await super().create_v2(async_db, obj_in=quote_marine_dict)


class CRUDQuote(
    CRUDBase[models.Quote, schemas.QuoteCreate, schemas.QuoteUpdate]
):  # noqa: E501
    async def create_v1(
            self, async_db: AsyncSession, *, obj_in: schemas.QuoteCreate
    ) -> models.Quote:
        quote_dict = jsonable_encoder(obj_in.model_dump(exclude_unset=True))
        # quote_dict = obj_in.model_dump(exclude_unset=True)

        proposals_list = obj_in.proposals
        proposals_list_db = []
        for prop in proposals_list:
            charges_list = prop.proposalcharges
            # for charge in charges_list:
            #     charge_dict = jsonable_encoder(**charge.model_dump(exclude_unset=True))
            #     charge.pchg_flexi = charge_dict
            #     charges_list_db.append(charge_dict)
            charges_list_db = [
                models.ProposalCharge(**charge.model_dump(exclude_unset=True))
                for charge in charges_list
            ]

            premiums_list = prop.proposalpremiums
            premiums_list_db = []
            for premium in premiums_list:
                installments_list = premium.proposalinstallments
                installments_list_db = [
                    models.ProposalInstallment(**installment.model_dump(exclude_unset=True))
                    for installment in installments_list
                ]
                premium_dict = premium.model_dump(exclude_unset=True)
                premium_dict["proposalinstallments"] = installments_list_db
                premium_db = models.ProposalPremium(**premium_dict)
                premiums_list_db.append(premium_db)

            sections_list = prop.proposalsections
            sections_list_db = []
            for section in sections_list:
                risks_list = section.proposalrisks
                risks_list_db = []
                for risk in risks_list:
                    covers_list = risk.proposalcovers
                    covers_list_db = [
                        models.ProposalCover(**cover.model_dump(exclude_unset=True))
                        for cover in covers_list
                    ]
                    smis_list = risk.proposalsmis
                    smis_list_db = [
                        models.ProposalSMI(**smi.model_dump(exclude_unset=True))
                        for smi in smis_list
                    ]
                    motor_cert_list = risk.proposalmotorcerts
                    motor_cert_list_db = [
                        models.ProposalMotorCert(
                            **motor_cert.model_dump(exclude_unset=True)
                        )
                        for motor_cert in motor_cert_list
                    ]
                    risk_dict = risk.model_dump(exclude_unset=True)
                    risk_dict["proposalcovers"] = covers_list_db
                    risk_dict["proposalsmis"] = smis_list_db
                    risk_dict["proposalmotorcerts"] = motor_cert_list_db
                    # prai_flexi_field = risk_dict["prai_flexi"][0]
                    # del risk_dict["prai_flexi"]
                    # print(prai_flexi_field)
                    # risk_dict["prai_flexi"] = prai_flexi_field
                    risk_db = models.ProposalRisk(**risk_dict)
                    risks_list_db.append(risk_db)
                section_dict = section.model_dump(exclude_unset=True)
                section_dict["proposalrisks"] = risks_list_db
                section_db = models.ProposalSection(**section_dict)
                sections_list_db.append(section_db)
            proposal_dict = prop.model_dump(exclude_unset=True)
            proposal_dict["proposalsections"] = sections_list_db
            proposal_dict["proposalcharges"] = charges_list_db
            proposal_dict["proposalpremiums"] = premiums_list_db
            proposal_db = models.Proposal(**proposal_dict)
            proposals_list_db.append(proposal_db)

        quote_dict = obj_in.model_dump(exclude_unset=True)
        quote_dict["proposals"] = proposals_list_db
        return await super().create_v1(async_db, obj_in=quote_dict)


class CRUDProposal(
    CRUDBase[models.Proposal, schemas.ProposalCreate, schemas.ProposalUpdate]
):
    async def get_proposal_fields(self, async_db: AsyncSession, attr_name: str) -> dict[
        str, Any]:  # list[master_models.AttributeDefinition]:
        stmt = (
            select(self.model.pol_quot_sys_id, self.model.pol_quot_no, self.model.pol_comp_code,
                   self.model.pol_divn_code, self.model.pol_dept_code,
                   self.model.pol_prod_code, self.model.pol_type, self.model.pol_cust_code, self.model.pol_assr_code,
                   self.model.pol_fm_dt,
                   self.model.pol_to_dt, self.model.pol_dflt_si_curr_code, self.model.pol_prem_curr_code,
                   self.model.pol_flexi)
            # .join(self.json_attribute_alias, self.model.jsonattributes)
            .filter(self.model.attr_name == attr_name)
        )
        result = await async_db.execute(stmt)

        # Fetch the first row, if any
        row = result.fetchone()

        # Return a dictionary if a row is found, otherwise an empty dictionary
        if row:
            attr_name, data_type, entity_type, json_value = row
            return {
                "attr_name": attr_name,
                "data_type": data_type,
                "entity_type": entity_type,
                "json_value": json_value
            }
        return {}

    async def get_proposal(self, async_db: AsyncSession, sys_id: int) -> models.Proposal:
        prop = await super().get_by_id(async_db, id=sys_id)
        return prop


payload = CRUDPayload(vendor_models.Payload)
quote = CRUDQuote(models.Quote)
proposal = CRUDProposal(models.Proposal)
