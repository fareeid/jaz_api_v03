import os

from fastapi import APIRouter, Form, Query
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

# current_file_path = os.path.realpath(__file__)
# print(f"path_str:{path_str}")
# print(f"current_dir:{current_file_path}")

path_str = os.path.dirname(os.path.realpath(__file__))
# router.mount('/static', StaticFiles(directory=f"{path_str}/static"), name='static')
templates = Jinja2Templates(directory=f"{path_str}/templates")
# router.mount("/static", StaticFiles(directory="/usr/src/app/src/static"), name="static")
# templates = Jinja2Templates(directory="/usr/src/app/src/templates")

count = 0
tasks_db = []


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks_db})
    return templates.TemplateResponse(request=request, name="index.html", context={"tasks": tasks_db})


@router.post("/")
async def add_task(request: Request, task: str = Form(...), descriptions: str = Form(...)):
    global count
    data = {"id": count, 'title': task, "descriptions": descriptions}
    tasks_db.append(data)
    count += 1
    return RedirectResponse(url="/portalx", status_code=303)


@router.post("/delete-task/", response_class=HTMLResponse)
async def delete_task(request: Request, task_index: int = Form(...)):
    for i, task in enumerate(tasks_db):
        if int(task['id']) == int(task_index):
            del tasks_db[i]
    return RedirectResponse(url="/portalx/table", status_code=303)


@router.get("/table", response_class=HTMLResponse)
async def read_data(request: Request):
    # return templates.TemplateResponse("tables.html",{"request": request,"tasks": tasks_db})
    return templates.TemplateResponse(request=request, name="tables.html", context={"tasks": tasks_db})


@router.get("/update-task/", response_class=HTMLResponse)
async def update_task(request: Request, task_index: int = Query(...)):
    for task in tasks_db:
        if task['id'] == task_index:
            # print(task)
            # return templates.TemplateResponse("update.html", {"request": request, "tasks": task})
            return templates.TemplateResponse(request=request, name="update.html", context={"tasks": task})


@router.post("/update-task")
async def add_task(request: Request, id: str = Form(...), title: str = Form(...), descriptions: str = Form(...)):
    for i, task in enumerate(tasks_db):
        if int(task['id']) == int(id):
            del tasks_db[i]

    data = {"id": int(id), 'title': title, "descriptions": descriptions}
    tasks_db.append(data)
    return RedirectResponse(url="/portalx/table", status_code=303)