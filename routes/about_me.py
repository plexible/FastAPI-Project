from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/about-me/", response_class=HTMLResponse)
async def about_me(request: Request):
    return templates.TemplateResponse("about-me.html", {"request": request})
