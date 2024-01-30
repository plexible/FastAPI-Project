from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Dict, Any
from pathlib import Path
from EmbeddingExtractingPart import embedding_to_img, extracting_embedded_data
from cv2 import imwrite
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})
@app.get("/about-me/", response_class=HTMLResponse)
async def about_us(request: Request):
    return templates.TemplateResponse("about-me.html", {"request": request})
@app.get("/contact-me/", response_class=HTMLResponse)
async def about_us(request: Request):
    return templates.TemplateResponse("contact-me.html", {"request": request})
@app.get("/embedding/", response_class=HTMLResponse)
async def embedding_page(request: Request):
    return templates.TemplateResponse("embedding-page.html", {"request": request})
@app.get("/extracting/", response_class=HTMLResponse)
async def extracting_page(request: Request):
    return templates.TemplateResponse("extracting-page.html", {"request": request})

@app.post("/embedding/")
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
        image_path = os.path.join("images", file.filename)
        new_file_name = os.path.splitext(os.path.basename(image_path))[0]
        embedded_image_path = os.path.join("uploads", f"embedded_{new_file_name}.png")
        embedded_img = os.path.join("static/uploads", f"embedded_{new_file_name}.png")
        uploaded_image_path = embedded_image_path
        print(uploaded_image_path)
        imwrite(embedded_img, new_img)
        # Set success message
        success_message = "Embedding completed"
        return templates.TemplateResponse(
            "embedding-page.html",
            {"request": request, "success_message": success_message, "embedded_image": uploaded_image_path}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/download-image/")
async def download_image():
    if not uploaded_image_path:
        raise HTTPException(status_code=404, detail="No image available for download.")
    print(uploaded_image_path)
    # Endpoint for downloading the embedded image
    return FileResponse(uploaded_image_path, media_type="application/octet-stream", filename="embedded_image.png")

@app.post("/extracting/")
async def extracting(request: Request, file: UploadFile = File(...)):
    try:
        # Save the uploaded image
        image_path = f"images/{file.filename}"
        print(image_path)
        with open(image_path, "wb") as image_file:
            image_file.write(file.file.read())
        extracted_info = extracting_embedded_data(image_path)
        success_message = "Extracting completed"
        return templates.TemplateResponse(
            "extracting-page.html",
            {"request": request, "success_message": success_message, "name": extracted_info["name"], 
                "surname": extracted_info["surname"], "tcno": extracted_info["tcno"]}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
        
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)