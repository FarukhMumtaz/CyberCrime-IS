"""
Separate Streamlit entry point for officer authentication and case management.
"""

import pathlib
import sys
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

ROOT_DIR = pathlib.Path(__file__).resolve().parent
FRONTEND_DIR = ROOT_DIR / "frontend"

for _p in (str(ROOT_DIR), str(FRONTEND_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

load_dotenv(ROOT_DIR / ".env")


def load_css():
    css_path = FRONTEND_DIR / "static" / "styles.css"
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def initialize_session():
    if "officer_logged_in" not in st.session_state:
        st.session_state.officer_logged_in = False
    if "current_page" not in st.session_state:
        st.session_state.current_page = (
            "officer_panel" if st.session_state.officer_logged_in else "officer_login"
        )


def navigate_to(page_name: str):
    st.session_state.current_page = page_name
    st.rerun()


def main():
    st.set_page_config(page_title="Officer Portal", page_icon="🔐", layout="wide")
    initialize_session()
    load_css()

    st.markdown(
        """<div class="main-header"><h1>🔐 OFFICER PORTAL</h1><p>Secure law enforcement access for complaint review and case decisions</p></div>""",
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.markdown("### 🔐 OFFICER ACCESS")
        if st.session_state.get("officer_logged_in"):
            st.success(f"ACTIVE ID: {st.session_state.get('officer_id')}")
            if st.button("📊 OFFICER PANEL", use_container_width=True):
                navigate_to("officer_panel")
            if st.button("🚪 LOGOUT", use_container_width=True):
                st.session_state.officer_logged_in = False
                st.session_state.officer_id = None
                st.session_state.current_page = "officer_login"
                st.rerun()
        else:
            st.info("Authenticate or register with the official access key.")

    if st.session_state.get("officer_logged_in"):
        st.session_state.current_page = "officer_panel"

    if st.session_state.get("officer_logged_in"):
        from views.officer_panel import render_officer_panel

        render_officer_panel(set_page_config=False)
    else:
        from views.officer_login import render_officer_login

        render_officer_login(set_page_config=False)

    st.markdown(
        f"""<div class="footer"><p>© {datetime.now().year} NCIA Pakistan</p></div>""",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
