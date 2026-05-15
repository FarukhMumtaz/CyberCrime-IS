"""
Cyber Crime Reporting System - Database Service

Handles all database operations with Supabase.
"""

import os
from typing import Optional, List, Dict, Any
from supabase import create_client, Client
from datetime import datetime
import logging

try:
    from backend.models import User, Complaint, Evidence, Law, AuditLog
except ImportError:
    try:
        from models import User, Complaint, Evidence, Law, AuditLog
    except ImportError:
        # Models import may fail during service initialization
        pass

logger = logging.getLogger(__name__)

class DatabaseService:
    """Service for database operations."""

    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = (
            os.getenv("SUPABASE_SERVICE_ROLE_KEY")
            or os.getenv("SUPABASE_ANON_KEY")
            or os.getenv("SUPABASE_KEY")
        )

        if not self.supabase_url or not self.supabase_key:
            logger.warning("Supabase credentials not configured")
            self.client = None
        else:
            try:
                self.client: Client = create_client(self.supabase_url, self.supabase_key)
                logger.info("Supabase client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Supabase client: {e}")
                self.client = None

    def create_user(self, user_data: Dict[str, Any]) -> Optional[str]:
        """Create a new user."""
        if not self.client:
            return None

        try:
            response = self.client.table('users').insert(user_data).execute()
            return response.data[0]['id'] if response.data else None
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return None

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email."""
        if not self.client:
            return None

        try:
            response = self.client.table('users').select('*').eq('email', email).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error getting user: {e}")
            return None

    def create_complaint(self, complaint_data: Dict[str, Any]) -> Optional[str]:
        """Create a new complaint."""
        if not self.client:
            return None

        try:
            response = self.client.table('complaints').insert(complaint_data).execute()
            return response.data[0]['id'] if response.data else None
        except Exception as e:
            logger.error(f"Error creating complaint: {e}")
            return None

    def get_complaint(self, tracking_id: str, user_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get complaint by tracking ID."""
        if not self.client:
            return None

        try:
            query = self.client.table('complaints').select('*').eq('tracking_id', tracking_id)
            if user_id:
                query = query.or_(f'user_id.is.null,user_id.eq.{user_id}')
            response = query.execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error getting complaint: {e}")
            return None

    def update_complaint_by_tracking_id(self, tracking_id: str, update_data: Dict[str, Any]) -> bool:
        """Update complaint by tracking ID."""
        if not self.client:
            return False

        try:
            update_data['updated_at'] = datetime.utcnow().isoformat()
            self.client.table('complaints').update(update_data).eq('tracking_id', tracking_id).execute()
            return True
        except Exception as e:
            logger.error(f"Error updating complaint: {e}")
            return False

    def create_evidence(self, evidence_data: Dict[str, Any]) -> Optional[str]:
        """Create evidence record."""
        if not self.client:
            return None

        try:
            response = self.client.table('evidence').insert(evidence_data).execute()
            return response.data[0]['id'] if response.data else None
        except Exception as e:
            logger.error(f"Error creating evidence: {e}")
            return None

    def get_laws(self, category: Optional[str] = None, search: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get cyber laws with optional filtering."""
        if not self.client:
            return []

        try:
            query = self.client.table('laws').select('*')

            if category:
                query = query.eq('category', category)

            if search:
                query = query.or_(f'title.ilike.%{search}%,description.ilike.%{search}%')

            response = query.execute()
            return response.data or []
        except Exception as e:
            logger.error(f"Error getting laws: {e}")
            return []

    def create_audit_log(self, audit_data: Dict[str, Any]) -> bool:
        """Create audit log entry."""
        if not self.client:
            return False

        try:
            self.client.table('audit_logs').insert(audit_data).execute()
            return True
        except Exception as e:
            logger.error(f"Error creating audit log: {e}")
            return False

# Global instance
db_service = DatabaseService()
