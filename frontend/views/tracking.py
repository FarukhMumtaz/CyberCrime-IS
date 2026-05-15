"""
Cyber Crime Reporting System - Tracking Page
Modern Premium Version
"""

import streamlit as st
import json
import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Database files
COMPLAINTS_FILE = ROOT_DIR / "backend" / "data" / "complaints.json"
DECISIONS_FILE = ROOT_DIR / "backend" / "data" / "officer_decisions.json"

def load_json(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def render_tracking_page(set_page_config: bool = True):
    if set_page_config:
        st.set_page_config(page_title="Track Case - Cyber System", page_icon="📍", layout="wide")
    
    st.markdown("## 📍 CASE TRACKING MODULE")
    st.write("Access real-time operational status of your registered complaint.")

    # Search Unit
    col_input, col_btn = st.columns([3, 1])
    with col_input:
        tracking_id = st.text_input(
            "ENTER TRACKING ID",
            placeholder="CCRS-PK-2026-XXXXXXXX"
        )
    with col_btn:
        st.write("")
        st.write("")
        search_btn = st.button("EXECUTE SEARCH", type="primary", use_container_width=True)

    if search_btn and tracking_id:
        complaints = load_json(COMPLAINTS_FILE)
        decisions = load_json(DECISIONS_FILE)
        
        if tracking_id in complaints:
            c = complaints[tracking_id]
            d = decisions.get(tracking_id)
            
            st.markdown("---")
            st.markdown(f"### ✅ CASE NODE FOUND: {tracking_id}")
            
            # Tracking Card
            st.markdown('<div class="tracking-card cyber-glow">', unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                st.write(f"**Classification:** {c.get('complaint_reason')}")
                st.write(f"**Incident Date:** {c.get('incident_date')}")
                st.write(f"**Location:** {c.get('location')}")
            with c2:
                if c.get('anonymous'):
                    st.write("**Complainant:** ANONYMOUS")
                else:
                    st.write(f"**Complainant:** {c.get('full_name')}")
                st.write(f"**Submission Date:** {c.get('submitted_at')}")

            st.markdown("---")
            
            # Status Matrix
            st.subheader("📊 OPERATIONAL STATUS")
            
            if d:
                decision_text = d.get("decision", "").upper()
                notes = d.get("notes", "N/A")
                
                if "SOLVE" in decision_text:
                    st.markdown('<div class="solved-badge">CASE RESOLVED</div>', unsafe_allow_html=True)
                elif "APPROVE" in decision_text:
                    st.markdown('<div class="approved-badge">UNDER INVESTIGATION</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="rejected-badge">REJECTED / INSUFFICIENT DATA</div>', unsafe_allow_html=True)
                
                st.markdown(f"**Officer Remarks:** *\"{notes}\"*")
                st.markdown(f"**Operational Date:** {d.get('decided_at')}")
            else:
                st.markdown('<div class="pending-badge">PENDING REVIEW</div>', unsafe_allow_html=True)
                st.info("The complaint is currently in the review queue. Analysts will initialize investigation shortly.")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        else:
            st.error(f"❌ CASE ID '{tracking_id}' NOT FOUND IN CENTRAL DATABASE.")
    
    elif search_btn:
        st.warning("PLEASE PROVIDE A VALID TRACKING ID.")

if __name__ == "__main__":
    render_tracking_page()