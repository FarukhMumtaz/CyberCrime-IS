"""
Cyber Crime Reporting System - Backend API

FastAPI backend for secure processing of complaints, evidence, and AI services.
"""

from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Form, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
import os
import logging
from datetime import datetime
import re
import hashlib
import magic
from dotenv import load_dotenv
import jwt
from cryptography.fernet import Fernet
import groq
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import io
import uuid

# Configure logging early for import-time errors
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables before service initialization
load_dotenv()

# Import services (with error handling)
try:
    from backend.services import db_service, ai_service, file_service
except ImportError as e:
    try:
        from services import db_service, ai_service, file_service
    except ImportError as fallback_error:
        logger.error(f"Failed to import services: {fallback_error}")
        db_service = None
        ai_service = None
        file_service = None

try:
    from backend.models import UserCreate, ComplaintCreate, TokenData
except ImportError as e:
    try:
        from models import UserCreate, ComplaintCreate, TokenData
    except ImportError as fallback_error:
        logger.error(f"Failed to import models: {fallback_error}")
        # Define minimal models locally if import fails
        from pydantic import BaseModel, Field
        class UserCreate(BaseModel):
            email: str
            password: str
        class ComplaintCreate(BaseModel):
            incident_date: str
            location: str
            complaint_reason: str
            description: str
        class TokenData(BaseModel):
            user_id: str
            exp: int

try:
    from backend.utils.security import SecurityUtils
except ImportError as e:
    try:
        from utils.security import SecurityUtils
    except ImportError as fallback_error:
        logger.error(f"Failed to import SecurityUtils: {fallback_error}")
        SecurityUtils = None

# Environment variables are loaded before service initialization above.

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Cyber Crime Reporting System API",
    description="Secure backend API for cybercrime reporting",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "https://*.streamlit.app"],  # Streamlit default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()
JWT_SECRET = os.getenv("JWT_SECRET_KEY")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
if ENCRYPTION_KEY:
    try:
        fernet = Fernet(ENCRYPTION_KEY.encode())
    except Exception as e:
        logger.warning(f"Invalid encryption key: {e}")
        fernet = None
else:
    logger.warning("Encryption key not set")
    fernet = None

# Supabase client
from supabase import create_client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_ANON_KEY") or os.getenv("SUPABASE_KEY")
if supabase_url and supabase_key:
    try:
        supabase = create_client(supabase_url, supabase_key)
        logger.info("Supabase client initialized")
    except Exception as e:
        logger.warning(f"Failed to initialize Supabase client: {e}")
        supabase = None
else:
    logger.warning("Supabase credentials not configured")
    supabase = None

# Groq client
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if GROQ_API_KEY:
    try:
        groq_client = groq.Client(api_key=GROQ_API_KEY)
    except Exception as e:
        logger.warning(f"Failed to initialize Groq client: {e}")
        groq_client = None
else:
    logger.warning("Groq API key not set")
    groq_client = None

# Pydantic models
class UserCreate(BaseModel):
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None
    phone: Optional[str] = None
    cnic: Optional[str] = Field(None, pattern=r"^\d{13}$")

class ComplaintCreate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    cnic: Optional[str] = Field(None, pattern=r"^\d{13}$")
    address: Optional[str] = None
    incident_date: str
    location: str
    complaint_reason: str
    description: str

    @validator('incident_date')
    def validate_date(cls, v):
        try:
            datetime.fromisoformat(v)
            return v
        except:
            raise ValueError('Invalid date format')

class TokenData(BaseModel):
    user_id: str
    exp: int

