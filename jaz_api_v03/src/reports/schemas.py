import calendar
from datetime import datetime
from typing import Union

from pydantic import BaseModel


class SearchCriteria(BaseModel):
    cust_code: Union[str | None] = None
    first_date: Union[datetime | None] = datetime(datetime.today().year, datetime.today().month, 1)
    last_date: Union[datetime | None] = datetime(datetime.today().year, datetime.today().month, calendar.monthrange(datetime.today().year, datetime.today().month)[1])
    page_no: Union[int | None] = 1
    rows_per_page: Union[int | None] = 25


class ReportParams(BaseModel):
    proc_name: Union[str | None] = None
    search_criteria: SearchCriteria
