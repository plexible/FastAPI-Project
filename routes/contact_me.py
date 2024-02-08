from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# E-posta ayarları
conf = ConnectionConfig(
    MAIL_USERNAME="your_mail@gmail.com",
    MAIL_PASSWORD="yourapppassword",
    MAIL_FROM="your_mail@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

mail = FastMail(conf)

@router.get("/contact-me/", response_class=HTMLResponse)
async def contact_me(request: Request):
    return templates.TemplateResponse("contact-me.html", {"request": request})

@router.post("/send-email/")
async def send_email(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    message: str = Form(...)
):    
    message_ = MessageSchema(
        subject=f"ContactMe Form {name}",
        recipients=["your_mail@gmail.com"],
        body=f"Name: {name}\nPhone: {phone}\nEmail: {email}\nMessage: {message}",
        subtype="html"
    )

    try:
        await mail.send_message(message_)
        success_message = "Sent Successfully"
        return templates.TemplateResponse(
            "contact-me.html",
            {"request": request, "success_message": success_message}
        )
    except Exception as e:
        error_message = f"Transaction could not be completed"
        return templates.TemplateResponse(
            "contact-me.html",
            {"request": request, "success_message": error_message}
        )
