"""
Cyber Crime Reporting System - File Service

Handles file uploads, validation, encryption, and storage.
"""

import os
import hashlib
import magic
from typing import Optional, Dict, Any, List
from cryptography.fernet import Fernet
import logging
from pathlib import Path
import uuid

logger = logging.getLogger(__name__)

class FileService:
    """Service for file operations."""

    def __init__(self):
        self.encryption_key = os.getenv("ENCRYPTION_KEY")
        self.fernet = Fernet(self.encryption_key.encode()) if self.encryption_key else None

        # File size limits
        self.max_sizes = {
            'video': int(os.getenv("MAX_VIDEO_SIZE_MB", 1024)) * 1024 * 1024,
            'image': int(os.getenv("MAX_IMAGE_SIZE_MB", 50)) * 1024 * 1024,
            'pdf': int(os.getenv("MAX_PDF_SIZE_MB", 10)) * 1024 * 1024
        }

        # Allowed MIME types
        self.allowed_types = {
            'video': ['video/mp4', 'video/quicktime', 'video/x-msvideo'],
            'image': ['image/jpeg', 'image/png'],
            'pdf': ['application/pdf']
        }

    def validate_file(self, file_content: bytes, filename: str) -> Optional[Dict[str, Any]]:
        """Validate uploaded file."""
        try:
            # Check file size
            size = len(file_content)
            file_type = self._get_file_type(filename)

            if file_type not in self.max_sizes:
                return None

            if size > self.max_sizes[file_type]:
                return None

            # Check MIME type
            mime = magic.Magic(mime=True)
            detected_mime = mime.from_buffer(file_content)

            if detected_mime not in self.allowed_types[file_type]:
                return None

            # Calculate hash
            sha256 = hashlib.sha256()
            sha256.update(file_content)
            file_hash = sha256.hexdigest()

            return {
                "size": size,
                "mime_type": detected_mime,
                "sha256_hash": file_hash,
                "file_type": file_type
            }

        except Exception as e:
            logger.error(f"File validation error: {e}")
            return None

    def _get_file_type(self, filename: str) -> Optional[str]:
        """Determine file type from filename."""
        ext = filename.lower().split('.')[-1]
        if ext in ['mp4', 'mov', 'avi']:
            return 'video'
        elif ext in ['jpg', 'jpeg', 'png']:
            return 'image'
        elif ext == 'pdf':
            return 'pdf'
        return None

    def encrypt_file(self, file_content: bytes) -> bytes:
        """Encrypt file content."""
        if self.fernet:
            return self.fernet.encrypt(file_content)
        return file_content

    def decrypt_file(self, encrypted_content: bytes) -> bytes:
        """Decrypt file content."""
        if self.fernet:
            return self.fernet.decrypt(encrypted_content)
        return encrypted_content

    def generate_secure_filename(self, original_filename: str) -> str:
        """Generate secure filename."""
        ext = original_filename.split('.')[-1]
        return f"{uuid.uuid4()}.{ext}"

    def scan_for_malware(self, file_content: bytes) -> str:
        """Scan file for malware (placeholder - integrate with ClamAV)."""
        # TODO: Integrate with ClamAV
        # For now, return 'clean' for all files
        return "clean"

# Global instance
file_service = FileService()