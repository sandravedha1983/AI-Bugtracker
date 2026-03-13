from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message, Mail
from flask import url_for, render_template
import os
import logging

from extensions import mail


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_otp():
    import random
    return str(random.randint(100000, 999999))

def send_otp_email(to_email, otp_code):
    """Sends a 6-digit verification code to the user's email."""
    msg = Message(
        subject="AI Bug Tracker Verification Code",
        recipients=[to_email],
    )

    msg.body = f"""
Welcome to AI Bug Tracker.

Your verification code is:

{otp_code}

Enter this code in the verification page to complete your registration.
"""
    
    # HTML version for better UI
    msg.html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px; border: 1px solid #e2e8f0; border-radius: 12px;">
        <h2 style="color: #1a202c;">Welcome to AI Bug Tracker</h2>
        <p style="color: #4a5568;">Please use the following 6-digit code to verify your account:</p>
        <div style="background-color: #f7fafc; padding: 20px; text-align: center; border-radius: 8px; margin: 24px 0;">
            <span style="font-size: 32px; font-weight: bold; letter-spacing: 5px; color: #2d3748;">{otp_code}</span>
        </div>
        <p style="color: #718096; font-size: 14px;">This code will expire in 1 hour.</p>
        <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 24px 0;">
        <p style="color: #a0aec0; font-size: 12px; text-align: center;">&copy; 2026 AI Bug Tracker • Secure Issue Management</p>
    </div>
    """

    try:
        mail.send(msg)
        logger.info(f"SUCCESS: OTP email sent to {to_email}")
        return True
    except Exception as e:
        logger.error(f"CRITICAL EMAIL FAILURE: Failed to send to {to_email}")
        logger.error(f"ERROR DETAILS: {str(e)}")
        return False

def send_verification_email(to_email, otp_code):
    """Sends a verification email with the 6-digit OTP code."""
    return send_otp_email(to_email, otp_code)

def send_resend_verification_email(to_email, otp_code):
    """Alias for send_verification_email."""
    return send_otp_email(to_email, otp_code)
