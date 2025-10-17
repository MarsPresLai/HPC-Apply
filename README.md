# HPC Account Automation Tool

自動化 HPC 帳號建立與通知系統 / Automated HPC Account Creation and Notification System

## 📋 功能特色 / Features

✅ **自動建立帳號** - SSH 遠端建立使用者帳戶  
✅ **自動寄送通知** - 雙語郵件（中英文）通知申請者  
✅ **安全密碼生成** - 使用 `secrets` 模組生成高強度密碼  
✅ **附件支援** - 自動附加 Slurm 使用說明 PDF  
✅ **完整日誌** - 記錄所有操作，方便審計與除錯  
✅ **錯誤處理** - 完善的異常處理，避免中斷  
✅ **Dry Run 模式** - 測試流程不實際執行

---

## 🗂️ 專案結構 / Project Structure

```
HPC/
├── auto_hpc_account.py      # 主程式
├── applicants.csv           # 申請者資料（從 Google Sheet 匯出）
├── slurm_guide.pdf          # Slurm 使用說明（附件）
├── requirements.txt         # Python 依賴套件
├── .env                     # 環境變數（敏感資訊，不要上傳）
├── .env.example             # 環境變數範本
├── logs/                    # 執行日誌資料夾
│   └── hpc_account_YYYYMMDD_HHMMSS.log
└── README.md                # 本檔案
```

---

## 🚀 快速開始 / Quick Start

### 1️⃣ 安裝 Python 依賴

```bash
cd HPC
pip install -r requirements.txt
```

或使用 Python 3:

```bash
pip3 install -r requirements.txt
```

---

### 2️⃣ 設定環境變數

複製範本並填入您的憑證：

```bash
cp .env.example .env
```

編輯 `.env` 檔案：

```bash
# SMTP 郵件設定（Gmail 範例）
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_gmail_app_password

# SSH 伺服器設定
SSH_HOST=140.112.170.43
SSH_PORT=2201
SSH_USER=admin
SSH_PASS=your_admin_password

# PDF 路徑
PDF_GUIDE_PATH=slurm_guide.pdf
```

> ⚠️ **Gmail 使用者請注意**：  
> 請使用 **應用程式密碼**（App Password），而非一般密碼  
> 產生方式：https://myaccount.google.com/apppasswords

---

### 3️⃣ 準備申請者資料

從 Google Sheet 匯出為 CSV 檔案，命名為 `applicants.csv`：

| time | email | name | student_id | username |
|------|-------|------|------------|----------|
| 2025/10/17 下午 3:27:57 | b12901999@ntu.edu.tw | 潘哈哈 | b12901193 | b12901999 |

CSV 格式範例：

```csv
time,email,name,student_id,username
2025/10/17 下午 3:27:57,b12901999@ntu.edu.tw,潘哈哈,b12901193,b12901999
```

---

### 4️⃣ 執行程式

#### 測試模式（不實際執行）

```bash
python3 auto_hpc_account.py --dry-run
```

#### 正式執行

```bash
python3 auto_hpc_account.py
```

#### 使用自訂 CSV 檔案

```bash
python3 auto_hpc_account.py --csv /path/to/custom.csv
```

---

## 📧 郵件範本 / Email Template

程式會自動寄送雙語郵件：

**主旨**：HPC 帳號建立通知 / HPC Account Created

**內容**：

- 使用者名稱與密碼
- SSH 登入指令
- 安全提醒（首次登入請修改密碼）
- 附件：Slurm 使用說明 PDF
- 聯絡方式：ntueehpc@googlegroups.com

---

## 📝 日誌系統 / Logging System

所有操作都會記錄在 `logs/` 資料夾：

```
logs/
└── hpc_account_20251017_152757.log
```

日誌內容包含：

- ✅ 帳號建立成功/失敗
- 📧 郵件寄送狀態
- ⚠️ 錯誤與警告訊息
- 📊 執行統計摘要

---

## 🔒 安全性建議 / Security Best Practices

1. **不要上傳 `.env` 檔案**  
   將 `.env` 加入 `.gitignore`

2. **使用 SSH Key 取代密碼**  
   在 `.env` 中設定：
   ```bash
   SSH_KEY_FILE=/path/to/your/private_key
   ```

3. **定期更換密碼**  
   郵件中會提醒使用者首次登入後修改密碼

4. **限制 CSV 檔案權限**
   ```bash
   chmod 600 applicants.csv
   ```

---

## 🛠️ 進階功能 / Advanced Features

### 自訂密碼長度

修改 `auto_hpc_account.py` 中的 `generate_password()` 函數：

```python
def generate_password(length=12):  # 改為 12 位數
    ...
```

### 修改郵件範本

編輯 `send_email()` 函數中的 `body` 變數。

### 批次處理多個 CSV 檔案

```bash
for file in applicants_*.csv; do
    python3 auto_hpc_account.py --csv "$file"
done
```

---

## 🐛 常見問題 / Troubleshooting

### 問題 1：SMTP 認證失敗

**解決方法**：  
確認使用 Gmail **應用程式密碼**，而非一般密碼

### 問題 2：SSH 連線失敗

**解決方法**：  
1. 檢查防火牆是否允許 port 2201
2. 確認 SSH 使用者有 `sudo` 權限
3. 測試手動連線：
   ```bash
   ssh admin@140.112.170.43 -p 2201
   ```

### 問題 3：使用者已存在

程式會自動跳過已存在的使用者，並記錄警告。

### 問題 4：PDF 附件找不到

確認 `slurm_guide.pdf` 在專案根目錄，或修改 `.env` 中的路徑：
```bash
PDF_GUIDE_PATH=/full/path/to/slurm_guide.pdf
```

---

## 📊 執行範例 / Example Output

```
2025-10-17 15:27:57 - INFO - Starting HPC Account Automation Script
2025-10-17 15:27:57 - INFO - CSV file: applicants.csv
2025-10-17 15:27:57 - INFO - Dry run: False
2025-10-17 15:27:58 - INFO - Processing applicants from applicants.csv

============================================================
Processing: 潘哈哈 (b12901193) - b12901999
============================================================
2025-10-17 15:27:59 - INFO - Connecting to SSH server 140.112.170.43:2201
2025-10-17 15:28:01 - INFO - Creating account for user: b12901999
2025-10-17 15:28:03 - INFO - ✅ Successfully created account: b12901999
2025-10-17 15:28:04 - INFO - Preparing email for b12901999@ntu.edu.tw
2025-10-17 15:28:06 - INFO - 📧 Successfully sent email to b12901999@ntu.edu.tw

============================================================
SUMMARY
============================================================
Total applicants: 1
Accounts created: 1
Accounts failed: 0
Skipped: 0
Emails sent: 1
Emails failed: 0
============================================================
```

---

## 🤝 維護與支援 / Maintenance & Support

**系統管理團隊**  
Email: ntueehpc@googlegroups.com

**問題回報**  
請附上 `logs/` 資料夾中的日誌檔案

---

## 📄 授權 / License

本專案僅供內部使用，請勿外流敏感資訊。

---

## ✨ 更新紀錄 / Changelog

### v1.0.0 (2025-10-17)
- ✅ 初始版本
- ✅ SSH 帳號建立
- ✅ 雙語郵件通知
- ✅ 完整日誌系統
- ✅ Dry run 模式
