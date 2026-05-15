"""
Cyber Crime Reporting System - Services

Service layer for business logic.
"""

try:
    from .database_service import db_service, DatabaseService
except ImportError as e:
    print(f"Warning: Could not import database_service: {e}")
    db_service = None
    DatabaseService = None

try:
    from .ai_service import ai_service, AIService
except ImportError as e:
    print(f"Warning: Could not import ai_service: {e}")
    ai_service = None
    AIService = None

try:
    from .file_service import file_service, FileService
except ImportError as e:
    print(f"Warning: Could not import file_service: {e}")
    file_service = None
    FileService = None

__all__ = [
    'db_service', 'DatabaseService',
    'ai_service', 'AIService',
    'file_service', 'FileService'
]