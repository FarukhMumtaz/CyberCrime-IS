"""
Cyber Crime Reporting System - Help & Support Page
Modern Premium Version
"""

import streamlit as st
from components import FAQSection

def render_help_page():
    st.markdown("## 🛰️ HELP & SUPPORT CENTER")
    st.write("Access emergency resources and victim support services.")

    # Emergency contacts
    st.markdown("### 🚨 EMERGENCY CHANNELS")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("""
        <div class="stMetric cyber-glow">
            <h4>PAKISTAN POLICE</h4>
            <p><strong>DIAL:</strong> 15</p>
            <p style="font-size:0.8rem; opacity:0.8;">Primary Emergency Response</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="stMetric cyber-glow">
            <h4>FIA CYBERCRIME</h4>
            <p><strong>HELPDESK:</strong> 111-342-111</p>
            <p style="font-size:0.8rem; opacity:0.8;">Federal Investigation Agency</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="stMetric cyber-glow">
            <h4>NCIA UNIT</h4>
            <p><strong>PORTAL:</strong> ncia.gov.pk</p>
            <p style="font-size:0.8rem; opacity:0.8;">Specialized Investigations</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Victim support
    st.markdown("### 🛡️ VICTIM SUPPORT PROTOCOL")
    st.info("""
    **If you are a victim of cybercrime, initialize the following protocol immediately:**
    1. **HALT COMMUNICATION:** Do not engage with the threat actor.
    2. **DATA PRESERVATION:** Take high-resolution screenshots of all evidence.
    3. **NODE ISOLATION:** Change passwords and enable MFA on all affected accounts.
    4. **REPORT:** Initialize a case report on this portal immediately.
    """)

    # FAQ section
    st.markdown("---")
    st.markdown("### ❓ OPERATIONAL FAQ")
    FAQSection.render_faqs()

    # Contact form
    st.markdown("---")
    st.markdown("### 📧 DIRECT INQUIRY")
    with st.form("contact_form"):
        st.write("Send a secure inquiry to our support analysts.")
        st.markdown('<div class="complaint-form">', unsafe_allow_html=True)
        
        name = st.text_input("NAME / ALIAS")
        email = st.text_input("CONTACT EMAIL")
        subject = st.selectbox("SUBJECT NODE", ["General Inquiry", "Technical Issue", "Legal Question", "Feedback"])
        message = st.text_area("DETAILED MESSAGE")
        
        submitted = st.form_submit_button("DISPATCH MESSAGE", type="primary", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if submitted:
            if not name or not email or not message:
                st.error("ALL NODES IN FORM MUST BE POPULATED.")
            else:
                st.success("🛰️ MESSAGE DISPATCHED. RESPONSE WILL BE ROUTED TO YOUR EMAIL.")

if __name__ == "__main__":
    render_help_page()