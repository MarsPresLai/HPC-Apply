#!/usr/bin/env python3
"""
Simple Email Tester
-------------------
Send a test email using SMTP with TLS.
Environment variables are used for SMTP configuration.

Required .env or environment variables:
  SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASS
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
load_dotenv()
# Load from environment
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")


def send_test_email(recipient: str):
    """Send a simple test email."""
    print(f"Preparing to send test email to {recipient}...")
    
    # Validate email format
    if "@" not in recipient or "@" not in SMTP_USER:
        print("❌ Invalid email format detected")
        return False

    msg = MIMEMultipart()
    msg["From"] = SMTP_USER  # Use plain email, not formatted
    msg["To"] = recipient
    msg["Subject"] = "[TEST] Email Functionality Check"

    body = (
        "This is a test email sent from your Python SMTP configuration.\n\n"
        "If you received this message, your SMTP setup works correctly!"
    )
    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        print(f"Connecting to {SMTP_SERVER}:{SMTP_PORT}...")
        smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30)
        smtp.set_debuglevel(0)  # Set to 1 for detailed output
        
        print("Starting TLS encryption...")
        smtp.starttls()
        
        print("Logging in...")
        smtp.login(SMTP_USER, SMTP_PASS)
        
        print("Sending message...")
        smtp.sendmail(SMTP_USER, recipient, msg.as_string())
        
        smtp.quit()
        
        print("✅ Email sent successfully!")
        print(f"✅ Check inbox at: {recipient}")
        return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("   Check SMTP_USER and SMTP_PASS in .env")
        print("   Make sure you're using an App Password (not regular password)")
        return False
    except smtplib.SMTPException as e:
        print(f"❌ SMTP Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("=" * 60)
    print(" SIMPLE SMTP EMAIL TESTER ")
    print("=" * 60)
    print()

    # Verify config
    print("Checking configuration...")
    if not SMTP_SERVER:
        print("❌ SMTP_SERVER not set")
    else:
        print(f"✅ SMTP_SERVER: {SMTP_SERVER}")
    
    if not SMTP_PORT:
        print("❌ SMTP_PORT not set")
    else:
        print(f"✅ SMTP_PORT: {SMTP_PORT}")
    
    if not SMTP_USER:
        print("❌ SMTP_USER not set")
    else:
        print(f"✅ SMTP_USER: {SMTP_USER}")
    
    if not SMTP_PASS:
        print("❌ SMTP_PASS not set")
    else:
        print(f"✅ SMTP_PASS: ***{SMTP_PASS[-4:] if len(SMTP_PASS) > 4 else '***'}")
    
    print()
    
    if not all([SMTP_SERVER, SMTP_USER, SMTP_PASS]):
        print("❌ Missing SMTP configuration. Please check your .env file")
        return

    recipient = input(f"Recipient email (press Enter for {SMTP_USER}): ").strip() or SMTP_USER
    print()
    
    success = send_test_email(recipient)
    
    print()
    print("=" * 60)
    if success:
        print("✅ TEST PASSED!")
    else:
        print("❌ TEST FAILED - Check errors above")
    print("=" * 60)


if __name__ == "__main__":
    main()
