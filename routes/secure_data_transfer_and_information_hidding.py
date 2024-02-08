from fastapi import APIRouter, Request, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from cv2 import imwrite
import os

from projects_documents.EmbeddingExtractingPart import embedding_to_img, extracting_embedded_data

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/Secure-Data-Transfer-and-Information-Hiding/", response_class=HTMLResponse)
async def embedding_page(request: Request):
    return templates.TemplateResponse("Secure-Data-Transfer-and-Information-Hiding.html", {"request": request})

@router.post("/Secure-Data-Transfer-and-Information-Hiding/embedding/")
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



@router.get("/download-image/")
async def download_image():
    if not uploaded_image_path:
        raise HTTPException(status_code=404, detail="No image available for download.")
    print(uploaded_image_path)
    # Endpoint for downloading the embedded image
    return FileResponse(uploaded_image_path, media_type="application/octet-stream", filename="embedded_image.png")

@router.post("/Secure-Data-Transfer-and-Information-Hiding/extracting/")
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
    