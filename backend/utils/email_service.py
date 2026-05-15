import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)

def send_case_update_email(recipient_email, tracking_id, status, notes):
    """
    Sends a professional case update email.
    """
    # Stripping whitespace to prevent [Errno 11001] and other common copy-paste issues
    smtp_server = os.getenv('SMTP_SERVER', '').strip()
    smtp_port = os.getenv('SMTP_PORT', '').strip()
    smtp_user = os.getenv('SMTP_USERNAME', '').strip()
    smtp_pass = os.getenv('SMTP_PASSWORD', '').strip()

    if not all([smtp_server, smtp_port, smtp_user, smtp_pass]):
        err = "SMTP configuration incomplete. Please check your .env or Secrets."
        logger.error(err)
        return False, err

    try:
        smtp_port = int(smtp_port)
        msg = MIMEMultipart()
        msg['From'] = f"NCIA Cyber Portal <{smtp_user}>"
        msg['To'] = recipient_email
        msg['Subject'] = f"OFFICIAL CASE UPDATE: {tracking_id}"

        color = "#3b82f6" if status.lower() == "approved" else "#10b981" if status.lower() == "solved" else "#ef4444"
        
        html = f"""
        <div style="font-family: sans-serif; max-width: 650px; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden;">
            <div style="background: #1e3a8a; color: white; padding: 25px; text-align: center;">
                <h1 style="margin: 0; font-size: 24px;">NCIA CYBERCRIME WING</h1>
                <p style="margin: 5px 0 0 0; opacity: 0.9;">Government of Pakistan</p>
            </div>
            <div style="padding: 40px;">
                <p>Hello,</p>
                <p>Your reported case <b style="color: #1e3a8a;">{tracking_id}</b> has been processed.</p>
                <div style="background: #f7fafc; padding: 20px; border-left: 6px solid {color}; margin: 25px 0;">
                    <p style="margin: 0; font-weight: bold;">Case Status: <span style="color: {color};">{status.upper()}</span></p>
                </div>
                <div style="white-space: pre-line; line-height: 1.6; color: #2d3748;">
                    {notes}
                </div>
            </div>
            <div style="background: #edf2f7; padding: 20px; text-align: center; font-size: 11px; color: #a0aec0;">
                This is an automated notification. Do not reply.
            </div>
        </div>
        """
        
        msg.attach(MIMEText(html, 'html'))

        # Set timeout to 20s for slow networks
        with smtplib.SMTP(smtp_server, smtp_port, timeout=20) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        
        return True, "Dispatch successful."

    except Exception as e:
        err_msg = str(e)
        # Detailed hint for Errno 11001
        if "11001" in err_msg:
            err_msg += " (Hint: The SMTP server address is unreachable or incorrectly formatted. Check for typos like 'smtp.gmail.com')"
        logger.error(f"SMTP Error: {err_msg}")
        return False, err_msg
