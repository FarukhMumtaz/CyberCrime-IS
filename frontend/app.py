"""
Cyber Crime Reporting System - Main Application
Clean Stable Navigation (Dynamic Key Strategy)
"""

import streamlit as st
import os
import sys
import pathlib
from dotenv import load_dotenv
from datetime import datetime

# ── Path setup ────────────────────────────────────────────────────────────────
FRONTEND_DIR = pathlib.Path(__file__).resolve().parent
ROOT_DIR     = FRONTEND_DIR.parent

for _p in (str(ROOT_DIR), str(FRONTEND_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

load_dotenv()

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Cyber Portal PK", page_icon="🛡️", layout="wide")

# ── Custom CSS Loader ─────────────────────────────────────────────────────────
def load_css():
    css_path = FRONTEND_DIR / "static" / "styles.css"
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Session management ────────────────────────────────────────────────────────
def initialize_session():
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    if 'officer_logged_in' not in st.session_state:
        st.session_state.officer_logged_in = False

def navigate_to(page_name: str):
    """Simple, clean navigation using session state."""
    st.session_state.current_page = page_name
    st.rerun()

# ── Main ──
def main():
    initialize_session()
    load_css()

    st.markdown("""<div class="main-header"><h1>🛡️ CYBER CRIME PORTAL</h1><p>Government of Pakistan - Law Enforcement Access</p></div>""", unsafe_allow_html=True)

    # ── Sidebar ──
    with st.sidebar:
        st.markdown("### 🗺️ NAVIGATION")
        
        # Base pages
        pages = {
            "🏠 Home": "home",
            "📋 Report Crime": "report_form",
            "📍 Track Status": "tracking",
            "📚 Legal Guide": "law_guide",
            "❓ Help Center": "help_support"
        }
        
        # Add dynamic officer options
        if st.session_state.current_page == "officer_login":
            pages["🔐 Officer Login"] = "officer_login"
        elif st.session_state.current_page == "officer_panel":
            pages["👮 Officer Panel"] = "officer_panel"
            
        page_labels = list(pages.keys())
        page_values = list(pages.values())
        
        try:
            current_idx = page_values.index(st.session_state.current_page)
        except ValueError:
            current_idx = 0
            
        # 🔑 STABILITY FIX: Dynamic Key Strategy
        # By including current_page in the key, we force Streamlit to refresh the radio
        # when the page changes via a button, ensuring the 'index' is always applied.
        radio_key = f"nav_radio_{st.session_state.current_page}"
        selected_label = st.radio("Access Node:", page_labels, index=current_idx, key=radio_key)
        selected_page = pages[selected_label]
        
        # Handle User Interaction via Radio
        if selected_page != st.session_state.current_page:
            st.session_state.current_page = selected_page
            st.rerun()

        st.markdown("---")
        if not st.session_state.get('officer_logged_in'):
            if st.button("🔑 OFFICER AUTHENTICATION", use_container_width=True):
                navigate_to("officer_login")
        else:
            st.success(f"ACTIVE ID: {st.session_state.get('officer_id')}")
            if st.button("📊 DASHBOARD", use_container_width=True):
                navigate_to("officer_panel")
            if st.button("🚪 LOGOUT", use_container_width=True):
                st.session_state.officer_logged_in = False
                st.session_state.officer_id = None
                navigate_to("home")

    # ── Page Routing ──
    current = st.session_state.current_page
    if current == "home":
        show_home_page()
    elif current == "report_form":
        from views.report_form import render_report_form
        render_report_form(set_page_config=False)
    elif current == "tracking":
        from views.tracking import render_tracking_page
        render_tracking_page(set_page_config=False)
    elif current == "law_guide":
        from views.law_guide import render_law_guide_page
        render_law_guide_page()
    elif current == "help_support":
        from views.help import render_help_page
        render_help_page()
    elif current == "officer_login":
        from views.officer_login import render_officer_login
        render_officer_login(set_page_config=False)
    elif current == "officer_panel":
        from views.officer_panel import render_officer_panel
        render_officer_panel(set_page_config=False)

    # ── Chatbot ──
    from components.chatbot import render_chatbot
    with st.expander("🤖 CYBER ASSISTANT (AI)", expanded=False):
        render_chatbot()

    st.markdown(f"""<div class="footer"><p>© {datetime.now().year} NCIA Pakistan</p></div>""", unsafe_allow_html=True)

def show_home_page():
    st.markdown("### 🛰️ GLOBAL THREAT MONITOR")
    c1, c2, c3 = st.columns(3)
    c1.metric("NETWORK", "SECURE")
    c2.metric("COMPLIANCE", "PECA 2016")
    c3.metric("UPTIME", "100%")
    st.markdown("---")
    st.info("💡 Use the sidebar to initiate a report or track your existing case status.")
    if st.button("START COMPLAINT FORM", type="primary", use_container_width=True):
        navigate_to("report_form")

if __name__ == "__main__":
    main()