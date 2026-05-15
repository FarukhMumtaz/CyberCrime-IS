"""
Cyber Crime Reporting System - Utility Functions

Security utilities, encryption, validation, and helpers.
"""

import os
import re
import hashlib
import secrets
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import jwt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import logging

logger = logging.getLogger(__name__)

# Security constants
JWT_SECRET = os.getenv("JWT_SECRET_KEY")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

# CNIC validation pattern (13 digits)
CNIC_PATTERN = re.compile(r'^\d{13}$')

# Phone validation pattern (Pakistani mobile numbers)
PHONE_PATTERN = re.compile(r'^(\+92|0)?[3][0-4][0-9]{8}$')

# Email validation pattern
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

class SecurityUtils:
    """Security utility functions."""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using PBKDF2."""
        salt = os.urandom(32)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return f"{base64.urlsafe_b64encode(salt).decode()}:{key.decode()}"

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify password against hash."""
        try:
            salt_b64, key_b64 = hashed.split(':')
            salt = base64.urlsafe_b64decode(salt_b64)
            key = base64.urlsafe_b64decode(key_b64)

            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            derived_key = kdf.derive(password.encode())
            return secrets.compare_digest(key, base64.urlsafe_b64encode(derived_key))
        except Exception:
            return False

    @staticmethod
    def generate_jwt_token(user_id: str) -> str:
        """Generate JWT token for user."""
        expire = datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
        to_encode = {"sub": user_id, "exp": expire}
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_jwt_token(token: str) -> Optional[str]:
        """Verify JWT token and return user ID."""
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            user_id = payload.get("sub")
            return user_id
        except jwt.ExpiredSignatureError:
            logger.warning("JWT token expired")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Invalid JWT token")
            return None

    @staticmethod
    def encrypt_sensitive_data(data: str) -> str:
        """Encrypt sensitive data like CNIC."""
        if not ENCRYPTION_KEY:
            logger.warning("Encryption key not set, returning plain data")
            return data

        fernet = Fernet(ENCRYPTION_KEY.encode())
        return fernet.encrypt(data.encode()).decode()

    @staticmethod
    def decrypt_sensitive_data(encrypted_data: str) -> str:
        """Decrypt sensitive data."""
        if not ENCRYPTION_KEY:
            logger.warning("Encryption key not set, returning data as-is")
            return encrypted_data

        try:
            fernet = Fernet(ENCRYPTION_KEY.encode())
            return fernet.decrypt(encrypted_data.encode()).decode()
        except Exception as e:
            logger.error(f"Decryption failed: {str(e)}")
            return encrypted_data

    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        """Generate a secure random token."""
        return secrets.token_urlsafe(length)

    @staticmethod
    def calculate_file_hash(file_path: str) -> str:
        """Calculate SHA-256 hash of file."""
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()

class ValidationUtils:
    """Data validation utilities."""

    @staticmethod
    def validate_cnic(cnic: str) -> bool:
        """Validate Pakistani CNIC format (13 digits)."""
        if not cnic:
            return True  # Optional field
        return bool(CNIC_PATTERN.match(cnic))

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate Pakistani phone number."""
        if not phone:
            return True  # Optional field
        return bool(PHONE_PATTERN.match(phone))

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        if not email:
            return True  # Optional field
        return bool(EMAIL_PATTERN.match(email))

    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitize user input to prevent XSS."""
        # Basic sanitization - in production, use bleach or similar
        import html
        return html.escape(text.strip())

    @staticmethod
    def validate_file_type(filename: str, allowed_extensions: list) -> bool:
        """Validate file extension."""
        if not filename:
            return False
        ext = filename.lower().split('.')[-1]
        return ext in allowed_extensions

    @staticmethod
    def validate_file_size(size: int, max_size: int) -> bool:
        """Validate file size."""
        return size <= max_size

class TrackingUtils:
    """Tracking ID generation and management."""

    @staticmethod
    def generate_tracking_id() -> str:
        """Generate unique tracking ID with format CCRS-PK-YYYY-XXXXXX."""
        year = datetime.now().year
        random_part = secrets.token_hex(3).upper()  # 6 characters
        return f"CCRS-PK-{year}-{random_part}"

    @staticmethod
    def validate_tracking_id(tracking_id: str) -> bool:
        """Validate tracking ID format."""
        pattern = r'^CCRS-PK-\d{4}-[A-F0-9]{6}$'
        return bool(re.match(pattern, tracking_id))

class AuditUtils:
    """Audit logging utilities."""

    @staticmethod
    def log_user_action(
        user_id: Optional[str],
        action: str,
        resource_type: str,
        resource_id: str,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ):
        """Log user action for audit purposes."""
        try:
            from backend.services import db_service
        except ImportError:
            from services import db_service

        log_entry = {
            "user_id": user_id,
            "action": action,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "details": details or {},
            "ip_address": ip_address,
            "user_agent": user_agent,
            "created_at": datetime.utcnow().isoformat()
        }

        success = db_service.create_audit_log(log_entry)
        if not success:
            logger.warning(f"Failed to create audit log: {log_entry}")

        logger.info(f"Audit log: {log_entry}")

class RateLimitUtils:
    """Rate limiting utilities."""

    # Simple in-memory rate limiting (use Redis in production)
    _rate_limits = {}

    @staticmethod
    def check_rate_limit(identifier: str, max_requests: int = 100, window_minutes: int = 15) -> bool:
        """Check if request is within rate limit."""
        now = datetime.utcnow()
        window_start = now - timedelta(minutes=window_minutes)

        if identifier not in RateLimitUtils._rate_limits:
            RateLimitUtils._rate_limits[identifier] = []

        # Clean old requests
        RateLimitUtils._rate_limits[identifier] = [
            req_time for req_time in RateLimitUtils._rate_limits[identifier]
            if req_time > window_start
        ]

        # Check limit
        if len(RateLimitUtils._rate_limits[identifier]) >= max_requests:
            return False

        # Add current request
        RateLimitUtils._rate_limits[identifier].append(now)
        return True

class PDFUtils:
    """PDF generation utilities."""

    @staticmethod
    def add_watermark(canvas, text: str = "OFFICIAL DOCUMENT - CYBER CRIME REPORTING SYSTEM"):
        """Add watermark to PDF page."""
        canvas.saveState()
        canvas.setFont("Helvetica", 50)
        canvas.setFillColorRGB(0.9, 0.9, 0.9)  # Light gray
        canvas.rotate(45)
        canvas.drawCentredString(400, 400, text)
        canvas.restoreState()

class AIUtils:
    """AI processing utilities."""

    @staticmethod
    def sanitize_ai_prompt(prompt: str) -> str:
        """Sanitize AI prompts to prevent injection."""
        # Remove potentially harmful content
        sanitized = re.sub(r'[<>]', '', prompt)
        return sanitized[:1000]  # Limit length

    @staticmethod
    def validate_ai_response(response: str) -> bool:
        """Validate AI response for safety."""
        # Check for harmful content
        harmful_patterns = [
            r'hack', r'exploit', r'malware', r'virus',
            r'illegal', r'criminal', r'terror'
        ]
        for pattern in harmful_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                return False
        return True
