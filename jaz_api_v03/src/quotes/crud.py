# from typing import Any, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.crud_base import CRUDBase

# from ..quotes.models import (
#     Quote, ProposalCharge, ProposalCover, ProposalRisk, ProposalSection, ProposalSMI,
# )
from . import models, schemas

# from .schemas import QuoteCreate, QuoteUpdate


class CRUDQuote(CRUDBase[models.Quote, schemas.QuoteCreate, schemas.QuoteUpdate]):  # type: ignore  # noqa: E501
    async def create_v1(
        self, async_db: AsyncSession, *, obj_in: schemas.QuoteCreate
    ) -> models.Quote:
        quote_dict = jsonable_encoder(obj_in.dict(exclude_unset=True))

        proposals_list = obj_in.proposals
        proposals_list_db = []
        for proposal in proposals_list:
            charges_list = proposal.proposalcharges
            charges_list_db = [
                models.ProposalCharge(**charge.dict(exclude_unset=True))
                for charge in charges_list
            ]

            sections_list = proposal.proposalsections
            sections_list_db = []
            for section in sections_list:
                risks_list = section.proposalrisks
                risks_list_db = []
                for risk in risks_list:
                    covers_list = risk.proposalcovers
                    covers_list_db = [
                        models.ProposalCover(**cover.dict(exclude_unset=True))
                        for cover in covers_list
                    ]
                    smis_list = risk.proposalsmis
                    smis_list_db = [
                        models.ProposalSMI(**smi.dict(exclude_unset=True))
                        for smi in smis_list
                    ]
                    risk_dict = risk.dict(exclude_unset=True)
                    risk_dict["proposalcovers"] = covers_list_db
                    risk_dict["proposalsmis"] = smis_list_db
                    # prai_flexi_field = risk_dict["prai_flexi"][0]
                    # del risk_dict["prai_flexi"]
                    # print(prai_flexi_field)
                    # risk_dict["prai_flexi"] = prai_flexi_field
                    risk_db = models.ProposalRisk(**risk_dict)
                    risks_list_db.append(risk_db)
                section_dict = section.dict(exclude_unset=True)
                section_dict["proposalrisks"] = risks_list_db
                section_db = models.ProposalSection(**section_dict)
                sections_list_db.append(section_db)
            proposal_dict = proposal.dict(exclude_unset=True)
            proposal_dict["proposalsections"] = sections_list_db
            proposal_dict["proposalcharges"] = charges_list_db
            proposal_db = models.Proposal(**proposal_dict)
            proposals_list_db.append(proposal_db)

        quote_dict = obj_in.dict(exclude_unset=True)  # type: ignore
        quote_dict["proposals"] = proposals_list_db
        return await super().create_v1(async_db, obj_in=quote_dict)


quote = CRUDQuote(models.Quote)
