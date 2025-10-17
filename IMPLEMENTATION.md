# 🎉 HPC Account Automation - Implementation Summary

## ✅ What I've Modified

### 1. **Updated `auto_hpc_account.py`**

#### Changed: `create_account()` Function
- **Before**: Used basic Linux `useradd` commands
- **After**: Now interacts with your `add_user.sh` script

**New Parameters:**
```python
def create_account(username, group_number="1", professor="", custom_password="")
```

**How It Works:**
1. Connects to server via SSH
2. Checks if user exists in LDAP
3. Runs `sudo /home/sudoer1/add_user.sh` interactively
4. Sends inputs programmatically:
   - Username
   - Group number (1-5)
   - Professor name (for master/phd)
   - Password (auto-generated or custom)
5. Waits for completion and checks output
6. Returns password for email notification

#### Changed: `process_applicants()` Function
Now reads additional CSV columns:
- `group` - User type (1=undergrad, 2=master, 3=phd, 4=professor, 5=admin)
- `professor` - Professor name (required for master/phd)
- `password` - Optional custom password

**Validation Added:**
- ✅ Checks group is valid (1-5)
- ✅ Ensures professor name exists for master/phd students
- ✅ Skips invalid rows with clear error messages
- ✅ Logs group type in human-readable format

---

### 2. **Updated `.env.example`**

Added new configuration:
```bash
ADD_USER_SCRIPT_PATH=/home/sudoer1/add_user.sh
```

Updated SMTP for Outlook:
```bash
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USER=amaorisaki@outlook.com
```

---

### 3. **Updated `applicants.csv`**

New format with required columns:
```csv
time,email,name,student_id,username,group,professor,password,drive_link
```

**New Required Column:**
- `group` - Must be 1-5

**New Optional Columns:**
- `professor` - Required for group 2 & 3
- `password` - Leave blank for auto-generation

---

### 4. **Created New Documentation Files**

#### `CSV_FORMAT.md`
- Complete guide to CSV columns
- Examples for all user types
- Validation rules
- Troubleshooting tips

#### `QUICK_START.md`
- Step-by-step setup instructions
- Usage examples
- Command reference
- Troubleshooting guide

---

## 🔧 Technical Implementation Details

### SSH Interactive Shell Approach

The script uses `paramiko.invoke_shell()` to interact with the bash script:

```python
channel = ssh.invoke_shell()
channel.send("sudo /home/sudoer1/add_user.sh\n")

# Send inputs line by line
channel.send(f"{username}\n")
channel.send(f"{group_number}\n")
channel.send(f"{professor}\n")
channel.send(f"{password}\n")

# Wait and collect output
time.sleep(5)
output = channel.recv(4096).decode('utf-8')
```

**Why this approach?**
- ✅ Handles interactive prompts from `read -p`
- ✅ Works with scripts that require user input
- ✅ Captures all output for logging
- ✅ Properly handles sudo password prompts (if needed)

---

## 📋 Group Mapping

Your `add_user.sh` script handles these group types:

| Group # | Type | LDAP gidNumber | Storage Path | Slurm QOS |
|---------|------|----------------|--------------|-----------|
| 1 | undergrad | 1201 | `/storage/undergrad/` | studentbasic |
| 2 | master | 2201 | `/storage/master/` | masterbasic |
| 3 | phd | 3201 | `/storage/phd/` | phdbasic |
| 4 | professor | 4201 | `/storage/professor/` | professorbasic |
| 5 | admin | 5201 | `/storage/admin/` | normal |

---

## 🔍 What Happens Step-by-Step

1. **Read CSV** → Load applicant data with group info
2. **Validate** → Check required fields and group numbers
3. **SSH Connect** → Connect to `140.112.170.43:2201`
4. **Check Existence** → Query LDAP to see if user exists
5. **Run Script** → Execute `add_user.sh` with proper inputs
6. **LDAP Creation** → Script adds user to LDAP with hashed password
7. **Storage Setup** → Script creates `/storage/group/username`
8. **Slurm Config** → Script configures Slurm accounts and QOS
9. **Send Email** → Python sends bilingual notification with password
10. **Log Everything** → Save detailed logs to `logs/` folder

