from datetime import datetime
from typing import Union

from pydantic import BaseModel


# ########## Proposal Schema #########
# Shared properties
class ProposalBase(BaseModel):
    prop_sys_id: Union[int | None] = None
    prop_sr_no: Union[int | None] = None
    prop_paymt_ref: Union[str | None] = None
    prop_paymt_date: Union[datetime | None] = None
    pol_quot_sys_id: Union[int | None] = None
    pol_quot_no: Union[str | None] = None
    pol_comp_code: Union[str | None] = None
    pol_divn_code: Union[str | None] = None
    pol_prod_code: Union[str | None] = None
    pol_type: Union[str | None] = None
    pol_cust_code: Union[str | None] = None
    pol_assr_code: Union[str | None] = None
    pol_fm_dt: Union[datetime | None] = None
    pol_to_dt: Union[datetime | None] = None
    pol_dflt_si_curr_code: Union[str | None] = None
    pol_prem_curr_code: Union[str | None] = None