# Utility functions
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Verify JWT token and return user ID."""
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=["HS256"])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def generate_tracking_id() -> str:
    """Generate unique tracking ID."""
    year = datetime.now().year
    random_part = str(uuid.uuid4())[:6].upper()
    return f"CCRS-PK-{year}-{random_part}"

def validate_file(file: UploadFile, max_size: int, allowed_types: List[str]) -> Dict[str, Any]:
    """Validate uploaded file."""
    # Check file size
    file.file.seek(0, 2)  # Seek to end
    size = file.file.tell()
    file.file.seek(0)  # Reset to beginning

    if size > max_size:
        raise HTTPException(status_code=400, detail="File too large")

    # Check MIME type
    mime = magic.Magic(mime=True)
    file_content = file.file.read(1024)  # Read first 1KB
    detected_mime = mime.from_buffer(file_content)
    file.file.seek(0)  # Reset

    if detected_mime not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type")

    # Calculate hash
    sha256 = hashlib.sha256()
    file.file.seek(0)
    for chunk in iter(lambda: file.file.read(4096), b""):
        sha256.update(chunk)
    file.file.seek(0)

    return {
        "size": size,
        "mime_type": detected_mime,
        "sha256_hash": sha256.hexdigest()
    }

def encrypt_data(data: str) -> str:
    """Encrypt sensitive data."""
    if fernet:
        return fernet.encrypt(data.encode()).decode()
    return data

def decrypt_data(encrypted_data: str) -> str:
    """Decrypt sensitive data."""
    if fernet:
        return fernet.decrypt(encrypted_data.encode()).decode()
    return encrypted_data

# API Routes
@app.get("/")
async def root():
    """API root endpoint."""
    return {"message": "Cyber Crime Reporting System API", "version": "1.0.0"}

@app.post("/auth/register")
async def register_user(user: UserCreate):
    """Register a new user."""
    try:
        # Check if user already exists
        existing_user = db_service.get_user_by_email(user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        # Hash password
        hashed_password = SecurityUtils.hash_password(user.password)

        user_data = {
            "email": user.email,
            "hashed_password": hashed_password,
            "full_name": user.full_name,
            "phone": user.phone,
            "cnic": encrypt_data(user.cnic) if user.cnic else None,
            "is_active": True,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }

        user_id = db_service.create_user(user_data)
        if not user_id:
            raise HTTPException(status_code=500, detail="Failed to create user")

        # Create audit log
        db_service.create_audit_log({
            "action": "user_registered",
            "resource_type": "user",
            "resource_id": user_id,
            "details": {"email": user.email}
        })

        return {"message": "User registered successfully", "user_id": user_id}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(status_code=500, detail="Registration failed")

@app.post("/auth/login")
async def login_user(email: str = Form(...), password: str = Form(...)):
    """Authenticate user and return JWT token."""
    try:
        user = db_service.get_user_by_email(email)
        if not user or not SecurityUtils.verify_password(password, user['hashed_password']):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not user['is_active']:
            raise HTTPException(status_code=401, detail="Account deactivated")

        # Generate JWT token
        token = SecurityUtils.generate_jwt_token(user['id'])

        # Create audit log
        db_service.create_audit_log({
            "user_id": user['id'],
            "action": "user_login",
            "resource_type": "user",
            "resource_id": user['id'],
            "details": {"email": email}
        })

        return {"access_token": token, "token_type": "bearer"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail="Login failed")

@app.post("/complaints/")
async def create_complaint(
    complaint: ComplaintCreate,
    background_tasks: BackgroundTasks,
    user_id: Optional[str] = Depends(verify_token)
):
    """Create a new complaint."""
    try:
        tracking_id = generate_tracking_id()

        # Encrypt sensitive data
        encrypted_cnic = encrypt_data(complaint.cnic) if complaint.cnic else None

        complaint_data = {
            "tracking_id": tracking_id,
            "user_id": user_id,
            "full_name": complaint.full_name,
            "phone": complaint.phone,
            "cnic": encrypted_cnic,
            "address": complaint.address,
            "incident_date": complaint.incident_date,
            "location": complaint.location,
            "complaint_reason": complaint.complaint_reason,
            "description": complaint.description,
            "status": "submitted",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }

        complaint_id = db_service.create_complaint(complaint_data)
        if not complaint_id:
            raise HTTPException(status_code=500, detail="Failed to create complaint")

        # Background tasks for AI processing
        background_tasks.add_task(process_complaint_ai, tracking_id, complaint.description)

        # Create audit log
        db_service.create_audit_log({
            "user_id": user_id,
            "action": "complaint_submitted",
            "resource_type": "complaint",
            "resource_id": complaint_id,
            "details": {"tracking_id": tracking_id}
        })

        logger.info(f"Complaint created: {tracking_id}")
        return {
            "tracking_id": tracking_id,
            "message": "Complaint submitted successfully",
            "status": "submitted"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating complaint: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create complaint")

@app.post("/evidence/upload")
async def upload_evidence(
    complaint_id: str = Form(...),
    files: List[UploadFile] = File(...),
    user_id: str = Depends(verify_token)
):
    """Upload evidence files for a complaint."""
    uploaded_files = []

    for file in files:
        try:
            # Read file content
            file_content = await file.read()

            # Validate file
            validation_result = file_service.validate_file(file_content, file.filename)
            if not validation_result:
                uploaded_files.append({
                    "file_name": file.filename,
                    "status": "failed",
                    "error": "Invalid file type or size"
                })
                continue

            # Scan for malware
            malware_status = file_service.scan_for_malware(file_content)

            # Encrypt file
            encrypted_content = file_service.encrypt_file(file_content)

            # Generate secure filename
            secure_filename = file_service.generate_secure_filename(file.filename)

            # Upload to Supabase Storage
            file_path = f"evidence/{complaint_id}/{secure_filename}"
            if supabase:
                try:
                    supabase.storage.from_('evidence-files').upload(
                        file_path,
                        encrypted_content,
                        {"content-type": validation_result["mime_type"]}
                    )
                except Exception as e:
                    logger.error(f"Storage upload failed: {e}")
                    uploaded_files.append({
                        "file_name": file.filename,
                        "status": "failed",
                        "error": "Storage upload failed"
                    })
                    continue

            evidence_data = {
                "complaint_id": complaint_id,
                "file_name": secure_filename,
                "original_name": file.filename,
                "file_path": file_path,
                "file_type": validation_result["file_type"],
                "mime_type": validation_result["mime_type"],
                "file_size": validation_result["size"],
                "sha256_hash": validation_result["sha256_hash"],
                "is_encrypted": True,
                "malware_scan_status": malware_status,
                "uploaded_at": datetime.utcnow().isoformat()
            }

            evidence_id = db_service.create_evidence(evidence_data)

            # Create audit log
            db_service.create_audit_log({
                "user_id": user_id,
                "action": "evidence_uploaded",
                "resource_type": "evidence",
                "resource_id": evidence_id or complaint_id,
                "details": {"file_name": file.filename, "complaint_id": complaint_id}
            })

            uploaded_files.append({
                "file_name": file.filename,
                "status": "uploaded",
                "size": validation_result["size"]
            })

        except Exception as e:
            logger.error(f"Error uploading file {file.filename}: {str(e)}")
            uploaded_files.append({
                "file_name": file.filename,
                "status": "failed",
                "error": str(e)
            })

    return {"uploaded_files": uploaded_files}

@app.get("/laws/")
async def get_laws(category: Optional[str] = None, search: Optional[str] = None):
    """Get cyber laws with optional filtering."""
    try:
        laws = db_service.get_laws(category, search)
        return {"laws": laws}
    except Exception as e:
        logger.error(f"Error getting laws: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve laws")

@app.get("/complaints/{tracking_id}")
async def get_complaint(tracking_id: str, user_id: str = Depends(verify_token)):
    """Get complaint details by tracking ID."""
    try:
        complaint = db_service.get_complaint(tracking_id, user_id)
        if not complaint:
            raise HTTPException(status_code=404, detail="Complaint not found")

        # Decrypt sensitive data
        if complaint.get('cnic'):
            complaint['cnic'] = decrypt_data(complaint['cnic'])

        return {"complaint": complaint}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting complaint: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve complaint")

@app.get("/pdf/{tracking_id}")
async def generate_pdf(tracking_id: str, user_id: str = Depends(verify_token)):
    """Generate PDF report for complaint."""
    try:
        complaint = db_service.get_complaint(tracking_id, user_id)
        if not complaint:
            raise HTTPException(status_code=404, detail="Complaint not found")

        # Create PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()

        # PDF content
        content = [
            Paragraph("Cyber Crime Complaint Report", styles['Heading1']),
            Spacer(1, 12),
            Paragraph(f"Tracking ID: {tracking_id}", styles['Normal']),
            Paragraph(f"Status: {complaint.get('status', 'Unknown')}", styles['Normal']),
            Paragraph(f"Incident Date: {complaint.get('incident_date', 'Unknown')}", styles['Normal']),
            Paragraph(f"Location: {complaint.get('location', 'Unknown')}", styles['Normal']),
            Paragraph(f"Type: {complaint.get('complaint_reason', 'Unknown')}", styles['Normal']),
            Spacer(1, 12),
            Paragraph("Description:", styles['Heading2']),
            Paragraph(complaint.get('description', 'No description provided'), styles['Normal']),
        ]

        # Add watermark
        try:
            from backend.utils.security import PDFUtils
        except ImportError:
            from utils.security import PDFUtils
        PDFUtils.add_watermark(doc, "OFFICIAL DOCUMENT - CYBER CRIME REPORTING SYSTEM")

        doc.build(content)
        buffer.seek(0)

        return {
            "pdf_data": buffer.getvalue(),
            "filename": f"complaint_{tracking_id}.pdf"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate PDF")

# Background tasks
async def process_complaint_ai(tracking_id: str, description: str):
    """Process complaint with AI for categorization and summarization."""
    try:
        # AI categorization
        category = ai_service.categorize_complaint(description)

        # AI summarization
        summary = ai_service.summarize_complaint(description)

        # Update complaint in database
        update_data = {}
        if category:
            update_data['ai_category'] = category
        if summary:
            update_data['ai_summary'] = summary

        if update_data:
            db_service.update_complaint_by_tracking_id(tracking_id, update_data)

        logger.info(f"AI processing completed for {tracking_id}")

    except Exception as e:
        logger.error(f"AI processing failed for {tracking_id}: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
