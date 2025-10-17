# HPC Account Automation

Automatically create HPC user accounts and send notification emails from Google Forms data.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

**Note:** For Gmail, generate an App Password at https://myaccount.google.com/apppasswords

### 3. Run the Script

**Test mode (no actual changes):**
```bash
python auto_hpc_account.py applicants.csv --dry-run
```

**Create accounts and send emails:**
```bash
python auto_hpc_account.py
```
reads ```applicants.csv```
## What It Does

1. ✅ Reads Google Forms CSV data
2. ✅ Creates accounts via SSH on remote server
3. ✅ Sends bilingual email notification (Chinese + English)
4. ✅ Attaches Slurm user guides (PDF)
5. ✅ CC's HPC admin team
