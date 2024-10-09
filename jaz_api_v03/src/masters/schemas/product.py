from typing import Union

from pydantic import BaseModel


class ProductBase(BaseModel):
    prod_sys_id: int
    prod_code: str
    prod_desc: str
    prod_frz_flag: bool
    pol_trans_dflt: Union[dict, None] = None # JSONB is mapped as dict

    # Many-to-many relationships
    charges: list = []
    conditions: list = []
    sections: list = []
