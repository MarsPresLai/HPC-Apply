# ✅ CSV Format Update - Summary

## 🎯 What Changed

I've updated the system to work directly with your Google Forms export format.

---

## 📋 Your Google Form Structure

**Original headers from your form:**
```
時間戳記 | 電子郵件地址 | 你是... | 姓名 | 學號 | 電子郵件(學校email) | 指導教授（大學部免填） | 學生證上傳
```

**New CSV format (with English headers for the script):**
```csv
time,email_address,user_type,name,student_id,email_ntu,professor,drive_link
```

---

## 🔧 Updates Made

### 1. **Updated `applicants.csv`**
Changed to match your Google Form structure with English column names.

**Example row:**
```csv
2025/10/17 下午 3:27:57,b12901194@ntu.edu.tw,大學部學生,Mars Lai,b12901194,b12901194@ntu.edu.tw,,https://drive.google.com/...
```

### 2. **Added `convert_user_type_to_group()` Function**
Automatically converts Chinese user types to group numbers:

| 你是... | Group # |
|---------|---------|
| 大學部學生 | 1 |
| 碩士班學生 | 2 |
| 博士班學生 | 3 |
| 教授 | 4 |
| 管理員 | 5 |

### 3. **Updated `process_applicants()` Function**
Now handles both formats:
- ✅ New Google Form format (`user_type`, `email_ntu`, `student_id`)
- ✅ Old manual format (`group`, `email`, `username`)
- ✅ Automatic conversion from Chinese to group numbers
- ✅ Better error messages

### 4. **Created `GOOGLE_FORMS_GUIDE.md`**
Complete guide for:
- How to export from Google Forms
- Column mapping explanation
- Common issues and solutions
- Testing procedures

---

## 📝 How to Use

### Step 1: Export from Google Forms

1. Open your Google Form responses
2. Click the **Google Sheets** icon
3. In the spreadsheet, **File** → **Download** → **CSV**
4. Save as `applicants.csv`

### Step 2: Update Headers

Open the CSV and **replace the first line** with:
```csv
time,email_address,user_type,name,student_id,email_ntu,professor,drive_link
```

**Before:**
```csv
時間戳記	電子郵件地址	你是...	姓名	學號	電子郵件( 請填寫學校email帳號 ex: XXX@ntu.edu.tw )	指導教授（大學部免填）	學生證上傳
```

**After:**
```csv
time,email_address,user_type,name,student_id,email_ntu,professor,drive_link
```

### Step 3: Run the Script

Test first:
```bash
python3 auto_hpc_account.py --dry-run
```

Then run for real:
```bash
python3 auto_hpc_account.py
```

---

## 🎯 Key Features

### ✅ Automatic User Type Conversion
No need to manually convert "大學部學生" to "1" - the script does it automatically!

```python
"大學部學生" → Group 1 (undergrad)
"碩士班學生" → Group 2 (master)
"博士班學生" → Group 3 (phd)
```

### ✅ Flexible Column Names
The script works with:
- `student_id` → used as username
- `email_ntu` → used for email notifications
- `user_type` → automatically converted to group number

### ✅ Backward Compatible
Still works with the old format if you have manually created CSV files.

---

## 📊 Example CSV File

```csv
time,email_address,user_type,name,student_id,email_ntu,professor,drive_link
2025/10/17 15:00:00,student1@gmail.com,大學部學生,王小明,b12901194,b12901194@ntu.edu.tw,,https://drive.google.com/...
2025/10/17 15:05:00,student2@gmail.com,碩士班學生,李大華,r12921001,r12921001@ntu.edu.tw,張教授,https://drive.google.com/...
2025/10/17 15:10:00,student3@gmail.com,博士班學生,陳小美,d12941001,d12941001@ntu.edu.tw,王教授,https://drive.google.com/...
```

---

## ⚠️ Important Notes

### 1. Username = Student ID
The script uses `student_id` as the Linux username:
- `b12901194` → username will be `b12901194`

### 2. Email Notifications
Sent to `email_ntu` (the NTU school email), not `email_address`.

### 3. Professor Required
For 碩士班學生 (Master) and 博士班學生 (PhD):
- ✅ Must have professor name
- ❌ Row will be **skipped** if professor is empty

### 4. User Types Accepted
The script is flexible and accepts:
- `大學部學生`, `大學部`, `undergrad`
- `碩士班學生`, `碩士生`, `碩士`, `master`
- `博士班學生`, `博士生`, `博士`, `phd`
- `教授`, `professor`
- `管理員`, `admin`

---

## 🧪 Test Output Example

```bash
$ python3 auto_hpc_account.py --dry-run

Processing applicants from applicants.csv

============================================================
Processing: 王小明 (b12901194) - b12901194
Email: b12901194@ntu.edu.tw
Group: 1 (undergrad)
============================================================
[DRY RUN] Would create account for b12901194 (group: 1)
[DRY RUN] Would send email to b12901194@ntu.edu.tw

============================================================
Processing: 李大華 (r12921001) - r12921001
Email: r12921001@ntu.edu.tw
Group: 2 (master)
Professor: 張教授
============================================================
[DRY RUN] Would create account for r12921001 (group: 2)
[DRY RUN] Would send email to r12921001@ntu.edu.tw

============================================================
SUMMARY
============================================================
Total applicants: 2
Accounts created: 2
Emails sent: 2
```

---

## 📚 Documentation Files

- **`GOOGLE_FORMS_GUIDE.md`** ← Complete guide for Google Forms export
- **`CSV_FORMAT.md`** ← Original CSV format guide
- **`QUICK_START.md`** ← Quick setup instructions
- **`IMPLEMENTATION.md`** ← Technical details

---

## 🚀 You're Ready!

1. ✅ Export from Google Forms
2. ✅ Replace header row with English names
3. ✅ Save as `applicants.csv`
4. ✅ Test with `--dry-run`
5. ✅ Run for real!

**The script will automatically:**
- Convert "大學部學生" → Group 1
- Convert "碩士班學生" → Group 2
- Convert "博士班學生" → Group 3
- Use `student_id` as username
- Send emails to `email_ntu`
- Validate professor requirements

---

**Questions?** Check `GOOGLE_FORMS_GUIDE.md` or contact ntueehpc@googlegroups.com

🎉 **All set! The system now works seamlessly with your Google Forms!**
