# **Women’s Workplace Safety & Support System (SAKHI)**

**SAKHI** is a web-based platform designed to provide a safe and supportive space for women across various workplaces to report incidents such as harassment, verbal abuse, or unsafe working conditions. The system allows female employees to securely report workplace incidents, receive AI-driven mental health and legal guidance through a chatbot, and ensures confidentiality and compliance with **The POSH Act, 2013**. The system generates reports and sends them to the Internal Complaints Committee (IIC) for redressal.

---

## **Features**

- **Anonymous Reporting**: Allows users to report incidents anonymously or with their details (name, email, employee ID).
- **Incident Classification**: Uses NLP to detect the severity of the incident (high or low).
- **AI-Driven Support**: If the incident severity is low, users can interact with a chatbot for mental health support.
- **PDF Report Generation**: For high-severity incidents, a detailed report is generated and sent to the Internal Complaints Committee (IIC).
- **Legal Awareness**: Provides basic legal guidance related to workplace harassment and informs users about their rights under The POSH Act, 2013.
- **Data Privacy**: Ensures complete confidentiality and compliance with relevant workplace laws.

---

## **Technology Stack**

- **Backend**: 
  - **Python (FastAPI)** for handling NLP and generating PDF reports.
  - **Node.js** for handling API requests, interacting with the Gemini API, and managing chat functionality.
  
- **NLP (Natural Language Processing)**: 
  - Pre-trained **DistilBERT** model (via **Hugging Face Transformers**) for classifying the severity of reported incidents.

- **Frontend**: 
  - **Bootstrap** for responsive, user-friendly interfaces.
  
- **Chatbot**: 
  - **Gemini API** for providing emotional support through an AI-driven chatbot.

- **PDF Generation**: 
  - **Python libraries** such as **reportlab** for generating the detailed incident report in PDF format.

---

## **How to Run the Project**

### **1. Clone the Repository**
git clone https://github.com/your-username/sakhi-workplace-safety.git
cd sakhi-workplace-safety

### **2. Install Backend Dependencies**
cd python-backend
pip install -r requirements.txt

uvicorn main:app --reload

### **Business Model for SAKHI: Women’s Workplace Safety & Support System**

**Value Proposition**:
- **For Women Employees**: Secure, anonymous reporting of workplace incidents (e.g., harassment), AI-driven emotional support, and legal guidance based on the POSH Act.
- **For Employers**: Ensures compliance with workplace safety laws, automates incident management, and provides data-driven insights for improving workplace culture.

**Revenue Model**:
1. **Subscription-based Model**: Organizations pay based on employee count for access to the platform's features.
2. **Freemium Model for Employees**: Free basic services with premium mental health and legal features.
3. **Data Analytics Reports**: Selling anonymized data insights to organizations for improving workplace culture.
4. **Legal Partnering**: Partnering with law firms for additional services.

**Target Audience**:
- Women employees across industries.
- Organizations seeking to provide a safe workplace and comply with legal standards.

**Marketing Strategy**:
- Target HR and legal teams in companies.
- Content marketing, partnerships with NGOs, webinars, and referral programs.

**Cost Structure**:
- Development, AI infrastructure, marketing, legal consultation, and server costs.

**Scalability**:
- Expand globally, continuously improve AI models, and add more premium features for employers and employees.

**Competitive Advantage**:
- Focus on privacy, AI-driven support, and a comprehensive solution for workplace safety, legal guidance, and emotional support.
