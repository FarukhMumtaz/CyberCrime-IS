"""
Minimal Supabase sync helpers for the Streamlit JSON-backed workflow.

These helpers are intentionally best-effort: local JSON remains the existing
working source, while Supabase is kept organized for Table Editor visibility.
"""

from __future__ import annotations

import hashlib
import logging
import mimetypes
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

from dotenv import load_dotenv
from supabase import create_client

ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")

logger = logging.getLogger(__name__)
_CLIENT = None


def _get_client():
    global _CLIENT
    if _CLIENT is not None:
        return _CLIENT

    url = os.getenv("SUPABASE_URL")
    key = (
        os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        or os.getenv("SUPABASE_ANON_KEY")
        or os.getenv("SUPABASE_KEY")
    )
    if not url or not key:
        return None

    try:
        _CLIENT = create_client(url, key)
        return _CLIENT
    except Exception as exc:
        logger.warning("Supabase sync unavailable: %s", exc)
        return None


def _clean(value: Any) -> Any:
    if value in ("", "N/A", "ANONYMOUS"):
        return None
    return value


def _iso(value: Any) -> Optional[str]:
    if not value:
        return None
    return str(value)


def _file_type(filename: str) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix in {".jpg", ".jpeg", ".png", ".gif", ".webp"}:
        return "image"
    if suffix in {".mp4", ".mov", ".avi", ".mkv"}:
        return "video"
    if suffix == ".pdf":
        return "pdf"
    return suffix.lstrip(".") or "file"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _upload_evidence_file(
    client: Any,
    path: Path,
    complaint_id: str,
    filename: str,
    mime_type: str,
) -> Optional[str]:
    """Upload evidence to Supabase Storage when the configured bucket is available."""
    bucket = os.getenv("SUPABASE_EVIDENCE_BUCKET", "evidence-files")
    storage_path = f"evidence/{complaint_id}/{Path(filename).name}"

    try:
        client.storage.from_(bucket).upload(
            storage_path,
            path.read_bytes(),
            {"content-type": mime_type, "x-upsert": "true"},
        )
        return storage_path
    except Exception as exc:
        if "bucket not found" in str(exc).lower():
            try:
                client.storage.create_bucket(bucket, options={"public": False})
                client.storage.from_(bucket).upload(
                    storage_path,
                    path.read_bytes(),
                    {"content-type": mime_type, "x-upsert": "true"},
                )
                return storage_path
            except Exception as create_exc:
                logger.warning("Supabase evidence bucket setup skipped for %s: %s", bucket, create_exc)
        logger.warning("Supabase evidence file upload skipped for %s: %s", filename, exc)
        return None


def _get_complaint_row(tracking_id: str) -> Optional[Dict[str, Any]]:
    client = _get_client()
    if not client:
        return None

    try:
        response = (
            client.table("complaints")
            .select("*")
            .eq("tracking_id", tracking_id)
            .limit(1)
            .execute()
        )
        return response.data[0] if response.data else None
    except Exception as exc:
        logger.warning("Supabase complaint lookup failed for %s: %s", tracking_id, exc)
        return None


def _complaint_from_row(row: Dict[str, Any]) -> Dict[str, Any]:
    contact_values = [row.get("full_name"), row.get("phone"), row.get("cnic"), row.get("address")]
    return {
        "tracking_id": row.get("tracking_id"),
        "email": None,
        "full_name": row.get("full_name") or "ANONYMOUS",
        "phone": row.get("phone") or "N/A",
        "cnic": row.get("cnic") or "N/A",
        "address": row.get("address") or "N/A",
        "anonymous": not any(contact_values),
        "incident_date": _iso(row.get("incident_date")),
        "location": row.get("location") or "",
        "complaint_reason": row.get("complaint_reason"),
        "description": row.get("description"),
        "evidence_files": [],
        "submitted_at": _iso(row.get("created_at")),
        "updated_at": _iso(row.get("updated_at")),
        "status": row.get("status") or "pending",
        "ai_summary": row.get("ai_summary"),
        "ai_category": row.get("ai_category"),
        "supabase_id": row.get("id"),
    }


def _submission_details_by_tracking() -> Dict[str, Dict[str, Any]]:
    client = _get_client()
    if not client:
        return {}

    try:
        response = (
            client.table("audit_logs")
            .select("details,created_at")
            .eq("action", "complaint_submitted")
            .order("created_at")
            .limit(1000)
            .execute()
        )
    except Exception as exc:
        logger.warning("Supabase complaint audit lookup failed: %s", exc)
        return {}

    details_by_tracking: Dict[str, Dict[str, Any]] = {}
    for audit_row in response.data or []:
        details = audit_row.get("details") or {}
        tracking_id = details.get("tracking_id")
        if not tracking_id:
            continue
        details_by_tracking[tracking_id] = details
    return details_by_tracking


