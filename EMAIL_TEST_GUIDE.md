# 📧 Email Testing Guide

## 🚀 Quick Start

Test your email configuration without creating any HPC accounts:

```bash
cd HPC
python3 test_email.py
```

---

## 📋 What the Test Does

The test script will:

1. ✅ Check your `.env` configuration
2. ✅ Verify SMTP credentials
3. ✅ Check if PDF files exist
4. ✅ Send a test email with the same format as production
5. ✅ Attach PDF files (if they exist)
6. ✅ Show detailed logs of each step

**Important:** No HPC accounts are created during testing!

---

## 🎯 Test Output Example

```
======================================================================
HPC EMAIL FUNCTIONALITY TEST
======================================================================

2025-10-17 17:30:00 - INFO - Checking environment variables...
2025-10-17 17:30:00 - INFO - ✅ SMTP_SERVER: smtp-mail.outlook.com
2025-10-17 17:30:00 - INFO - ✅ SMTP_PORT: 587
2025-10-17 17:30:00 - INFO - ✅ SMTP_USER: amaorisaki@outlook.com
2025-10-17 17:30:00 - INFO - ✅ SMTP_PASS: ***i71

2025-10-17 17:30:00 - INFO - Checking PDF files...
2025-10-17 17:30:00 - INFO - ✅ First PDF found: slurm_guide.pdf (1,234,567 bytes)
2025-10-17 17:30:00 - INFO - ✅ Second PDF found: additional_guide.pdf (987,654 bytes)

----------------------------------------------------------------------

Enter recipient email (press Enter for amaorisaki@outlook.com): 

2025-10-17 17:30:05 - INFO - Sending test email to: amaorisaki@outlook.com
2025-10-17 17:30:05 - INFO - Test username: test_user
2025-10-17 17:30:05 - INFO - Test password: TestPass123

----------------------------------------------------------------------

2025-10-17 17:30:05 - INFO - Preparing test email for amaorisaki@outlook.com
2025-10-17 17:30:05 - INFO - ✅ Attached first PDF: slurm_guide.pdf
2025-10-17 17:30:05 - INFO - ✅ Attached second PDF: additional_guide.pdf
2025-10-17 17:30:05 - INFO - Connecting to SMTP server smtp-mail.outlook.com:587
2025-10-17 17:30:06 - INFO - Starting TLS...
2025-10-17 17:30:07 - INFO - Logging in...
2025-10-17 17:30:08 - INFO - Sending test message with 2 PDF attachment(s)...
2025-10-17 17:30:10 - INFO - 📧 ✅ Successfully sent test email to amaorisaki@outlook.com

======================================================================
✅ TEST PASSED - Email sent successfully!
======================================================================

Please check your inbox (and spam folder) for the test email.
The email should have:
  - Subject: [TEST] HPC 帳號建立通知 / HPC Account Created
  - Bilingual content (Chinese + English)
  - Test username and password
  - PDF attachment(s) if configured
======================================================================
```

---

## 📝 Test Email Content

The test email will look exactly like a production email, except:

**Subject:**
```
[TEST] HPC 帳號建立通知 / HPC Account Created
```

**Body includes:**
- ⚠️ Warning banner: "THIS IS A TEST EMAIL - NO ACTUAL ACCOUNT WAS CREATED"
- Test credentials (username: `test_user`, password: `TestPass123`)
- Bilingual content (Chinese + English)
- SSH login instructions
- PDF attachments (if configured)

---

## 🎛️ Customization

### Send to Different Email

When prompted, enter any email address:
```
Enter recipient email (press Enter for amaorisaki@outlook.com): student@ntu.edu.tw
```

Or press Enter to send to yourself (SMTP_USER).

### Change Test Data

Edit `test_email.py` around line 200:
```python
test_username = "test_user"      # Change this
test_password = "TestPass123"    # Change this
test_name = "測試用戶 Test User"   # Change this
```

---

## ✅ What to Check in the Test Email

When you receive the test email, verify:

- [ ] Subject line is correct
- [ ] Email displays correctly (no encoding issues)
- [ ] Chinese characters display properly
- [ ] English section displays properly
- [ ] Test username and password are visible
- [ ] SSH command is correct
- [ ] First PDF is attached
- [ ] Second PDF is attached (if configured)
- [ ] No spam/phishing warnings
- [ ] Sender is "HPC Admin <your-email>"

---

## 🐛 Common Issues

### Issue 1: "SMTP authentication failed"
**Solution:**
- Use an **App Password**, not your regular password
- Go to: https://account.microsoft.com/security
- Create a new app password
- Update `SMTP_PASS` in `.env`

### Issue 2: "Invalid domain name" (501)
**Solution:**
- Check `.env` for extra spaces:
  ```bash
  SMTP_USER=amaorisaki@outlook.com     # ✅ Good
  SMTP_USER=amaorisaki@outlook.com     # ❌ Bad (space)
  ```
- Remove quotes if present:
  ```bash
  SMTP_USER=amaorisaki@outlook.com     # ✅ Good
  SMTP_USER="amaorisaki@outlook.com"   # ❌ Bad
  ```

### Issue 3: "Connection timeout"
**Solution:**
- Check firewall allows port 587
- Test connection:
  ```bash
  telnet smtp-mail.outlook.com 587
  ```

### Issue 4: PDFs not attached
**Check:**
- PDF files exist in HPC/ directory
- Filenames match `.env` configuration
- File permissions allow reading

---

## 🔍 Enable Verbose Debug Mode

To see detailed SMTP communication, edit `test_email.py` line ~112:

```python
# Change:
smtp.set_debuglevel(0)

# To:
smtp.set_debuglevel(1)  # Shows all SMTP commands
```

This will show you every command sent to/from the SMTP server.

---

## 📊 Test Multiple Recipients

Create a simple loop test:

```python
# test_multiple.py
from test_email import send_test_email

recipients = [
    "student1@ntu.edu.tw",
    "student2@ntu.edu.tw",
    "student3@ntu.edu.tw"
]

for email in recipients:
    print(f"\nTesting {email}...")
    send_test_email(email, "test_user", "TestPass123", "Test User")
```

---

## 🔄 After Successful Test

Once the test passes:

1. ✅ Check your email inbox
2. ✅ Verify all content displays correctly
3. ✅ Check PDF attachments open properly
4. ✅ Ready to run the full script!

```bash
# Run the full script in dry-run mode
python3 auto_hpc_account.py --dry-run

# Run for real when ready
python3 auto_hpc_account.py
```

---

## 📞 Still Having Issues?

1. Run the test with debug mode enabled
2. Check `SMTP_TROUBLESHOOTING.md` for detailed help
3. Verify Outlook account settings
4. Test with a simple SMTP client separately
5. Contact: ntueehpc@googlegroups.com

---

## 💡 Pro Tips

- **Test to yourself first** - Press Enter when prompted for recipient
- **Check spam folder** - First test emails might go to spam
- **Add to safe senders** - Mark as "Not spam" to whitelist the sender
- **Test before batch runs** - Always test after changing email templates
- **Keep test logs** - Useful for troubleshooting

---

## 📁 Files Needed

```
HPC/
├── test_email.py          # Test script
├── .env                   # Your credentials
├── slurm_guide.pdf        # First PDF (optional)
├── additional_guide.pdf   # Second PDF (optional)
└── ...
```

---

**Quick Test Command:**
```bash
python3 test_email.py
```

**That's it!** 🚀
