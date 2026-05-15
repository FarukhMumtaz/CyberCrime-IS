"""
Cyber Crime Reporting System - Database Models

Pydantic models for data validation and serialization.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
import re

# CNIC validation pattern
CNIC_PATTERN = re.compile(r'^\d{13}$')

class User(BaseModel):
    """User model for registered users."""
    id: Optional[str] = None
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    hashed_password: Optional[str] = None
    full_name: Optional[str] = None
    phone: Optional[str] = Field(None, pattern=r'^(\+92|0)?[3][0-4][0-9]{8}$')
    cnic: Optional[str] = Field(None, pattern=r'^\d{13}$')
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @validator('cnic')
    def validate_cnic(cls, v):
        if v and not CNIC_PATTERN.match(v):
            raise ValueError('CNIC must be 13 digits')
        return v

class UserCreate(BaseModel):
    """Model for user registration."""
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None
    phone: Optional[str] = Field(None, pattern=r'^(\+92|0)?[3][0-4][0-9]{8}$')
    cnic: Optional[str] = Field(None, pattern=r'^\d{13}$')

class UserLogin(BaseModel):
    """Model for user login."""
    email: str
    password: str

class Complaint(BaseModel):
    """Complaint model."""
    id: Optional[str] = None
    tracking_id: Optional[str] = None
    user_id: Optional[str] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    cnic: Optional[str] = None  # Encrypted
    address: Optional[str] = None
    incident_date: str
    location: str
    complaint_reason: str
    description: str
    status: str = "submitted"
    ai_summary: Optional[str] = None
    ai_category: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @validator('incident_date')
    def validate_date(cls, v):
        try:
            datetime.fromisoformat(v)
            return v
        except:
            raise ValueError('Invalid date format')

class ComplaintCreate(BaseModel):
    """Model for creating complaints."""
    full_name: Optional[str] = None
    phone: Optional[str] = None
    cnic: Optional[str] = Field(None, pattern=r'^\d{13}$')
    address: Optional[str] = None
    incident_date: str
    location: str
    complaint_reason: str
    description: str

class Evidence(BaseModel):
    """Evidence model."""
    id: Optional[str] = None
    complaint_id: str
    file_name: str
    original_name: str
    file_path: str
    file_type: str  # video, image, pdf
    mime_type: str
    file_size: int
    sha256_hash: str
    is_encrypted: bool = True
    malware_scan_status: str = "pending"
    metadata: Optional[Dict[str, Any]] = None
    uploaded_at: Optional[datetime] = None

class Law(BaseModel):
    """Cyber law model."""
    id: Optional[str] = None
    category: str
    section: str
    title: str
    description: str
    punishment: str
    relevant_pepa_sections: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class AuditLog(BaseModel):
    """Audit log model."""
    id: Optional[str] = None
    user_id: Optional[str] = None
    action: str
    resource_type: str
    resource_id: str
    details: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    created_at: Optional[datetime] = None

class TokenData(BaseModel):
    """JWT token data."""
    user_id: str
    exp: int

class FileValidation(BaseModel):
    """File validation result."""
    size: int
    mime_type: str
    sha256_hash: str

class EvidenceUpload(BaseModel):
    """Evidence upload response."""
    file_name: str
    status: str
    size: int
    error: Optional[str] = None

class APIResponse(BaseModel):
    """Generic API response."""
    success: bool
    message: str
    data: Optional[Any] = None

class ComplaintResponse(BaseModel):
    """Complaint creation response."""
    tracking_id: str
    message: str
    status: str

class PDFResponse(BaseModel):
    """PDF generation response."""
    pdf_data: bytes
    filename: str
