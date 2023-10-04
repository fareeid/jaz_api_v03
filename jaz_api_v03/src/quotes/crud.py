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

        # if quote_dict.proposals.get("charges"):
        #     charges_list = [
        #         models.ProposalCharge(**charge) for charge in quote_dict["charges"]
        #     ]

        # if quote_dict.get("smis"):
        #     smis_list = [models.ProposalSMI(**smi) for smi in quote_dict["smis"]]

        # if quote_dict.get("covers"):
        #     covers_list = [
        #         models.ProposalCover(**cover) for cover in quote_dict["covers"]
        #     ]

        # if quote_dict.get("risks"):
        #     quote_dict.risks["covers"] = covers_list
        #     quote_dict.risks["smis"] = smis_list
        #     risks_list = [models.ProposalSMI(**risk) for risk in quote_dict["risks"]]

        # if quote_dict.get("sections"):
        #     quote_dict.sections["risks"] = risks_list
        #     sections_list = [
        #         models.ProposalSection(**section) for section in quote_dict["sections"]  # noqa: E501
        #     ]

        # if quote_dict.get("proposals"):
        #     quote_dict.proposals["sections"] = sections_list
        #     quote_dict.proposals["charges"] = charges_list
        #     proposals_list = [
        #         models.Proposal(**proposal) for proposal in quote_dict["proposals"]
        #     ]
        #     quote_dict["proposals"]

        quote_dict = obj_in.dict(exclude_unset=True)  # type: ignore
        return await super().create_v1(async_db, obj_in=quote_dict)


quote = CRUDQuote(models.Quote)
