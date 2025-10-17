# SMTP Error Troubleshooting Guide

## 🐛 Common SMTP Errors & Solutions

### Error: "Invalid domain name" (501)

```
ERROR - SMTP error: (501, b'5.5.4 Invalid domain name [TP0P295CA0057.TWNP295.PROD.OUTLOOK.COM]')
```

#### ✅ Solutions Applied

The script has been updated with the following fixes:

1. **Properly Formatted From Header**
   ```python
   msg["From"] = f"HPC Admin <{SMTP_USER}>"  # Instead of just SMTP_USER
   ```

2. **Email Validation**
   - Validates recipient email has "@" symbol
   - Validates SMTP_USER is properly formatted
   - Logs errors if emails are invalid

3. **Better SMTP Connection Handling**
   - Added timeout (30 seconds)
   - Added detailed logging for each step
   - Better error messages

#### 🔧 Additional Checks

If you still get the error, check your `.env` file:

**❌ Wrong:**
```bash
SMTP_USER=amaorisaki@outlook.com 
# (with extra space at the end)
```

**✅ Correct:**
```bash
SMTP_USER=amaorisaki@outlook.com
```

**Also check:**
```bash
# Make sure no quotes around email
SMTP_USER=amaorisaki@outlook.com     # ✅ Good
SMTP_USER="amaorisaki@outlook.com"   # ❌ May cause issues
```

---

### Error: Authentication Failed (535)

```
ERROR - SMTP authentication failed. Check email credentials.
```

#### Solutions:

1. **Use Outlook App Password (Not Regular Password)**
   - Go to: https://account.microsoft.com/security
   - Click "Advanced security options"
   - Under "App passwords", click "Create a new app password"
   - Use that password in `.env` file

2. **Enable 2-Factor Authentication**
   - App passwords only work with 2FA enabled
   - Go to: https://account.microsoft.com/security
   - Turn on "Two-step verification"

3. **Check Account Settings**
   - Make sure SMTP is enabled for your account
   - Some organizations block SMTP access

---

### Error: Connection Timeout

```
ERROR - SMTP connection error: timed out
```

#### Solutions:

1. **Check Firewall**
   ```bash
   # Test if port 587 is accessible
   telnet smtp-mail.outlook.com 587
   ```

2. **Try Alternative Port**
   In `.env`:
   ```bash
   SMTP_PORT=587  # Try this first (STARTTLS)
   # or
   SMTP_PORT=465  # SSL/TLS (may need code changes)
   ```

3. **Check Internet Connection**
   ```bash
   ping smtp-mail.outlook.com
   ```

---

### Error: Recipient Rejected (550)

```
ERROR - SMTP error: (550, b'5.7.1 Unable to relay')
```

#### Solutions:

1. **Verify Recipient Email**
   - Make sure `email_ntu` in CSV is correct
   - Must be a valid email address

2. **Check "From" Address**
   - Must match your authenticated SMTP_USER
   - Or be authorized to send from that account

---

## 🧪 Test SMTP Connection

Create a test script `test_smtp.py`:

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Your settings
SMTP_SERVER = "smtp-mail.outlook.com"
SMTP_PORT = 587
SMTP_USER = "amaorisaki@outlook.com"
SMTP_PASS = "your_app_password"

try:
    print(f"Connecting to {SMTP_SERVER}:{SMTP_PORT}...")
    
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as smtp:
        smtp.set_debuglevel(1)  # Show detailed output
        
        print("Starting TLS...")
        smtp.starttls()
        
        print("Logging in...")
        smtp.login(SMTP_USER, SMTP_PASS)
        
        print("Creating test message...")
        msg = MIMEMultipart()
        msg["From"] = f"HPC Admin <{SMTP_USER}>"
        msg["To"] = "test@ntu.edu.tw"
        msg["Subject"] = "Test Email"
        msg.attach(MIMEText("This is a test.", "plain"))
        
        print("Sending message...")
        smtp.send_message(msg)
        
        print("✅ SUCCESS! Email sent successfully.")
        
except Exception as e:
    print(f"❌ ERROR: {e}")
```

Run:
```bash
python3 test_smtp.py
```

---

## 📋 Checklist for SMTP Issues

- [ ] SMTP_USER is a valid email address (no spaces, no quotes)
- [ ] SMTP_PASS is an **App Password** (not regular password)
- [ ] 2-Factor Authentication is enabled on Outlook account
- [ ] Port 587 is not blocked by firewall
- [ ] Recipient email addresses are valid
- [ ] No trailing spaces in `.env` file
- [ ] `.env` file is in the correct directory
- [ ] `.env` encoding is UTF-8 (not UTF-16 or other)

---

## 🔍 Enable Debug Mode

To see detailed SMTP communication, edit `auto_hpc_account.py`:

```python
# Change this line (around line 305):
smtp.set_debuglevel(0)  # Change 0 to 1

# To:
smtp.set_debuglevel(1)  # Shows all SMTP commands
```

This will show you exactly what's being sent/received.

---

## 📧 Two PDF Attachments

### Setup

In `.env` file:
```bash
PDF_GUIDE_PATH=slurm_guide.pdf
PDF_GUIDE_PATH_2=additional_guide.pdf
```

### File Structure
```
HPC/
├── auto_hpc_account.py
├── slurm_guide.pdf          ← First PDF
├── additional_guide.pdf     ← Second PDF (optional)
├── applicants.csv
└── .env
```

### Notes
- If `PDF_GUIDE_PATH_2` is empty or file doesn't exist, it's skipped (no error)
- Both PDFs will be attached to every email
- Filename in email = actual filename from disk

---

## 🚀 Quick Fix Commands

```bash
# 1. Check .env file for issues
cat .env | grep SMTP

# 2. Test SMTP connection
python3 test_smtp.py

# 3. Run with dry-run to test without sending
python3 auto_hpc_account.py --dry-run

# 4. Check logs for detailed errors
tail -f logs/hpc_account_*.log

# 5. Verify PDFs exist
ls -lh *.pdf
```

---

## 📞 Still Having Issues?

1. Check logs: `logs/hpc_account_*.log`
2. Enable debug mode: `smtp.set_debuglevel(1)`
3. Test SMTP separately with test script
4. Verify Outlook account settings
5. Contact: ntueehpc@googlegroups.com

---

**Last Updated:** October 17, 2025
