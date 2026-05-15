"""
Cyber Crime Reporting System - Frontend Components

Reusable Streamlit components for the application.
"""

import streamlit as st
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class ComplaintForm:
    """Component for complaint form handling."""

    @staticmethod
    def render_form() -> Optional[Dict[str, Any]]:
        """Render the complaint form and return submitted data."""
        with st.form("complaint_form"):
            st.markdown('<div class="complaint-form">', unsafe_allow_html=True)

            # Personal Information (Optional for anonymity)
            st.subheader("Personal Information (Optional)")
            anonymous = st.checkbox("Report Anonymously", value=True)

            if not anonymous:
                col1, col2 = st.columns(2)
                with col1:
                    full_name = st.text_input("Full Name")
                    phone = st.text_input("Phone Number")
                with col2:
                    cnic = st.text_input("CNIC (13 digits)", max_chars=13)
                    address = st.text_area("Address")

            # Incident Details
            st.subheader("Incident Details")
            incident_date = st.date_input("Date of Incident")
            location = st.text_input("Incident Location")
            complaint_reason = st.selectbox(
                "Type of Cybercrime",
                ["Hacking", "Phishing", "Cyberstalking", "Online Harassment",
                 "Data Theft", "Financial Fraud", "Child Exploitation", "Other"]
            )
            description = st.text_area("Detailed Description", height=150)

            # Evidence Upload Section
            st.markdown('<div class="evidence-section">', unsafe_allow_html=True)
            st.subheader("📎 Electronic Evidence (Optional)")
            st.write("Upload supporting evidence securely. All files are encrypted and scanned.")

            uploaded_files = st.file_uploader(
                "Upload Evidence",
                type=['mp4', 'mov', 'avi', 'jpg', 'jpeg', 'png', 'pdf'],
                accept_multiple_files=True,
                help="Max video size: 1GB, Images/PDFs: 50MB each"
            )
            st.markdown('</div>', unsafe_allow_html=True)

            # Submit button
            submitted = st.form_submit_button("Submit Complaint", type="primary")

            st.markdown('</div>', unsafe_allow_html=True)

        if submitted:
            # Validate form
            if not complaint_reason:
                st.error("Please select the type of cybercrime.")
                return None

            if not description or len(description.strip()) < 10:
                st.error("Please provide a detailed description (minimum 10 characters).")
                return None

            if not anonymous:
                if not full_name or len(full_name.strip()) < 2:
                    st.error("Please provide your full name.")
                    return None
                if cnic and len(cnic) != 13:
                    st.error("CNIC must be exactly 13 digits.")
                    return None

            # Return form data
            return {
                "anonymous": anonymous,
                "full_name": full_name if not anonymous else None,
                "phone": phone if not anonymous else None,
                "cnic": cnic if not anonymous else None,
                "address": address if not anonymous else None,
                "incident_date": incident_date,
                "location": location,
                "complaint_reason": complaint_reason,
                "description": description,
                "uploaded_files": uploaded_files or []
            }

        return None

class LawGuide:
    """Component for displaying cyber laws."""

    @staticmethod
    def render_law_search() -> None:
        """Render the law search and display component."""
        # Search and filter
        col1, col2 = st.columns([2, 1])
        with col1:
            search_term = st.text_input("Search laws...", placeholder="Enter keywords...")
        with col2:
            category_filter = st.selectbox(
                "Filter by category:",
                ["All", "Unauthorized Access", "Data Damage", "Cyberstalking", "Phishing",
                 "Child Pornography", "Identity Theft", "Hacking", "Malware", "Data Theft",
                 "Spamming", "Online Harassment", "Financial Fraud", "Privacy Violation"]
            )

        # Mock law data (replace with API call)
        laws_data = [
            {
                "section": "13",
                "title": "Unauthorized access to information system",
                "category": "Unauthorized Access",
                "description": "Whoever intentionally accesses or causes access to any information system without lawful authority shall be punished.",
                "punishment": "Imprisonment up to 3 years or fine up to Rs. 5 million or both"
            },
            {
                "section": "20",
                "title": "Cyberstalking",
                "category": "Cyberstalking",
                "description": "Whoever uses information system to stalk or harass another person shall be punished.",
                "punishment": "Imprisonment up to 3 years or fine up to Rs. 1 million or both"
            },
            {
                "section": "21",
                "title": "Fraudulent use of information system",
                "category": "Phishing",
                "description": "Whoever uses information system to deceive or mislead any person or cause harm through fraudulent means shall be punished.",
                "punishment": "Imprisonment up to 3 years or fine up to Rs. 5 million or both"
            }
        ]

        # Filter laws
        filtered_laws = laws_data
        if search_term:
            filtered_laws = [law for law in filtered_laws
                            if search_term.lower() in law['title'].lower() or
                               search_term.lower() in law['description'].lower()]
        if category_filter != "All":
            filtered_laws = [law for law in filtered_laws if law['category'] == category_filter]

        # Display laws
        if filtered_laws:
            for law in filtered_laws:
                with st.expander(f"Section {law['section']}: {law['title']}"):
                    st.write(f"**Category:** {law['category']}")
                    st.write(f"**Description:** {law['description']}")
                    st.write(f"**Punishment:** {law['punishment']}")
                    st.write(f"**Relevant PECA Sections:** PECA Section {law['section']}")
        else:
            st.info("No laws found matching your search criteria.")

class StatusTracker:
    """Component for tracking complaint status."""

    @staticmethod
    def render_tracker() -> None:
        """Render the complaint status tracker."""
        st.subheader("Track Your Complaint")

        tracking_id = st.text_input(
            "Enter Tracking ID",
            placeholder="CCRS-PK-2024-XXXXXX",
            help="Enter the tracking ID you received after submitting your complaint"
        )

        if st.button("Check Status", type="primary"):
            if not tracking_id:
                st.error("Please enter a tracking ID.")
                return

            # TODO: Replace with actual API call
            # Mock status check
            if tracking_id.startswith("CCRS-PK-"):
                st.success("Complaint found!")
                st.info(f"**Status:** Under Review")
                st.write("**Last Updated:** 2024-01-15 14:30:00")
                st.write("**Next Steps:** Investigation in progress")
            else:
                st.error("Invalid tracking ID format.")

class FAQSection:
    """Component for FAQ display."""

    @staticmethod
    def render_faqs() -> None:
        """Render the FAQ section."""
        faq_data = [
            {
                "question": "What types of cybercrimes can I report?",
                "answer": "You can report hacking, phishing, cyberstalking, online harassment, data theft, financial fraud, child exploitation, and other cybercrimes."
            },
            {
                "question": "Is my report anonymous?",
                "answer": "Yes, you can choose to report anonymously. However, providing contact information helps authorities investigate more effectively."
            },
            {
                "question": "What evidence should I preserve?",
                "answer": "Save emails, messages, screenshots, URLs, transaction records, and any other relevant digital evidence. Do not delete or modify anything."
            },
            {
                "question": "How long does investigation take?",
                "answer": "Investigation time varies depending on the complexity of the case. You will receive updates via your tracking ID."
            },
            {
                "question": "Can I withdraw my complaint?",
                "answer": "Contact the investigating authority using your tracking ID if you need to withdraw or modify your complaint."
            },
            {
                "question": "What if I'm not in Pakistan?",
                "answer": "This system is designed for Pakistani citizens. For international incidents, contact local law enforcement or INTERPOL."
            }
        ]

        for faq in faq_data:
            with st.expander(faq["question"]):
                st.write(faq["answer"])