"""
Cyber Crime Reporting System - Law Guide Page
Modern Premium Version
"""

import streamlit as st
from components import LawGuide

def render_law_guide_page():
    st.markdown("## ⚖️ CYBER LAW REPOSITORY")
    st.write("Access Pakistan's legal framework for digital security and electronic crimes.")

    # AI Legal Assistant
    st.markdown("""
    <div class="stMetric cyber-glow">
        <h3>🤖 NEURAL LEGAL ASSISTANT</h3>
        <p>Get instant guidance on PECA 2016 sections based on incident classification.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_sel, col_act = st.columns([3, 1])
    with col_sel:
        complaint_type = st.selectbox(
            "CLASSIFY YOUR SITUATION:",
            ["", "Hacking", "Phishing", "Cyberstalking", "Online Harassment",
             "Data Theft", "Financial Fraud", "Child Exploitation", "Other"]
        )
    with col_act:
        st.write("")
        st.write("")
        get_guidance = st.button("QUERY LAWS", type="primary", use_container_width=True)

    if get_guidance and complaint_type:
        st.markdown(f"""
        <div class="law-section">
            <h4>APPLICABLE LEGAL FRAMEWORK: {complaint_type.upper()}</h4>
            <p>Based on initial analysis, this incident falls under <strong>PECA 2016 Sections 13-16</strong>.</p>
            <p>Authorities prioritize these cases for unauthorized system access and digital intrusion.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Law search component
    st.markdown("### 📚 PECA 2016 LAWBOOK")
    LawGuide.render_law_search()

    st.markdown("---")
    
    st.warning("""
    ⚠️ **LEGAL DISCLAIMER:** This repository provides general guidance based on PECA 2016. 
    It does not constitute formal legal advice. For active litigation, consult qualified legal counsel.
    """)

if __name__ == "__main__":
    render_law_guide_page()