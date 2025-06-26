from fastapi import APIRouter, HTTPException
from models import Report
from services.report_gen import generate_pdf
from pymongo import MongoClient
import os

router = APIRouter()

# Load Mongo URI securely
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URL)
db = client["sakhi_db"]
reports_collection = db["reports"]

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
