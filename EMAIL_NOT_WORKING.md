# 🐛 Email Test Not Working - Diagnosis & Solutions

## Problem Identified

Your email test is **hanging/timing out** when trying to connect to Outlook's SMTP server from WSL.

### Error Symptoms:
```
Connecting to smtp-mail.outlook.com:587...
Starting TLS encryption...
[HANGS HERE - Times out after 30 seconds]
```

Or:
```
SMTPServerDisconnected: Connection unexpectedly closed: timed out
```

---

## 🔍 Root Cause

**WSL Networking Issue**: WSL2 sometimes has problems with SMTP connections due to:
1. Windows Firewall blocking
2. WSL network translation issues  
3. VPN/Corporate network blocking port 587
4. Antivirus interfering with SMTP traffic

---

## ✅ Solutions (Try in Order)

### Solution 1: Use Windows Python (RECOMMENDED)

Instead of running from WSL, run directly in Windows Command Prompt or PowerShell:

```powershell
# In Windows PowerShell (not WSL):
cd C:\Users\user\Documents\Code\HPC
python test_email.py
```

This bypasses WSL network issues entirely.

---

### Solution 2: Check Windows Firewall

```powershell
# In Windows PowerShell (Run as Administrator):
# Check if port 587 is blocked
Test-NetConnection -ComputerName smtp-mail.outlook.com -Port 587

# Should show: TcpTestSucceeded : True
```

If it fails, temporarily disable Windows Firewall and test again.

---

### Solution 3: Try Alternative Port (465 SSL)

Some networks block port 587 but allow 465.

Edit `.env`:
```bash
SMTP_PORT=465
```

Then create this test script `test_email_ssl.py`:

```python
#!/usr/bin/env python3
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

msg = MIMEMultipart()
msg["From"] = SMTP_USER
msg["To"] = SMTP_USER
msg["Subject"] = "[TEST] SSL Connection"
msg.attach(MIMEText("Test email via SSL", "plain"))

try:
    print(f"Connecting via SSL to {SMTP_SERVER}:{SMTP_PORT}...")
    # Use SMTP_SSL for port 465
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=30) as smtp:
        print("Logging in...")
        smtp.login(SMTP_USER, SMTP_PASS)
        print("Sending...")
        smtp.sendmail(SMTP_USER, SMTP_USER, msg.as_string())
    print("✅ Email sent successfully via SSL!")
except Exception as e:
    print(f"❌ Error: {e}")
```

---

### Solution 4: Use Gmail Instead (If Available)

Gmail's SMTP is sometimes more reliable:

In `.env`:
```bash
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_gmail@gmail.com
SMTP_PASS=your_app_password
```

---

### Solution 5: Fix WSL Networking

```bash
# In WSL terminal:
# 1. Check if you can reach the server
ping smtp-mail.outlook.com

# 2. Check if port is accessible
nc -zv smtp-mail.outlook.com 587

# If connection fails, try resetting WSL network:
# In Windows PowerShell (Run as Administrator):
wsl --shutdown
# Then restart WSL
```

---

### Solution 6: Use Python Requests with SMTP Relay Service

If direct SMTP continues to fail, consider using a service like:
- SendGrid (free tier: 100 emails/day)
- Mailgun (free tier: 1000 emails/month)
- AWS SES (free tier: 62,000 emails/month)

---

## 🚀 Quick Test: Windows PowerShell Method

**EASIEST SOLUTION - Try this first:**

1. Open **Windows PowerShell** (not WSL)
2. Navigate to your project:
   ```powershell
   cd C:\Users\user\Documents\Code\HPC
   ```

3. Install dependencies (if needed):
   ```powershell
   pip install python-dotenv
   ```

4. Run the test:
   ```powershell
   python test_email.py
   ```

This should work because Windows Python has direct network access without WSL translation.

---

## 📝 Alternative: Test with curl

To verify SMTP server is accessible:

```bash
# In WSL or Windows:
curl -v --url "smtp://smtp-mail.outlook.com:587" \
  --mail-from "amaorisaki@outlook.com" \
  --mail-rcpt "amaorisaki@outlook.com" \
  --upload-file - <<EOF
From: amaorisaki@outlook.com
To: amaorisaki@outlook.com
Subject: Test

Test message
EOF
```

---

## 🔧 Temporary Workaround: Skip Email Testing

If you can't get SMTP working in your environment:

1. **Comment out email testing** for now
2. **Run account creation only**:
   ```python
   # In auto_hpc_account.py, comment out:
   # send_email(email, username, password, name)
   ```
3. **Manually email credentials** to users
4. **Fix SMTP later** when you have better network access

---

## 📊 Debugging Checklist

- [ ] Tried Windows PowerShell instead of WSL
- [ ] Tested with `Test-NetConnection` in PowerShell
- [ ] Verified `.env` has correct credentials
- [ ] Tried port 465 (SSL) instead of 587 (TLS)
- [ ] Disabled Windows Firewall temporarily
- [ ] Checked if VPN is interfering
- [ ] Tested `ping smtp-mail.outlook.com`
- [ ] Tested `nc -zv smtp-mail.outlook.com 587`
- [ ] Verified app password (not regular password)
- [ ] Tried from different network (mobile hotspot?)

---

## 💡 Recommended Solution

**Use Windows PowerShell** to run the script:

```powershell
# Windows PowerShell:
cd C:\Users\user\Documents\Code\HPC  
python test_email.py
```

This avoids all WSL networking issues! ✅

---

Need help? The issue is almost certainly WSL network translation, not your code or SMTP settings.
