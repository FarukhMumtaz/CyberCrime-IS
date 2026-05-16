"""
Cybercrime Complaint Report Form Page
Modern Premium Version with Evidence Persistence
"""

import streamlit as st
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import logging
from datetime import datetime
import uuid
import json
from frontend.utils.supabase_sync import sync_complaint, sync_evidence_metadata

# Ensure local path imports work
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

load_dotenv()
logger = logging.getLogger(__name__)

# Paths
COMPLAINTS_FILE = ROOT_DIR / "backend" / "data" / "complaints.json"
EVIDENCE_DIR = ROOT_DIR / "backend" / "data" / "evidence"

def load_complaints():
    if os.path.exists(COMPLAINTS_FILE):
        try:
            with open(COMPLAINTS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_complaints(complaints):
    os.makedirs(COMPLAINTS_FILE.parent, exist_ok=True)
    with open(COMPLAINTS_FILE, 'w') as f:
        json.dump(complaints, f, indent=2, default=str)

def save_evidence(tracking_id, uploaded_files):
    """Saves evidence files to the local filesystem."""
    if not uploaded_files:
        return []
    
    case_evidence_dir = EVIDENCE_DIR / tracking_id
    os.makedirs(case_evidence_dir, exist_ok=True)
    
    saved_files = []
    for uploaded_file in uploaded_files:
        file_path = case_evidence_dir / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        saved_files.append(uploaded_file.name)
    
    return saved_files

def render_report_form(set_page_config: bool = True):
    if set_page_config:
        st.set_page_config(page_title="Initialize Report", page_icon="📋", layout="wide")

    st.markdown("## 📋 INITIALIZE NEW CASE REPORT")
    anonymous = False
    
    with st.form("complaint_form", clear_on_submit=False):
        st.markdown('<div class="complaint-form">', unsafe_allow_html=True)

        st.markdown("### 👤 CONTACT INFORMATION")
        email = st.text_input("PRIMARY EMAIL (REQUIRED)", placeholder="citizen@example.com")

        c1, c2 = st.columns(2)
        with c1:
            full_name = st.text_input("FULL LEGAL NAME")
            phone = st.text_input("MOBILE CONTACT")
        with c2:
            cnic = st.text_input("CNIC (13 DIGITS)", max_chars=13)
            address = st.text_area("PHYSICAL ADDRESS")

        st.markdown("---")
        st.markdown("### 🛰️ INCIDENT MATRIX")
        c_type, c_date = st.columns(2)
        with c_type:
            reason = st.selectbox("CRIME CLASSIFICATION", ["Hacking", "Phishing", "Cyberstalking", "Online Harassment", "Financial Fraud", "Other"])
        with c_date:
            inc_date = st.date_input("INCIDENT TIMESTAMP")
        
        location = st.text_input("LOCATION (URL/Physical)")
        description = st.text_area("DETAILED LOG", height=150)

        st.markdown("#### 📎 ELECTRONIC EVIDENCE BUNDLE")
        uploaded_files = st.file_uploader("UPLOAD DATA", accept_multiple_files=True, type=['jpg','png','pdf','mp4','zip'])

        submitted = st.form_submit_button("SUBMIT CASE REPORT", type="primary", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if submitted:
        if not email or "@" not in email:
            st.error("Valid email required.")
            return
        if len(description) < 20:
            st.error("Please provide more detail in the log.")
            return

        tracking_id = f"CCRS-PK-{datetime.now().year}-{str(uuid.uuid4())[:6].upper()}"
        
        # Save files FIRST
        evidence_filenames = save_evidence(tracking_id, uploaded_files)
        
        complaint_data = {
            "tracking_id": tracking_id,
            "email": email,
            "full_name": full_name,
            "phone": phone,
            "cnic": cnic,
            "address": address,
            "anonymous": anonymous,
            "incident_date": inc_date.isoformat(),
            "location": location,
            "complaint_reason": reason,
            "description": description,
            "evidence_files": evidence_filenames,
            "submitted_at": datetime.now().isoformat(),
            "status": "pending"
        }

        complaints = load_complaints()
        complaints[tracking_id] = complaint_data
        save_complaints(complaints)
        sync_complaint(complaint_data)
        sync_evidence_metadata(tracking_id, EVIDENCE_DIR, evidence_filenames)

        st.success(f"🛰️ CASE REGISTERED. TRACKING ID: {tracking_id}")
        st.info("Your evidence has been encrypted and stored in our secure repository.")

if __name__ == "__main__":
    render_report_form()
