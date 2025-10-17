# CSV File Format Guide

## 📋 Required CSV Columns

Your `applicants.csv` file must include the following columns:

| Column | Required | Description | Example |
|--------|----------|-------------|---------|
| `time` | Optional | Application timestamp | `2025/10/17 下午 3:27:57` |
| `email` | **Required** | Applicant's email address | `b12901193@ntu.edu.tw` |
| `name` | **Required** | Applicant's full name | `潘哈哈` |
| `student_id` | Optional | Student/Staff ID | `b12901193` |
| `username` | **Required** | HPC username to create | `b12901193` |
| `group` | **Required** | User group (1-5, see below) | `1` |
| `professor` | Conditional | Professor name (required for groups 2 & 3) | `張教授` |
| `password` | Optional | Custom password (auto-generated if empty) | Leave blank |
| `drive_link` | Optional | Google Drive link or notes | `https://...` |

---

## 👥 Group Numbers

Use these values in the `group` column:

| Number | Group | Description | Professor Required? |
|--------|-------|-------------|---------------------|
| `1` | undergrad | Undergraduate student | ❌ No |
| `2` | master | Master's student | ✅ **Yes** |
| `3` | phd | PhD student | ✅ **Yes** |
| `4` | professor | Professor/Faculty | ❌ No |
| `5` | admin | Administrator | ❌ No |

---

## 📝 CSV Examples

### Example 1: Undergraduate Student
```csv
time,email,name,student_id,username,group,professor,password,drive_link
2025/10/17 15:00:00,b12901193@ntu.edu.tw,潘哈哈,b12901193,b12901193,1,,,
```

### Example 2: Master's Student (Professor Required)
```csv
time,email,name,student_id,username,group,professor,password,drive_link
2025/10/17 15:30:00,r12921001@ntu.edu.tw,王小明,r12921001,r12921001,2,張教授,,
```

### Example 3: PhD Student with Custom Password
```csv
time,email,name,student_id,username,group,professor,password,drive_link
2025/10/17 16:00:00,d12941001@ntu.edu.tw,李大華,d12941001,d12941001,3,陳教授,MySecure123,
```

### Example 4: Professor Account
```csv
time,email,name,student_id,username,group,professor,password,drive_link
2025/10/17 16:30:00,prof_chen@ntu.edu.tw,陳教授,prof001,profchen,4,,,
```

### Example 5: Multiple Users
```csv
time,email,name,student_id,username,group,professor,password,drive_link
2025/10/17 15:00:00,b12901193@ntu.edu.tw,潘哈哈,b12901193,b12901193,1,,,
2025/10/17 15:05:00,r12921001@ntu.edu.tw,王小明,r12921001,r12921001,2,張教授,,
2025/10/17 15:10:00,d12941001@ntu.edu.tw,李大華,d12941001,d12941001,3,陳教授,,
2025/10/17 15:15:00,prof_wang@ntu.edu.tw,王教授,prof002,profwang,4,,,
```

---

## ⚠️ Important Notes

### Professor Field Rules
- **REQUIRED** for `group=2` (master) and `group=3` (phd)
- **NOT REQUIRED** for other groups
- Used by Slurm to assign accounts properly
- If missing for master/phd, the row will be **skipped**

### Password Field
- Leave **blank** to auto-generate a secure 12-character password
- Provide custom password if needed (not recommended for security)
- Auto-generated passwords use letters + digits only

### Username Requirements
- Must be valid Linux username (lowercase, no spaces)
- Will be used for SSH login
- Must be unique across the system

---

## 🔄 Exporting from Google Sheets

1. Open your Google Sheet
2. Click **File** → **Download** → **Comma Separated Values (.csv)**
3. Save as `applicants.csv`
4. Place in the `HPC/` directory

**Google Sheets Template:**

| time | email | name | student_id | username | group | professor | password | drive_link |
|------|-------|------|------------|----------|-------|-----------|----------|------------|
| 2025/10/17 15:00:00 | b12901193@ntu.edu.tw | 潘哈哈 | b12901193 | b12901193 | 1 | | | |

---

## ✅ Validation

The script will automatically:
- ✅ Check for missing required fields (email, username, name)
- ✅ Validate group numbers (1-5)
- ✅ Verify professor name exists for master/phd students
- ✅ Skip rows with validation errors
- ✅ Log all validation issues

---

## 🐛 Common Errors

### Error: "Professor name required for master/phd student"
**Solution**: Add professor name in the `professor` column for group 2 or 3

### Error: "Invalid group"
**Solution**: Use only numbers 1-5 in the `group` column

### Error: "Missing email or username"
**Solution**: Ensure both `email` and `username` columns are filled

---

## 📊 Processing Summary

After running the script, you'll see:

```
============================================================
SUMMARY
============================================================
Total applicants: 5
Accounts created: 4
Accounts failed: 0
Skipped: 1 (missing professor for master student)
Emails sent: 4
Emails failed: 0
============================================================
```

Check the `logs/` directory for detailed processing information.