def fetch_supabase_complaints() -> Dict[str, Dict[str, Any]]:
    """Fetch complaints from Supabase for shared citizen/officer portal state."""
    client = _get_client()
    if not client:
        return {}

    try:
        response = client.table("complaints").select("*").order("created_at").execute()
    except Exception as exc:
        logger.warning("Supabase complaint list failed: %s", exc)
        return {}

    submission_details = _submission_details_by_tracking()
    complaints: Dict[str, Dict[str, Any]] = {}
    for row in response.data or []:
        complaint = _complaint_from_row(row)
        tracking_id = complaint.get("tracking_id")
        if not tracking_id:
            continue
        details = submission_details.get(tracking_id, {})
        if details.get("email"):
            complaint["email"] = details.get("email")
        if "anonymous" in details:
            complaint["anonymous"] = details.get("anonymous")
        complaints[tracking_id] = complaint
    return complaints


def fetch_supabase_complaint(tracking_id: str) -> Optional[Dict[str, Any]]:
    """Fetch one complaint from Supabase by tracking ID."""
    row = _get_complaint_row(tracking_id)
    if not row:
        return None

    complaint = _complaint_from_row(row)
    details = _submission_details_by_tracking().get(tracking_id, {})
    if details.get("email"):
        complaint["email"] = details.get("email")
    if "anonymous" in details:
        complaint["anonymous"] = details.get("anonymous")
    return complaint


def fetch_supabase_officer_decisions() -> Dict[str, Dict[str, Any]]:
    """Fetch officer decisions from Supabase audit logs."""
    client = _get_client()
    if not client:
        return {}

    try:
        response = (
            client.table("audit_logs")
            .select("details,created_at")
            .eq("action", "officer_decision")
            .order("created_at")
            .limit(1000)
            .execute()
        )
    except Exception as exc:
        logger.warning("Supabase officer decision lookup failed: %s", exc)
        return {}

    decisions: Dict[str, Dict[str, Any]] = {}
    for audit_row in response.data or []:
        details = audit_row.get("details") or {}
        tracking_id = details.get("tracking_id")
        if not tracking_id:
            continue
        decisions[tracking_id] = {
            "officer_id": details.get("officer_id"),
            "decision": details.get("decision"),
            "notes": details.get("notes"),
            "timestamp": details.get("timestamp") or audit_row.get("created_at"),
            "status": details.get("status"),
        }
    return decisions


def fetch_supabase_evidence(tracking_id: str) -> list[Dict[str, Any]]:
    """Fetch evidence metadata for a complaint from Supabase."""
    client = _get_client()
    complaint = _get_complaint_row(tracking_id)
    complaint_id = complaint.get("id") if complaint else None
    if not client or not complaint_id:
        return []

    try:
        response = (
            client.table("evidence")
            .select("*")
            .eq("complaint_id", complaint_id)
            .order("uploaded_at")
            .execute()
        )
        return response.data or []
    except Exception as exc:
        logger.warning("Supabase evidence lookup failed for %s: %s", tracking_id, exc)
        return []


def download_supabase_evidence(file_path: str) -> Optional[bytes]:
    """Download an evidence file from Supabase Storage if it is stored there."""
    client = _get_client()
    if not client or not file_path or not file_path.startswith("evidence/"):
        return None

    bucket = os.getenv("SUPABASE_EVIDENCE_BUCKET", "evidence-files")
    try:
        return client.storage.from_(bucket).download(file_path)
    except Exception as exc:
        logger.warning("Supabase evidence download failed for %s: %s", file_path, exc)
        return None


def sync_complaint(complaint_data: Dict[str, Any]) -> Optional[str]:
    """Create or update the Supabase complaint row for a local complaint."""
    client = _get_client()
    tracking_id = complaint_data.get("tracking_id")
    if not client or not tracking_id:
        return None

    created_at = _iso(complaint_data.get("submitted_at")) or datetime.utcnow().isoformat()
    row = {
        "tracking_id": tracking_id,
        "user_id": None,
        "full_name": _clean(complaint_data.get("full_name")),
        "phone": _clean(complaint_data.get("phone")),
        "cnic": _clean(complaint_data.get("cnic")),
        "address": _clean(complaint_data.get("address")),
        "incident_date": _iso(complaint_data.get("incident_date")),
        "location": _clean(complaint_data.get("location")),
        "complaint_reason": complaint_data.get("complaint_reason"),
        "description": complaint_data.get("description"),
        "status": complaint_data.get("status") or "pending",
        "ai_summary": complaint_data.get("ai_summary"),
        "ai_category": complaint_data.get("ai_category"),
        "created_at": created_at,
        "updated_at": datetime.utcnow().isoformat(),
    }

    try:
        existing = _get_complaint_row(tracking_id)
        created = existing is None
        if existing:
            response = (
                client.table("complaints")
                .update(row)
                .eq("tracking_id", tracking_id)
                .execute()
            )
        else:
            response = client.table("complaints").insert(row).execute()

        saved = response.data[0] if response.data else existing
        complaint_id = saved.get("id") if saved else None
        if complaint_id and created:
            _create_audit_log(
                "complaint_submitted",
                "complaint",
                complaint_id,
                {
                    "tracking_id": tracking_id,
                    "email": complaint_data.get("email"),
                    "anonymous": complaint_data.get("anonymous"),
                },
            )
        return complaint_id
    except Exception as exc:
        logger.warning("Supabase complaint sync failed for %s: %s", tracking_id, exc)
        return None


