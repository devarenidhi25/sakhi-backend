from fastapi import APIRouter, HTTPException
from services.nlp_analysis import analyzer
import logging
from pydantic import BaseModel
#from database import reports_collection
import time
router = APIRouter()
logger = logging.getLogger(__name__)

class SeverityRequest(BaseModel):
    incident_text: str
    incident_id: str = None

class SeverityResponse(BaseModel):
    incident_id: str
    severity: str
    status: str


@router.post("/", response_model=SeverityResponse)
async def check_severity(data: SeverityRequest):
    '''severity = classify_severity(data["incident_text"])
    ##reports_collection.update_one({"incident_id": data["incident_id"]}, {"$set": {"severity": severity}})
    return {"incident_id": data["incident_id"], "severity": severity}'''
    
    try:
        incident_id = data.incident_id or f"SK-{int(time.time())}"
        logger.info(f"Processing severity check for incident: {incident_id}")
        
        severity = analyzer.classify_severity(data.incident_text)

        response_data = SeverityResponse(
            incident_id=incident_id,
            severity=severity,
            status="success"
        )

        logger.info(f"Severity check complete: {response_data}")
        # print("This is data:",response_data)
        return response_data

    except Exception as e:
        logger.error(f"Error in check_severity: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")