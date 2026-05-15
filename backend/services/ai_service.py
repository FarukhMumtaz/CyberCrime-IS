"""
Cyber Crime Reporting System - AI Service

Handles AI-powered complaint analysis and legal guidance.
"""

import os
import groq
from typing import Optional, Dict, Any
import logging
import re

logger = logging.getLogger(__name__)

class AIService:
    """Service for AI operations using Groq."""

    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if self.api_key:
            try:
                self.client = groq.Client(api_key=self.api_key)
                logger.info("Groq client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Groq client: {e}")
                self.client = None
        else:
            logger.warning("Groq API key not set")
            self.client = None

    def categorize_complaint(self, description: str) -> Optional[str]:
        """Categorize complaint using AI."""
        if not self.client:
            return None

        try:
            prompt = f"""
            Analyze this cybercrime complaint and determine the most appropriate category from:
            - Hacking
            - Phishing
            - Cyberstalking
            - Online Harassment
            - Data Theft
            - Financial Fraud
            - Child Exploitation
            - Other

            Complaint: {description}

            Return only the category name.
            """

            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-8b-8192",
                max_tokens=50,
                temperature=0.1
            )

            category = response.choices[0].message.content.strip()
            return category if category in [
                "Hacking", "Phishing", "Cyberstalking", "Online Harassment",
                "Data Theft", "Financial Fraud", "Child Exploitation", "Other"
            ] else "Other"

        except Exception as e:
            logger.error(f"Error categorizing complaint: {e}")
            return None

    def summarize_complaint(self, description: str) -> Optional[str]:
        """Generate summary of complaint."""
        if not self.client:
            return None

        try:
            prompt = f"""
            Summarize this cybercrime complaint in 2-3 sentences, focusing on key facts and evidence:

            Complaint: {description}
            """

            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-8b-8192",
                max_tokens=200,
                temperature=0.3
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"Error summarizing complaint: {e}")
            return None

    def get_legal_guidance(self, complaint_type: str, description: str) -> Optional[str]:
        """Get legal guidance for complaint type."""
        if not self.client:
            return None

        try:
            prompt = f"""
            Based on Pakistan's Prevention of Electronic Crimes Act (PECA) 2016,
            provide brief legal guidance for a {complaint_type} complaint.

            Complaint details: {description}

            Focus on:
            1. Applicable sections
            2. Recommended actions
            3. Evidence preservation tips

            Keep response under 300 words.
            """

            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-8b-8192",
                max_tokens=300,
                temperature=0.2
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"Error getting legal guidance: {e}")
            return None

    def sanitize_prompt(self, prompt: str) -> str:
        """Sanitize AI prompts."""
        # Remove potentially harmful content
        sanitized = re.sub(r'[<>]', '', prompt)
        return sanitized[:1000]  # Limit length

    def validate_response(self, response: str) -> bool:
        """Validate AI response for safety."""
        # Check for harmful content
        harmful_patterns = [
            r'hack', r'exploit', r'malware', r'virus',
            r'illegal', r'criminal', r'terror'
        ]
        for pattern in harmful_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                return False
        return True

# Global instance
ai_service = AIService()