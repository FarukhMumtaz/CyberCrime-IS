"""
Officer Panel - Case Management Dashboard
Includes AI Automation and Evidence Review.
"""

import streamlit as st
import json
import os
import sys
import requests
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.utils.email_service import send_case_update_email
from frontend.utils.supabase_sync import (
    download_supabase_evidence,
    fetch_supabase_complaints,
    fetch_supabase_evidence,
    fetch_supabase_officer_decisions,
    sync_complaint,
    sync_officer_decision,
)

# Database files
COMPLAINTS_FILE = ROOT_DIR / "backend" / "data" / "complaints.json"
OFFICER_DECISIONS_FILE = ROOT_DIR / "backend" / "data" / "officer_decisions.json"
EVIDENCE_BASE_DIR = ROOT_DIR / "backend" / "data" / "evidence"

def load_json(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_json(file_path, data):
    os.makedirs(file_path.parent, exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2, default=str)

def merge_complaints(local_complaints, supabase_complaints):
    merged = dict(supabase_complaints)
    for tid, local_complaint in local_complaints.items():
        if tid not in merged:
            merged[tid] = local_complaint
            continue

        combined = {**local_complaint, **merged[tid]}
        for field in ("email", "evidence_files"):
            if not combined.get(field) and local_complaint.get(field):
                combined[field] = local_complaint.get(field)
        merged[tid] = combined
    return merged

def load_shared_complaints():
    return merge_complaints(load_json(COMPLAINTS_FILE), fetch_supabase_complaints())

def load_shared_decisions():
    decisions = load_json(OFFICER_DECISIONS_FILE)
    for tid, decision in fetch_supabase_officer_decisions().items():
        decisions[tid] = {**decisions.get(tid, {}), **decision}
    return decisions

def get_actual_evidence_files(tracking_id):
    case_dir = EVIDENCE_BASE_DIR / tracking_id
    if case_dir.exists() and case_dir.is_dir():
        return [f for f in os.listdir(case_dir) if os.path.isfile(case_dir / f)]
    return []

def get_evidence_items(tracking_id):
    items = []
    seen_names = set()

    for filename in get_actual_evidence_files(tracking_id):
        path = EVIDENCE_BASE_DIR / tracking_id / filename
        items.append({"source": "local", "name": filename, "path": path})
        seen_names.add(filename)

    for row in fetch_supabase_evidence(tracking_id):
        name = row.get("original_name") or row.get("file_name")
        if not name or name in seen_names:
            continue
        items.append(
            {
                "source": "supabase",
                "name": name,
                "file_path": row.get("file_path"),
                "mime_type": row.get("mime_type"),
            }
        )
        seen_names.add(name)

    return items

def draft_ai_email(c, decision, officer_notes):
    """Uses AI to draft a detailed, professional email including all case data."""
    try:
        api_key = os.getenv("GROQ_API_KEY")
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        
        prompt = f"""
        Draft a formal official email from NCIA Pakistan to a citizen.
        
        CASE DATA:
        - Name: {c.get('full_name', 'N/A')}
        - CNIC: {c.get('cnic', 'N/A')}
        - Reason: {c.get('complaint_reason')}
        - Description: {c.get('description')}
        - Decision: {decision}
        - Remarks: {officer_notes}
        
        Include the Tracking ID: {c.get('tracking_id')}
        Tone: Formal, Official, Supportive. Use 'NCIA Operations' as the sender.
        """
        
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "system", "content": "Professional secretary."}, {"role": "user", "content": prompt}],
            "temperature": 0.3
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=12)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
    except:
        return f"Case Update: {decision}\n\nRemarks: {officer_notes}"
    return "Drafting failed."

