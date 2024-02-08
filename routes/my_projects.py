from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/my-projects/", response_class=HTMLResponse)
async def my_projects(request: Request):
    return templates.TemplateResponse("my-projects.html", {"request": request})
