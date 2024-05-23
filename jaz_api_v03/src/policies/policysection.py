# from datetime import datetime
from typing import Union

from pydantic import BaseModel


# ########## Section Schema #########
# Shared properties
class PolicySectionBase(BaseModel):
    pol_sys_id: Union[int | None] = None
    pol_end_no_idx: Union[int | None] = None
    pol_end_sr_no: Union[int | None] = None
    pol_comp_code: Union[str | None] = None
