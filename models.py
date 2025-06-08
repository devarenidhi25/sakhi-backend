from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Report(BaseModel):
    incident_id: str
    user_id: str
    description: str
    incident_type: str
    date_time: datetime
    location: str
    #evidence: Optional[str]= None
    severity: Optional[str]= "PENDING"