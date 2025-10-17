# Quick Setup & Usage Guide

## 🚀 Setup (First Time Only)

### 1. Install Dependencies
```bash
cd HPC
pip install -r requirements.txt
```

### 2. Create `.env` File
```bash
cp .env.example .env
```

Edit `.env`:
```bash
# Email Configuration
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USER=amaorisaki@outlook.com
SMTP_PASS=your_outlook_password

# SSH Configuration
SSH_HOST=140.112.170.43
SSH_PORT=2201
SSH_USER=sudoer1
SSH_PASS=your_ssh_password

# Script Location
ADD_USER_SCRIPT_PATH=/home/sudoer1/add_user.sh

# PDF Guide
PDF_GUIDE_PATH=slurm_guide.pdf
```

### 3. Prepare CSV File

Create `applicants.csv` with this format:
```csv
time,email,name,student_id,username,group,professor,password,drive_link
2025/10/17 15:00:00,student@ntu.edu.tw,學生姓名,b12345678,b12345678,1,,,
```

**Group Numbers:**
- `1` = Undergraduate
- `2` = Master (requires professor name)
- `3` = PhD (requires professor name)
- `4` = Professor
- `5` = Admin

See `CSV_FORMAT.md` for detailed examples.

---

## ▶️ Usage

### Test Mode (Recommended First)
```bash
python3 auto_hpc_account.py --dry-run
```
This shows what will happen without actually creating accounts or sending emails.

### Create Accounts
```bash
python3 auto_hpc_account.py
```

### Use Custom CSV File
```bash
python3 auto_hpc_account.py --csv /path/to/custom.csv
```

---

## 📊 What the Script Does

For each applicant in the CSV:

1. **Connects via SSH** to `140.112.170.43:2201`
2. **Checks if user exists** in LDAP
3. **Runs `add_user.sh`** with:
   - Username
   - Group number (1-5)
   - Professor name (if needed)
   - Password (auto-generated or custom)
4. **Sends bilingual email** with:
   - Username and password
   - SSH login instructions
   - Slurm guide PDF attachment
5. **Logs everything** to `logs/hpc_account_TIMESTAMP.log`

---

## 📝 The `add_user.sh` Script

The script automates:
- ✅ LDAP user creation
- ✅ Home directory setup (`/storage/group/username`)
- ✅ Slurm account configuration
- ✅ Group-based permissions
- ✅ Password policy enforcement

**Group-specific behavior:**
- **Undergrad**: Own account, student QOS
- **Master/PhD**: Personal + professor account, higher QOS
- **Professor**: Own account with professor QOS
- **Admin**: Full access with normal QOS

---

## 📧 Email Template

Recipients receive:

**Subject:** HPC 帳號建立通知 / HPC Account Created

**Content:**
- Username and temporary password
- SSH login command
- Security reminder (change password on first login)
- Slurm guide PDF attachment
- Support contact: ntueehpc@googlegroups.com

---

## 🔍 Check Logs

```bash
cat logs/hpc_account_*.log
```

Look for:
- ✅ `Successfully created account`
- 📧 `Successfully sent email`
- ⚠️ Warnings or errors

---

## ✅ Verify Account Creation

SSH to the server:
```bash
ssh sudoer1@140.112.170.43 -p 2201
```

Check LDAP:
```bash
ldapsearch -x -H ldap://192.168.110.21 \
  -D 'cn=Manager,dc=hpc,dc=ntuee,dc=org' \
  -w 'ntuee123' \
  -b 'ou=People,dc=hpc,dc=ntuee,dc=org' \
  '(cn=b12345678)'
```

Check Slurm:
```bash
sacctmgr show assoc where user=b12345678
```

Check home directory:
```bash
ls -la /storage/undergrad/b12345678
```

---

## 🐛 Troubleshooting

### Problem: "SSH authentication failed"
**Solution:** Check `SSH_USER` and `SSH_PASS` in `.env`

### Problem: "SMTP authentication failed"
**Solution:** 
- Use Outlook App Password (not regular password)
- Enable 2FA at https://account.microsoft.com/security

### Problem: "Script execution may have failed"
**Solution:**
- Check if `add_user.sh` exists at the correct path
- Verify SSH user has sudo privileges
- Check logs for detailed error messages

### Problem: "Professor name required"
**Solution:** Add professor name in CSV for group 2 (master) or 3 (phd)

### Problem: "User already exists"
**Solution:** This is normal - script skips existing users automatically

---

## 📁 File Structure

```
HPC/
├── auto_hpc_account.py      # Main script
├── applicants.csv           # Your applicant data
├── .env                     # Your credentials (DO NOT COMMIT)
├── .env.example             # Template
├── requirements.txt         # Python dependencies
├── slurm_guide.pdf          # PDF attachment
├── CSV_FORMAT.md            # CSV format guide
├── QUICK_START.md           # This file
├── README.md                # Full documentation
└── logs/                    # Execution logs
    └── hpc_account_*.log
```

---

## 🔐 Security Best Practices

1. **Never commit `.env`** - Add to `.gitignore`
2. **Use SSH keys** instead of passwords when possible
3. **Restrict log file permissions**: `chmod 600 logs/*.log`
4. **Regularly rotate passwords**
5. **Review logs** after each batch

---

## 📞 Support

- **Email:** ntueehpc@googlegroups.com
- **Logs:** Always attach `logs/` files when reporting issues

---

## ✨ Quick Command Reference

```bash
# Test without executing
python3 auto_hpc_account.py --dry-run

# Run for real
python3 auto_hpc_account.py

# Custom CSV
python3 auto_hpc_account.py --csv batch1.csv

# View latest log
tail -f logs/hpc_account_*.log

# Check script help
python3 auto_hpc_account.py --help
```

Good luck! 🚀
