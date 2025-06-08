import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import uuid
from datetime import datetime

from report_gen import generate_pdf

def test_generate_pdf():
    report_data = {
        "incident_id": str(uuid.uuid4()), 
        "user_id": str(uuid.uuid4()),  
        "description": "This is a test incident for report generation.",
        "incident_type": "Harassment",
        "date_time": str(datetime.now()),
        "location": "Office",
        "severity": "HIGH"  
    }

    reports_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../reports"))
    os.makedirs(reports_folder, exist_ok=True)

    pdf_path = generate_pdf(report_data)
    print(f"Report saved at: {pdf_path}")
    
    assert os.path.exists(pdf_path), "PDF was not created"
    
    os.remove(pdf_path)
    print("Test Passed: PDF Generation Successful")

if __name__ == "__main__":
    test_generate_pdf()
