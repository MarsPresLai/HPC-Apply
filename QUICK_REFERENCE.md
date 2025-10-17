# 🚀 Quick Reference Card

## 📋 Step-by-Step Workflow

### 1️⃣ Export from Google Forms
```
Google Form → Responses → Google Sheets Icon → File → Download → CSV
```

### 2️⃣ Fix the Header Row
Open CSV, replace first line with:
```csv
time,email_address,user_type,name,student_id,email_ntu,professor,drive_link
```

### 3️⃣ Save & Test
```bash
# Save as applicants.csv in HPC/ folder
cd HPC
python3 auto_hpc_account.py --dry-run
```

### 4️⃣ Run for Real
```bash
python3 auto_hpc_account.py
```

---

## 📝 CSV Header (Copy-Paste This)

```csv
time,email_address,user_type,name,student_id,email_ntu,professor,drive_link
```

---

## 👥 User Type → Group Mapping

| Google Form Answer | Group | Username Example |
|-------------------|-------|------------------|
| 大學部學生 | 1 (undergrad) | b12901194 |
| 碩士班學生 | 2 (master) ⚠️ | r12921001 |
| 博士班學生 | 3 (phd) ⚠️ | d12941001 |
| 教授 | 4 (professor) | profchen |
| 管理員 | 5 (admin) | admin01 |

⚠️ = Professor name **required**

---

## ✅ Validation Checklist

Before running, ensure:
- [ ] CSV has correct English headers
- [ ] All rows have `student_id` (used as username)
- [ ] All rows have `email_ntu` (for notifications)
- [ ] Master/PhD students have professor name
- [ ] File saved as UTF-8 encoding
- [ ] File named `applicants.csv` in HPC/ folder

---

## 🧪 Test Commands

```bash
# Test without creating accounts
python3 auto_hpc_account.py --dry-run

# Run with custom CSV
python3 auto_hpc_account.py --csv batch1.csv

# View latest log
tail -f logs/hpc_account_*.log

# Check for errors
grep -i error logs/hpc_account_*.log
```

---

## 📧 What Gets Sent

Each applicant receives:
- ✉️ Email to: `email_ntu` (NTU school email)
- 🔑 Username: `student_id`
- 🔐 Password: Auto-generated (12 chars)
- 📄 Attachment: Slurm guide PDF
- 🇨🇳🇬🇧 Bilingual: Chinese + English

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| "Missing email or username" | Check `student_id` and `email_ntu` are filled |
| "Professor name required" | Add professor for master/phd students |
| "Unknown user type" | Check spelling of 大學部學生, 碩士班學生, etc. |
| "SSH authentication failed" | Check `.env` file credentials |
| "SMTP authentication failed" | Use Outlook App Password |

---

## 📂 File Locations

```
HPC/
├── auto_hpc_account.py    # Main script
├── applicants.csv         # ← Your exported file goes here
├── .env                   # ← Your credentials
├── logs/                  # ← Check here for details
└── slurm_guide.pdf        # PDF to attach
```

---

## 🔧 Quick .env Setup

```bash
# Copy template
cp .env.example .env

# Edit with your credentials
SMTP_USER=amaorisaki@outlook.com
SMTP_PASS=your_outlook_app_password
SSH_USER=sudoer1
SSH_PASS=your_ssh_password
```

---

## 📊 Expected Output

```
============================================================
Processing: 王小明 (b12901194) - b12901194
Email: b12901194@ntu.edu.tw
Group: 1 (undergrad)
============================================================
✅ Successfully created account: b12901194
📧 Successfully sent email to b12901194@ntu.edu.tw
```

---

## 🎯 Success Indicators

Look for these in logs:
- ✅ `Successfully created account`
- ✅ `Successfully sent email`
- ✅ `User xxx added to LDAP successfully`
- ✅ `done ! please check`

---

## ⚡ Commands Cheat Sheet

```bash
# Full workflow
cd HPC
python3 auto_hpc_account.py --dry-run  # Test
python3 auto_hpc_account.py            # Execute

# Check last account created
ssh sudoer1@140.112.170.43 -p 2201
sacctmgr show assoc where user=b12901194

# View logs
ls -lt logs/
cat logs/hpc_account_20251017_*.log
```

---

## 📞 Get Help

- 📖 Full guide: `GOOGLE_FORMS_GUIDE.md`
- 🚀 Setup: `QUICK_START.md`
- 📧 Email: ntueehpc@googlegroups.com

---

**Print this page and keep it handy! 📄**
