from typing import Union

from pydantic import BaseModel, ConfigDict


class StockBase(BaseModel):
    symbol: Union[str | None] = None
    price: Union[float | None] = None
    change: Union[float | None] = None


# Properties to receive via API on creation
class StockCreate(StockBase):
    symbol: str


class StockInDBBase(StockBase):
    model_config = ConfigDict(from_attributes=True)


class Stock(StockInDBBase):
    pass