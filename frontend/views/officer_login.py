"""
Officer Login - Secure Authentication Node
Supports Authentication and Official Registration.
"""

import streamlit as st
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

load_dotenv(ROOT_DIR / ".env")

OFFICERS_FILE = ROOT_DIR / "backend" / "data" / "officers.json"

def load_officers():
    if os.path.exists(OFFICERS_FILE):
        try:
            with open(OFFICERS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_officers(officers_data):
    os.makedirs(OFFICERS_FILE.parent, exist_ok=True)
    with open(OFFICERS_FILE, 'w') as f:
        json.dump(officers_data, f, indent=2)

def render_officer_login(set_page_config: bool = True):
    if set_page_config:
        st.set_page_config(page_title="Officer Login", page_icon="🔐", layout="centered")

    st.markdown('<div class="login-form">', unsafe_allow_html=True)
    st.markdown("### 🔐 OFFICER AUTHENTICATION")
    
    # Check if already logged in
    if st.session_state.get('officer_logged_in'):
        st.success(f"Authenticated as: {st.session_state.officer_id}")
        if st.button("PROCEED TO DASHBOARD"):
            st.session_state.current_page = "officer_panel"
            st.rerun()
        return

    officer_id = st.text_input("NODE ID (ID)", placeholder="CYBER2026FARUKH")
    password = st.text_input("SECURE KEY (PASSWORD)", type="password")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("AUTHORIZE", type="primary", use_container_width=True):
            if verify_officer(officer_id, password):
                st.session_state.officer_logged_in = True
                st.session_state.officer_id = officer_id
                st.session_state.current_page = "officer_panel"
                st.success("ACCESS GRANTED.")
                st.rerun()
            else:
                st.error("INVALID CREDENTIALS.")
    
    with col2:
        if st.button("REGISTER", use_container_width=True):
            st.session_state.show_officer_signup = True
            
    with col3:
        if st.button("CANCEL", use_container_width=True):
            st.session_state.current_page = "home"
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.get("show_officer_signup"):
        show_registration_form()

def verify_officer(officer_id, password):
    officers = load_officers()
    if officer_id in officers:
        return officers[officer_id].get("password") == password
    return False

def show_registration_form():
    st.markdown("---")
    st.markdown("### 📝 OFFICER REGISTRATION")
    
    with st.form("officer_signup_form"):
        name = st.text_input("FULL NAME")
        email = st.text_input("OFFICIAL EMAIL")
        role = st.selectbox("OPERATIONAL ROLE", ["Inspector", "Analyst", "Cyber Expert"])
        p1 = st.text_input("SET PASSWORD", type="password")
        p2 = st.text_input("CONFIRM PASSWORD", type="password")
        secret_access_key = st.text_input("Secret Access Key", type="password")
        
        col_reg, col_close = st.columns(2)
        
        if col_reg.form_submit_button("CREATE ACCOUNT", use_container_width=True):
            if not secret_access_key or secret_access_key != os.getenv("OFFICER_SECRET_ACCESS_KEY"):
                st.error("Invalid Secret Access Key.")
            elif not all([name, email, p1]):
                st.error("ALL FIELDS REQUIRED.")
            elif p1 != p2:
                st.error("PASSWORDS DO NOT MATCH.")
            else:
                generated_id = f"CYBER2026{name.replace(' ', '').upper()}"
                officers = load_officers()
                officers[generated_id] = {
                    "name": name,
                    "email": email,
                    "role": role,
                    "password": p1,
                    "created_at": datetime.now().isoformat()
                }
                save_officers(officers)
                st.success(f"ACCOUNT CREATED. YOUR NODE ID IS: {generated_id}")
                st.session_state.show_officer_signup = False
        
        if col_close.form_submit_button("CLOSE", use_container_width=True):
            st.session_state.show_officer_signup = False
            st.rerun()

def logout_officer():
    st.session_state.officer_logged_in = False
    st.session_state.officer_id = None