def sync_evidence_metadata(
    tracking_id: str,
    evidence_dir: Path,
    filenames: Iterable[str],
) -> None:
    """Sync local evidence file metadata to Supabase evidence rows."""
    client = _get_client()
    if not client or not tracking_id:
        return

    complaint = _get_complaint_row(tracking_id)
    complaint_id = complaint.get("id") if complaint else None
    if not complaint_id:
        return

    for filename in filenames or []:
        path = evidence_dir / tracking_id / filename
        if not path.exists() or not path.is_file():
            continue

        mime_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        try:
            existing = (
                client.table("evidence")
                .select("id")
                .eq("complaint_id", complaint_id)
                .eq("original_name", filename)
                .limit(1)
                .execute()
            )
            if existing.data:
                continue

            storage_path = _upload_evidence_file(client, path, complaint_id, filename, mime_type)
            file_path = storage_path or f"local-evidence/{tracking_id}/{filename}"
            evidence_data = {
                "complaint_id": complaint_id,
                "file_name": filename,
                "original_name": filename,
                "file_path": file_path,
                "file_type": _file_type(filename),
                "mime_type": mime_type,
                "file_size": path.stat().st_size,
                "sha256_hash": _sha256(path),
                "is_encrypted": False,
                "malware_scan_status": "not_scanned",
                "metadata": {
                    "tracking_id": tracking_id,
                    "source": "streamlit_storage_upload" if storage_path else "streamlit_local_upload",
                    "storage_bucket": os.getenv("SUPABASE_EVIDENCE_BUCKET", "evidence-files") if storage_path else None,
                },
                "uploaded_at": datetime.utcnow().isoformat(),
            }
            response = client.table("evidence").insert(evidence_data).execute()
            evidence_id = response.data[0].get("id") if response.data else complaint_id
            _create_audit_log(
                "evidence_uploaded",
                "evidence",
                evidence_id,
                {"tracking_id": tracking_id, "file_name": filename},
            )
        except Exception as exc:
            logger.warning("Supabase evidence sync failed for %s: %s", filename, exc)


def sync_officer_decision(
    tracking_id: str,
    decision_data: Dict[str, Any],
) -> None:
    """Sync officer decision/status to Supabase complaint and audit logs."""
    client = _get_client()
    if not client or not tracking_id:
        return

    complaint = _get_complaint_row(tracking_id)
    complaint_id = complaint.get("id") if complaint else None
    if not complaint_id:
        return

    decision = decision_data.get("decision", "")
    decision_lower = decision.lower()
    if "solve" in decision_lower:
        status = "resolved"
    elif "approve" in decision_lower:
        status = "under_review"
    elif "reject" in decision_lower:
        status = "rejected"
    else:
        status = decision_lower or "pending"

    try:
        (
            client.table("complaints")
            .update({"status": status, "updated_at": datetime.utcnow().isoformat()})
            .eq("tracking_id", tracking_id)
            .execute()
        )
        _create_audit_log(
            "officer_decision",
            "complaint",
            complaint_id,
            {
                "tracking_id": tracking_id,
                "officer_id": decision_data.get("officer_id"),
                "decision": decision,
                "notes": decision_data.get("notes"),
                "timestamp": decision_data.get("timestamp") or decision_data.get("decided_at"),
                "status": status,
            },
        )
    except Exception as exc:
        logger.warning("Supabase officer decision sync failed for %s: %s", tracking_id, exc)


def _create_audit_log(
    action: str,
    resource_type: str,
    resource_id: str,
    details: Dict[str, Any],
) -> None:
    client = _get_client()
    if not client or not resource_id:
        return

    try:
        client.table("audit_logs").insert(
            {
                "action": action,
                "resource_type": resource_type,
                "resource_id": resource_id,
                "details": details,
                "created_at": datetime.utcnow().isoformat(),
            }
        ).execute()
    except Exception as exc:
        logger.warning("Supabase audit log sync failed: %s", exc)