---

## 🎯 Key Features Added

### ✅ Group-Based Account Creation
- Supports all 5 user types
- Automatic Slurm QOS assignment
- Proper storage directory creation

### ✅ Professor Association
- Master/PhD students linked to professor accounts
- Required field validation
- Slurm account hierarchy

### ✅ Enhanced Validation
- Group number validation
- Professor requirement checks
- User existence checks (LDAP)

### ✅ Better Logging
- Human-readable group names
- Detailed script output
- Error tracking

### ✅ Flexible Configuration
- Configurable script path
- Support for custom passwords
- Optional fields

---

## 📊 CSV Examples for Different User Types

### Undergraduate Student
```csv
2025/10/17 15:00:00,b12901193@ntu.edu.tw,潘哈哈,b12901193,b12901193,1,,,
```

### Master's Student (needs professor)
```csv
2025/10/17 15:30:00,r12921001@ntu.edu.tw,王小明,r12921001,r12921001,2,張教授,,
```

### PhD Student (needs professor)
```csv
2025/10/17 16:00:00,d12941001@ntu.edu.tw,李大華,d12941001,d12941001,3,陳教授,,
```

### Professor Account
```csv
2025/10/17 16:30:00,prof@ntu.edu.tw,陳教授,prof001,profchen,4,,,
```

---

## 🧪 Testing Recommendations

### 1. Dry Run First
```bash
python3 auto_hpc_account.py --dry-run
```
This shows what will happen without executing.

### 2. Test with Single User
Create a test CSV with one user:
```csv
time,email,name,student_id,username,group,professor,password,drive_link
2025/10/17 15:00:00,test@ntu.edu.tw,測試用戶,test001,testuser,1,,,
```

### 3. Verify on Server
After running, SSH to server and check:
```bash
# Check LDAP
ldapsearch -x -H ldap://192.168.110.21 \
  -D 'cn=Manager,dc=hpc,dc=ntuee,dc=org' -w 'ntuee123' \
  -b 'ou=People,dc=hpc,dc=ntuee,dc=org' '(cn=testuser)'

# Check Slurm
sacctmgr show assoc where user=testuser

# Check home directory
ls -la /storage/undergrad/testuser
```

---

## ⚠️ Important Security Notes

### 1. SSH User Privileges
Your SSH user (`sudoer1`) must have:
- ✅ Sudo privileges without password prompt (or configure NOPASSWD in sudoers)
- ✅ Access to LDAP admin credentials
- ✅ Permissions to create storage directories

### 2. LDAP Credentials in Script
Your `add_user.sh` contains hardcoded LDAP admin password:
```bash
admin_password="ntuee123"
```
Consider moving this to a secure configuration file.

### 3. Sensitive Data
- `.env` contains SSH and email passwords
- `logs/` contain passwords (encrypted in LDAP but visible in logs)
- Restrict file permissions: `chmod 600 .env logs/*.log`

---

## 🚀 Next Steps

### Ready to Use!
1. Copy `.env.example` to `.env`
2. Fill in your credentials
3. Prepare your CSV file
4. Run `--dry-run` to test
5. Execute for real!

### Optional Enhancements
Consider adding:
- Status column in CSV to track processed users
- Email retry logic for failed sends
- Slack/Discord notifications
- Web dashboard for monitoring
- Batch processing with progress bars

---

## 📞 Need Help?

Check documentation:
- `QUICK_START.md` - Quick setup guide
- `CSV_FORMAT.md` - CSV format details
- `README.md` - Full documentation
- `logs/` - Detailed execution logs

Contact: ntueehpc@googlegroups.com

---

**Created:** October 17, 2025  
**Version:** 1.1.0 (add_user.sh integration)
