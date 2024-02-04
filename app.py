from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Form
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from typing import Dict, Any, List
from pathlib import Path
from pydantic import EmailStr, BaseModel
from projects_documents.EmbeddingExtractingPart import embedding_to_img, extracting_embedded_data
from cv2 import imwrite
import os
from joblib import load
import pandas

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})
@app.get("/about-me/", response_class=HTMLResponse)
async def about_me(request: Request):
    return templates.TemplateResponse("about-me.html", {"request": request})
@app.get("/contact-me/", response_class=HTMLResponse)
async def contact_me(request: Request):
    return templates.TemplateResponse("contact-me.html", {"request": request})
@app.get("/my-projects/", response_class=HTMLResponse)
async def my_prjects(request: Request):
    return templates.TemplateResponse("my-projects.html", {"request": request})
@app.get("/Secure-Data-Transfer-and-Information-Hiding/", response_class=HTMLResponse)
async def embedding_page(request: Request):
    return templates.TemplateResponse("Secure-Data-Transfer-and-Information-Hiding.html", {"request": request})
@app.get("/loan-approval-prediction/", response_class=HTMLResponse)
async def loan_approval_prediction(request: Request):
    return templates.TemplateResponse("loan-approval-prediction.html", {"request": request})


@app.post("/Secure-Data-Transfer-and-Information-Hiding/embedding/")
async def upload_image(
    request: Request,
    file: UploadFile = File(...),
    name: str = Form(...),
    surname: str = Form(...),
    tcno: str = Form(...),
):    
    global uploaded_image_path
    try:
        # Combine extracted information into a dictionary
        info_dict = {"name": name, "surname": surname, "tcno": tcno}

        # Save the uploaded image
        image_path = f"images/{file.filename}"
        with open(image_path, "wb") as image_file:
            image_file.write(file.file.read())
            
        new_img = embedding_to_img(image_path, info_dict)
        
        # Provide the path to the embedded image
        new_file_name = os.path.splitext(os.path.basename(image_path))[0]
        embedded_image_path = os.path.join("uploads", f"embedded_{new_file_name}.png")
        embedded_img = os.path.join("static", "uploads", f"embedded_{new_file_name}.png")
        uploaded_image_path = embedded_img
        print(uploaded_image_path)
        imwrite(embedded_img, new_img)
        
        if embedded_image_path:
            success_message = "Embedding completed"
            return JSONResponse(content={"success_message": success_message, "embedded_image": embedded_image_path})
        else:
            raise HTTPException(status_code=400, detail="Failed to extract information from the image")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")



@app.get("/download-image/")
async def download_image():
    if not uploaded_image_path:
        raise HTTPException(status_code=404, detail="No image available for download.")
    print(uploaded_image_path)
    # Endpoint for downloading the embedded image
    return FileResponse(uploaded_image_path, media_type="application/octet-stream", filename="embedded_image.png")

@app.post("/Secure-Data-Transfer-and-Information-Hiding/extracting/")
async def extracting(request: Request, file: UploadFile = File(...)):
    try:
        # Save the uploaded image
        image_path = f"images/{file.filename}"
        print(image_path)
        with open(image_path, "wb") as image_file:
            image_file.write(file.file.read())
        extracted_info = extracting_embedded_data(image_path)
        if extracted_info:
            success_message = "Extracting completed"
            return JSONResponse(content={ "success_message": success_message, **extracted_info})
        else:
            raise HTTPException(status_code=400, detail="Failed to extract information from the image")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
def preprocess_user_input(user_input, scaler):
    scaled_input = scaler.transform([user_input])
    return scaled_input

@app.post("/loan-approval-prediction/")
async def prediction(request: Request, 
    current_loan_amount: str = Form(...),
    term: str = Form(...),
    credit_score: str = Form(...),
    annual_income: str = Form(...),
    home_ownership: str = Form(...),
    monthly_debt: str = Form(...),
    years_of_credit_history: str = Form(...),
    number_of_open_accounts: str = Form(...)):
    try:
        input_data = [
            float(current_loan_amount),
            int(term),
            float(credit_score),
            float(annual_income),
            int(home_ownership),
            float(monthly_debt),
            float(years_of_credit_history),
            float(number_of_open_accounts)
        ]
        loaded_model = load('projects_documents/random_forest_model.joblib')
        scaler = load('projects_documents/scaler.joblib')
        scaled_input = preprocess_user_input(input_data, scaler)
        prediction = loaded_model.predict(scaled_input)
        prediction_result = prediction[0]
        if prediction_result != None:
            prediction_result = "Not approved" if prediction_result == 0 else "Approved"
            success_message = "Prediction completed"
            return JSONResponse(content={ "success_message": success_message, "prediction": prediction_result})
        else:
            raise HTTPException(status_code=400, detail="Failed to predict")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

  
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

# E-posta gönderme endpoint'i
@app.post("/send-email/")
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)