def render_officer_panel(set_page_config: bool = True):
    if set_page_config:
        try: st.set_page_config(page_title="Officer Dashboard", layout="wide")
        except: pass
    
    if not st.session_state.get('officer_logged_in'):
        st.error("ACCESS DENIED.")
        return
    
    officer_id = st.session_state.get('officer_id')
    st.markdown(f"### 👮 OFFICER DASHBOARD | `{officer_id}`")
    
    complaints = load_shared_complaints()
    decisions = load_shared_decisions()
    
    tab1, tab2, tab3 = st.tabs(["📥 QUEUE", "✅ PROCESSED", "🤖 AI AUTOMATION"])
    
    with tab1:
        pending = [tid for tid in complaints if tid not in decisions]
        if not pending:
            st.info("Queue clear.")
        else:
            for tid in pending:
                c = complaints[tid]
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"""<div class="complaint-card"><span class="status-pill status-pending">PENDING</span>
                        <h4 style="margin:5px 0;">{c.get('complaint_reason')}</h4><p>ID: {tid}</p></div>""", unsafe_allow_html=True)
                    with col2:
                        if st.button("REVIEW", key=f"rev_{tid}"):
                            st.session_state.review_tid = tid
                            st.rerun()

    # Manual Review Section
    if st.session_state.get('review_tid'):
        tid = st.session_state.review_tid
        c = complaints.get(tid)
        if not c:
            st.error("Selected complaint is no longer available.")
            st.session_state.review_tid = None
            return
        st.markdown("---")
        st.subheader(f"🔍 CASE DOSSIER: {tid}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 👤 Citizen Data")
            st.write(f"**Name:** {c.get('full_name')}")
            st.write(f"**CNIC:** {c.get('cnic')}")
            st.write(f"**Address:** {c.get('address')}")
        with col2:
            st.markdown("#### 🛰️ Incident Info")
            st.write(f"**Type:** {c.get('complaint_reason')}")
            st.write(f"**Location:** {c.get('location')}")
            st.write(f"**Date:** {c.get('incident_date')}")

        st.markdown("#### 📄 Description")
        st.info(c.get('description'))

        st.markdown("#### 📁 EVIDENCE REPOSITORY")
        evidence_items = get_evidence_items(tid)
        if not evidence_items:
            st.warning("No physical evidence attached.")
        else:
            cols = st.columns(4)
            for i, item in enumerate(evidence_items):
                fname = item["name"]
                with cols[i % 4]:
                    if item["source"] == "local":
                        fpath = item["path"]
                        with open(fpath, "rb") as f:
                            st.download_button(f"📥 {fname[:10]}...", f, fname, key=f"dl_{tid}_{i}")
                        if fname.lower().endswith(('.png', '.jpg', '.jpeg')):
                            st.image(str(fpath), use_column_width=True)
                    else:
                        file_data = download_supabase_evidence(item.get("file_path"))
                        if file_data:
                            st.download_button(f"📥 {fname[:10]}...", file_data, fname, key=f"dl_{tid}_{i}")
                            if fname.lower().endswith(('.png', '.jpg', '.jpeg')):
                                st.image(file_data, use_column_width=True)
                        else:
                            st.caption(f"{fname} metadata available")

        with st.form("action_form"):
            decision = st.selectbox("Status:", ["Approve", "Solve", "Reject"])
            notes = st.text_area("Remarks:")
            if st.form_submit_button("SUBMIT DECISION", use_container_width=True):
                decisions[tid] = {"officer_id": officer_id, "decision": decision, "notes": notes, "timestamp": datetime.now().isoformat()}
                local_decisions = load_json(OFFICER_DECISIONS_FILE)
                local_decisions[tid] = decisions[tid]
                save_json(OFFICER_DECISIONS_FILE, local_decisions)
                sync_complaint(c)
                sync_officer_decision(tid, decisions[tid])
                st.session_state.review_tid = None
                st.rerun()
            if st.form_submit_button("CLOSE", use_container_width=True):
                st.session_state.review_tid = None
                st.rerun()

    with tab2:
        for tid, d in decisions.items():
            c = complaints.get(tid, {})
            st.markdown(f'<div class="complaint-card"><h4 style="margin:5px 0;">{c.get("complaint_reason")}</h4><p>ID: {tid}</p></div>', unsafe_allow_html=True)

    with tab3:
        st.subheader("🤖 AI AUTOMATION CENTER")
        processed_tids = list(decisions.keys())
        if not processed_tids:
            st.warning("No cases to automate.")
        else:
            sel_tid = st.selectbox("Select Case to Notify:", processed_tids)
            if sel_tid:
                c = complaints.get(sel_tid, {})
                d = decisions.get(sel_tid)
                st.markdown("---")
                db_email = c.get('email', '')
                victim_email = st.text_input("Recipient Email:", value=db_email)
                
                if st.button("🪄 GENERATE AI DRAFT"):
                    with st.spinner("AI Synthesizing..."):
                        draft = draft_ai_email(c, d['decision'], d['notes'])
                        st.session_state.ai_draft = draft
                
                if st.session_state.get('ai_draft'):
                    final = st.text_area("Review AI Draft:", value=st.session_state.ai_draft, height=400)
                    if st.button("📧 DISPATCH EMAIL", type="primary"):
                        if not victim_email: st.error("Email required.")
                        else:
                            with st.spinner("Sending..."):
                                success, err = send_case_update_email(victim_email, sel_tid, d['decision'], final)
                                if success: st.success("Sent."); st.session_state.ai_draft = None
                                else: st.error(f"Failed: {err}")

if __name__ == "__main__":
    render_officer_panel()
