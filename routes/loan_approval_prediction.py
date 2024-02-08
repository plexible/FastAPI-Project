from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from joblib import load
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/loan-approval-prediction/", response_class=HTMLResponse)
async def loan_approval_prediction(request: Request):
    return templates.TemplateResponse("loan-approval-prediction.html", {"request": request})

def preprocess_user_input(user_input, scaler):
    scaled_input = scaler.transform([user_input])
    return scaled_input

@router.post("/loan-approval-prediction/")
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
        if prediction_result is not None:
            prediction_result = "Not approved" if prediction_result == 0 else "Approved"
            success_message = "Prediction completed"
            return JSONResponse(content={ "success_message": success_message, "prediction": prediction_result})
        else:
            raise HTTPException(status_code=400, detail="Failed to predict")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
