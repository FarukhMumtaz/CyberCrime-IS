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
        
        pages = {
            "🏠 Home": "home",
            "📋 Report Crime": "report_form",
            "📍 Track Status": "tracking",
            "📚 Legal Guide": "law_guide",
            "❓ Help Center": "help_support"
        }

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
        selected_label = st.radio("Portal Access:", page_labels, index=current_idx, key=radio_key)
        selected_page = pages[selected_label]
        
        # Handle User Interaction via Radio
        if selected_page != st.session_state.current_page:
            st.session_state.current_page = selected_page
            st.rerun()

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

    # ── Chatbot ──
    from components.chatbot import render_chatbot
    with st.expander("🤖 CYBER ASSISTANT (AI)", expanded=False):
        render_chatbot()

    st.markdown(f"""<div class="footer"><p>© {datetime.now().year} NCIA Pakistan</p></div>""", unsafe_allow_html=True)

def show_home_page():
    st.markdown("### 🛰️ Cyber Reporting Services")
    c1, c2, c3 = st.columns(3)
    service_cards = [
        (c1, "Report Cybercrime", "Submit a complaint with incident details and evidence."),
        (c2, "Track Complaint", "Check the review status of an existing case."),
        (c3, "Legal Awareness", "Read public guidance on cybercrime laws and safety."),
    ]
    for column, title, body in service_cards:
        column.markdown(
            f"""
            <div class="cyber-glow">
                <h4>{title}</h4>
                <p>{body}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("---")
    st.info("💡 Submit cybercrime reports securely and monitor complaint progress through the official digital portal.")
    if st.button("START COMPLAINT FORM", type="primary", use_container_width=True):
        navigate_to("report_form")

if __name__ == "__main__":
    main()
