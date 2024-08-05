import os
import random
import urllib.parse as urlparse
from typing import Union, Any

from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import HTMLResponse

from . import schemas

router = APIRouter()
path_str = os.path.dirname(os.path.realpath(__file__))
templates = Jinja2Templates(directory=f"{path_str}/stockwatcher")
MAX_PRICE = 100.0
MAX_PRICE_CHANGE = 0.02


@router.get("/gwt_static/stockwatcher/stock_data_local", response_model=list[schemas.Stock])
async def stock_data_local(q: Union[str, None] = None) -> Any:
    form = {}
    querystr = "q=" + q if q else ""
    form = dict(urlparse.parse_qsl(querystr))
    body = '['
    if 'q' in form:
        quotes = []

        for symbol in urlparse.unquote_plus(form['q']).split(' '):
            price = random.random() * MAX_PRICE
            change = price * MAX_PRICE_CHANGE * (random.random() * 2.0 - 1.0)
            stock = schemas.Stock(symbol=symbol, price=price, change=change)
            quotes.append(stock)

    return quotes


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks_db})
    return templates.TemplateResponse(request=request, name="index.html", context={"tasks": "tasks_db"})
