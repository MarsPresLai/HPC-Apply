# Google Forms to CSV Conversion Guide

## 📋 Your Google Form Structure

Your form has these columns:
```
時間戳記 | 電子郵件地址 | 你是... | 姓名 | 學號 | 電子郵件(學校email) | 指導教授（大學部免填） | 學生證上傳
```

---

## ✅ Required CSV Format

The script expects this format:

```csv
time,email_address,user_type,name,student_id,email_ntu,professor,drive_link
```

### Column Mapping:

| Google Form Column | CSV Column | Description | Example |
|-------------------|------------|-------------|---------|
| 時間戳記 | `time` | Application timestamp | `2025/10/17 下午 3:27:57` |
| 電子郵件地址 | `email_address` | Google account email | `student@gmail.com` |
| 你是... | `user_type` | User type (see below) | `大學部學生` |
| 姓名 | `name` | Full name | `王小明` |
| 學號 | `student_id` | Student ID (used as username) | `b12901194` |
| 電子郵件(學校email) | `email_ntu` | NTU email (for notifications) | `b12901194@ntu.edu.tw` |
| 指導教授（大學部免填） | `professor` | Professor name | `張教授` |
| 學生證上傳 | `drive_link` | Google Drive link | `https://...` |

---

## 👥 User Type Mapping

The script automatically converts these Chinese user types to group numbers:

| 你是... (User Type) | Group # | English |
|-------------------|---------|---------|
| 大學部學生 | 1 | Undergraduate |
| 碩士班學生 / 碩士生 / 碩士 | 2 | Master |
| 博士班學生 / 博士生 / 博士 | 3 | PhD |
| 教授 | 4 | Professor |
| 管理員 | 5 | Admin |

**Note:** The script is flexible and accepts variations of these terms.

---

## 📝 Example CSV

### Single Undergraduate Student
```csv
time,email_address,user_type,name,student_id,email_ntu,professor,drive_link
2025/10/17 下午 3:27:57,student@gmail.com,大學部學生,王小明,b12901194,b12901194@ntu.edu.tw,,https://drive.google.com/...
```

### Master's Student (Professor Required)
```csv
time,email_address,user_type,name,student_id,email_ntu,professor,drive_link
2025/10/17 下午 3:30:00,master@gmail.com,碩士班學生,李大華,r12921001,r12921001@ntu.edu.tw,張教授,https://drive.google.com/...
```

### Multiple Users
```csv
time,email_address,user_type,name,student_id,email_ntu,professor,drive_link
2025/10/17 15:00:00,student1@gmail.com,大學部學生,王小明,b12901194,b12901194@ntu.edu.tw,,https://drive.google.com/...
2025/10/17 15:05:00,student2@gmail.com,碩士班學生,李大華,r12921001,r12921001@ntu.edu.tw,張教授,https://drive.google.com/...
2025/10/17 15:10:00,student3@gmail.com,博士班學生,陳小美,d12941001,d12941001@ntu.edu.tw,王教授,https://drive.google.com/...
```

---

## 🔄 How to Export from Google Forms

### Method 1: Direct Export
1. Open your Google Form responses
2. Click the **Google Sheets** icon (green spreadsheet)
3. In the spreadsheet, click **File** → **Download** → **Comma Separated Values (.csv)**
4. Open the CSV in a text editor
5. **Rename the header row** to match the format above:
   ```csv
   time,email_address,user_type,name,student_id,email_ntu,professor,drive_link
   ```
6. Save as `applicants.csv`

### Method 2: Google Sheets Formula (Automated)
Create a new sheet in your Google Sheets with this formula in A1:

```
=ARRAYFORMULA(IF(ROW('表單回應 1'!A:A)=1,
  {"time","email_address","user_type","name","student_id","email_ntu","professor","drive_link"},
  IF(LEN('表單回應 1'!A:A),
    {'表單回應 1'!A:A,'表單回應 1'!B:B,'表單回應 1'!C:C,'表單回應 1'!D:D,'表單回應 1'!E:E,'表單回應 1'!F:F,'表單回應 1'!G:G,'表單回應 1'!H:H},
    "")))
```

Then download this processed sheet as CSV.

---

## ⚠️ Important Notes

### 1. Professor Field
- **REQUIRED** for 碩士班學生 (Master) and 博士班學生 (PhD)
- **Optional** for 大學部學生 (Undergrad)
- Leave blank for undergraduate students

### 2. Student ID = Username
- The `student_id` column is used as the **Linux username**
- Must be unique across all users
- Typically: `b12901194` (undergrad), `r12921001` (master), `d12941001` (phd)

### 3. Email Field
- Use the **NTU email** (`email_ntu` column) for account notifications
- This is where the password and login instructions will be sent

### 4. User Type Flexibility
The script accepts multiple formats:
- ✅ `大學部學生`
- ✅ `大學部`
- ✅ `undergrad`
- ✅ `碩士班學生`, `碩士生`, `碩士`
- ✅ `博士班學生`, `博士生`, `博士`

---

## 🧪 Testing Your CSV

Before running the script, test with:

```bash
python3 auto_hpc_account.py --dry-run
```

This will show you:
- ✅ How each user type is converted to group numbers
- ✅ Which fields are missing
- ✅ Any validation errors
- ✅ What would happen without actually creating accounts

---

## 🐛 Common Issues

### Issue 1: "Missing email or username"
**Cause:** `student_id` or `email_ntu` column is empty  
**Solution:** Ensure all applicants filled in both fields

### Issue 2: "Professor name required for master/phd student"
**Cause:** Master/PhD student without professor name  
**Solution:** Contact applicant to provide professor name, or manually add to CSV

### Issue 3: Headers don't match
**Cause:** CSV exported with Chinese headers  
**Solution:** Replace first line with English headers:
```csv
time,email_address,user_type,name,student_id,email_ntu,professor,drive_link
```

### Issue 4: Encoding problems
**Cause:** CSV encoding is not UTF-8  
**Solution:** Save CSV as UTF-8:
- In Excel: **File** → **Save As** → **CSV UTF-8 (Comma delimited)**
- In Notepad++: **Encoding** → **Convert to UTF-8**

---

## 📊 Validation Summary

After preparing your CSV, the script will:

1. ✅ Read all rows
2. ✅ Convert user types to group numbers automatically
3. ✅ Validate required fields (email, student_id)
4. ✅ Check professor requirements for master/phd
5. ✅ Skip invalid rows with clear error messages
6. ✅ Log all validation issues

---

## 📞 Support

If you encounter issues:
1. Run with `--dry-run` to see what's wrong
2. Check logs in `logs/` folder
3. Contact: ntueehpc@googlegroups.com

---

**Last Updated:** October 17, 2025
