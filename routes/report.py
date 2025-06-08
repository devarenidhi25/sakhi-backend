from fastapi import APIRouter, HTTPException
#from database import reports_collection
from models import Report
from services.report_gen import generate_pdf
#from database import chatbot_history
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")  # Adjust if needed
db = client["sakhi_db"]
reports_collection = db["reports"]

router = APIRouter()

@router.post("/")
async def submit_report(report: Report):
    try:
        report_data = report.model_dump()  
        reports_collection.insert_one(report_data) 

        pdf_path = generate_pdf(report_data)

        return {
            "message": "Report submitted successfully!!!",
            "pdf": pdf_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

'''def store_chatbot_message(user_id, message, response):
    chatbot_history.insert_one({
        "user_id": user_id,
        "message": message,
        "response": response
    })'''
