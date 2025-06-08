from fastapi import FastAPI, HTTPException, Depends, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.requests import Request
from routes.report import router as report_router
from routes.severity import router as severity_router
from routes.chatbot import router as chatbot_router
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from dotenv import load_dotenv
from authlib.integrations.starlette_client import OAuth
from pydantic import BaseModel
import logging
import os
import jwt
from datetime import datetime, timedelta
import bcrypt

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
#GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
#GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# MongoDB Connection
client = MongoClient(MONGO_URI)
db = client["user_database"]
users_collection = db["users"]

app = FastAPI()

# Middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware for session handling
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")

'''
# OAuth for Google Login
oauth = OAuth()
oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params={"scope": "openid email profile"},
    access_token_url="https://oauth2.googleapis.com/token",
    client_kwargs={"scope": "openid email profile"},
)
'''
# Add middleware to protect routes
async def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

@app.post("/signin")
async def signin(response: Response, form_data: dict):
    try:
        # Find user in database
        user = users_collection.find_one({"username": form_data["username"]})
        
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
            
        # Verify password
        if not verify_password(form_data["password"], user["password"]):
            raise HTTPException(status_code=401, detail="Incorrect password")

        # Create access token
        access_token = create_access_token(
            data={"sub": user["username"]}
        )

        # Set cookie with token
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            max_age=1800,  # 30 minutes
            samesite="lax"
        )

        return {
            "message": "Login successful",
            "username": user["username"],
            "access_token": access_token
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
app.include_router(report_router, prefix="/report", tags=["Incident Report"])
app.include_router(severity_router, prefix="/severity", tags=["Severity Analysis"])
app.include_router(chatbot_router, prefix="/chatbot", tags=["SAKHI"])

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")    
templates = Jinja2Templates(directory="templates")

# Define routes with UNIQUE paths
@app.get("/", response_class=HTMLResponse)
async def serve_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/sign-in", response_class=HTMLResponse)
async def serve_sign(request: Request):
    return templates.TemplateResponse("sign-in.html", {"request": request})


@app.get("/sign-up", response_class=HTMLResponse)
async def serve_signup(request: Request):
    return templates.TemplateResponse("sign-up.html", {"request": request})

@app.get("/form", response_class=HTMLResponse)
async def serve_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.get("/chatbot", response_class=HTMLResponse)
async def serve_chatbot(request: Request):
    return templates.TemplateResponse("chatbot.html", {"request": request})

@app.get("/chatbot/context")
async def get_chatbot_context():
    return {"message": "How can I help you with your situation?"}

class IncidentRequest(BaseModel):
    incident_text: str
from services.nlp_analysis import analyzer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/nlp_analysis")
async def analyze_severity(incident: IncidentRequest):
    """Calls the NLP model to classify incident severity."""
    
    # try:
    #     severity = analyzer.classify_severity(incident.incident_text)
    #     incident_id = f"SK-{hash(incident.incident_text)}"

    #     return {
    #         "incident_id": incident_id,
    #         "severity": severity
    #     }
    # except Exception as e:
    #     logger.error(f"Error analyzing severity: {e}")
    #     raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/api-status")
def root():
    return {"message": "API running successfully"}  


# User Model
class User(BaseModel):
    username: str
    email: str
    password: str

# Password Hashing Function
def hash_password(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# OAuth2 Scheme for Login
#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# SIGN UP ENDPOINT
@app.post("/signup")
async def signup(user: User):
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(user.password)
    users_collection.insert_one({"username": user.username, "email": user.email, "password": hashed_password})

    return {"message": "User registered successfully"}


# SIGN IN ENDPOINT
@app.post("/signin")
async def signin(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_collection.find_one({"email": form_data.username})  # username here is email
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful"}

'''
# GOOGLE LOGIN ENDPOINTS
@app.get("/google-login")
async def google_login(request: Request):
    redirect_uri = request.url_for("google_auth")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/google-auth")
async def google_auth(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.parse_id_token(request, token)

    # Check if user exists in database
    user = users_collection.find_one({"email": user_info["email"]})
    if not user:
        users_collection.insert_one({"username": user_info["name"], "email": user_info["email"], "password": None})
    
    return {"message": "Google login successful", "user": user_info}'''
