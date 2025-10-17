#!/usr/bin/env python3
"""
HPC Account Automation Script
Automatically creates HPC user accounts via SSH and sends notification emails
"""

import csv
import os
import secrets
import string
import smtplib
import logging
from datetime import datetime
from pathlib import Path
import paramiko
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


# ====== Setup Logging ======
def setup_logging():
    """Configure logging to both file and console"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"hpc_account_{timestamp}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


# Initialize logger
logger = setup_logging()

# ====== Load Environment Variables ======
load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

SSH_HOST = os.getenv("SSH_HOST")
SSH_PORT = int(os.getenv("SSH_PORT", "2201"))
SSH_USER = os.getenv("SSH_USER")
SSH_PASS = os.getenv("SSH_PASS")
SSH_KEY_FILE = os.getenv("SSH_KEY_FILE")  # Optional: use SSH key instead of password
ADD_USER_SCRIPT_PATH = os.getenv("ADD_USER_SCRIPT_PATH", "/home/sudoer1/add_user.sh")

PDF_GUIDE_PATH = os.getenv("PDF_GUIDE_PATH", "Slurm_User_Guide.pdf")
PDF_GUIDE_PATH_2 = os.getenv("PDF_GUIDE_PATH_2", "Slurm_User_Guide_EN.pdf")  # Optional second PDF


# ====== Generate Secure Password ======
def generate_password(length=8):
    """Generate a secure random password"""
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    logger.debug(f"Generated password of length {length}")
    return password


# ====== SSH Account Creation ======
def create_account(username, group_number="1", professor="", custom_password=""):
    """
    Create a user account on the remote HPC server via SSH using add_user.sh script
    
    Args:
        username (str): The username to create
        group_number (str): Group number (1: undergrad, 2: master, 3: phd, 4: professor, 5: admin)
        professor (str): Professor's name (required for master and phd)
        custom_password (str): Custom password (if empty, will be auto-generated)
        
    Returns:
        str: The generated/used password, or None if failed
    """
    password = ""
    
    try:
        logger.info(f"Connecting to SSH server {SSH_HOST}:{SSH_PORT}")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect using password or key
        if SSH_KEY_FILE and os.path.exists(SSH_KEY_FILE):
            ssh.connect(
                SSH_HOST, 
                port=SSH_PORT, 
                username=SSH_USER, 
                key_filename=SSH_KEY_FILE
            )
        else:
            ssh.connect(
                SSH_HOST, 
                port=SSH_PORT, 
                username=SSH_USER, 
                password=SSH_PASS
            )
        
        logger.info(f"Creating account for user: {username} (group: {group_number}, professor: {professor or 'N/A'})")
        
        # Check if user already exists in LDAP
        check_cmd = f"ldapsearch -x -H ldap://192.168.110.21 -D 'cn=Manager,dc=hpc,dc=ntuee,dc=org' -w 'ntuee123' -b 'ou=People,dc=hpc,dc=ntuee,dc=org' '(cn={username})'"
        stdin, stdout, stderr = ssh.exec_command(check_cmd)
        output = stdout.read().decode()
        
        if f"cn: {username}" in output:
            logger.warning(f"User {username} already exists in LDAP. Skipping creation.")
            ssh.close()
            return None
        
        # Prepare input for add_user.sh script
        script_input = f"{username}\n{group_number}\n{professor}\n{password}\n"
        
        # Execute the add_user.sh script with sudo
        logger.info(f"Executing add_user.sh script for {username}...")
        command = f"sudo {ADD_USER_SCRIPT_PATH}"
        
        # Use invoke_shell for interactive script
        channel = ssh.invoke_shell()
        channel.send(command + "\n")
        
        import time
        time.sleep(3)  # Wait for sudo password prompt
        
        channel.send(f"{SSH_PASS}\n")
        time.sleep(3)

        channel.send(f"{username}\n")
        time.sleep(1)
        channel.send(f"{group_number}\n")
        time.sleep(1) 
        channel.send(f"{professor}\n")
        time.sleep(1)
        channel.send(f"\n")
        time.sleep(1)

        # Collect all output
        output = ""
        max_attempts = 5
        for attempt in range(max_attempts):
            if channel.recv_ready():
                chunk = channel.recv(8192).decode('utf-8', errors='ignore')
                output += chunk
                time.sleep(0.5)
            else:
                break
        
        # Log the full output
        logger.info(f"Script output:\n{output}")
        
        # Check for success indicators in the output
        success_keywords = [
            "done ! please check",
            "successfully",
            f"user {username} added to ldap successfully",
            "storage directory",
            "adding user(s)"
        ]
        
        output_lower = output.lower()
        success = any(keyword in output_lower for keyword in success_keywords)
        
        # Also check if there are critical errors
        error_keywords = ["error", "failed", "invalid group", "username and group are required"]
        has_errors = any(keyword in output_lower for keyword in error_keywords)
        
        if success and not has_errors:
            logger.info(f"✅ Successfully created account: {username}")
            
            # Try to extract generated password from script output if we left it blank
            if not custom_password and "generated password:" in output_lower:
                import re
                match = re.search(r'Generated password:\s*(\S+)', output, re.IGNORECASE)
                if match:
                    extracted_password = match.group(1)
                    logger.info(f"Extracted generated password from script output")
                    ssh.close()
                    return extracted_password
            
            ssh.close()
            return password
        else:
            logger.error(f"Script execution may have failed. Check logs for details.")
            if has_errors:
                logger.error(f"Errors detected in output")
            ssh.close()
            return None
        
    except paramiko.AuthenticationException:
        logger.error("SSH authentication failed. Check credentials.")
        return None
    except paramiko.SSHException as e:
        logger.error(f"SSH connection error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error creating account: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return None


# ====== Send Email Notification ======
def send_email(recipient, username, password, name="User"):
    """
    Send account creation notification email to the applicant
    
    Args:
        recipient (str): Email address of the recipient
        username (str): HPC username
        password (str): Generated password
        name (str): Name of the applicant
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        logger.info(f"Preparing email for {recipient}")
        
        # Validate email addresses
        if not recipient or "@" not in recipient:
            logger.error(f"Invalid recipient email address: {recipient}")
            return False
        
        if not SMTP_USER or "@" not in SMTP_USER:
            logger.error(f"Invalid SMTP_USER email address: {SMTP_USER}")
            return False
        
        msg = MIMEMultipart()
        msg["From"] = f"HPC Admin <{SMTP_USER}>"  # Properly formatted From header
        msg["To"] = recipient
        msg["Subject"] = "HPC 帳號建立通知 / HPC Account Created"
        
        # Bilingual email body (Chinese + English)
        body = f"""您好 {name}，

您申請的高效能運算（HPC）平台帳號已經建立，相關資訊如下：

帳號 (Username)：{username}
預設密碼 (Initial Password)：{password}

請於首次登入後立即修改密碼，以確保帳號安全。

登入方式：
  SSH：ssh {username}@{SSH_HOST} -p {SSH_PORT}

為協助您熟悉系統操作，本信附上 Slurm 簡易使用說明 PDF，供您參考。

若有任何使用上的問題，請聯繫系統管理團隊：
  ntueehpc@googlegroups.com

感謝您的使用，祝研究與學習順利。

HPC 系統管理團隊

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Dear {name},

Your High-Performance Computing (HPC) platform account has been successfully created.

Please find the account information below:

Username: {username}
Initial Password: {password}

Please change your password immediately after your first login for security.

Login methods:
  SSH: ssh {username}@{SSH_HOST} -p {SSH_PORT}

To help you get started, we have attached a Slurm User Guide (PDF).

For any questions or technical support, please contact the system administration team:
  ntueehpc@googlegroups.com

Thank you for using our HPC platform. We wish you success in your research and studies.

HPC System Administration Team
"""
        
        msg.attach(MIMEText(body, "plain", "utf-8"))
        
        # Attach PDF guide if it exists
        if os.path.exists(PDF_GUIDE_PATH):
            with open(PDF_GUIDE_PATH, "rb") as f:
                pdf = MIMEApplication(f.read(), _subtype="pdf")
                pdf.add_header("Content-Disposition", "attachment", filename="Slurm_User_Guide.pdf")
                msg.attach(pdf)
            logger.debug(f"Attached PDF guide: {PDF_GUIDE_PATH}")
        else:
            logger.warning(f"PDF guide not found at {PDF_GUIDE_PATH}, skipping attachment")
        
        # Attach second PDF guide if it exists
        if PDF_GUIDE_PATH_2 and os.path.exists(PDF_GUIDE_PATH_2):
            with open(PDF_GUIDE_PATH_2, "rb") as f:
                pdf2 = MIMEApplication(f.read(), _subtype="pdf")
                # Extract filename from path
                filename2 = os.path.basename(PDF_GUIDE_PATH_2)
                pdf2.add_header("Content-Disposition", "attachment", filename=filename2)
                msg.attach(pdf2)
            logger.debug(f"Attached second PDF guide: {PDF_GUIDE_PATH_2}")
        
        # Send email via SMTP
        logger.info(f"Connecting to SMTP server {SMTP_SERVER}:{SMTP_PORT}")
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as smtp:
            smtp.set_debuglevel(0)  # Set to 1 for verbose debug output
            logger.debug("Starting TLS...")
            smtp.starttls()
            logger.debug("Logging in...")
            smtp.login(SMTP_USER, SMTP_PASS)
            logger.debug("Sending message...")
            smtp.send_message(msg)
        
        logger.info(f"📧 Successfully sent email to {recipient}")
        return True
        
    except smtplib.SMTPAuthenticationError:
        logger.error("SMTP authentication failed. Check email credentials.")
        return False
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error sending email: {e}")
        return False


# ====== Convert User Type to Group Number ======
def convert_user_type_to_group(user_type):
    """
    Convert Chinese user type from Google Form to group number
    
    Args:
        user_type (str): User type in Chinese (大學部學生, 碩士班學生, etc.)
        
    Returns:
        str: Group number (1-5)
    """
    user_type = user_type.strip()
    
    # Mapping from Chinese to group numbers
    type_mapping = {
        "大學部學生": "1",
        "大學部": "1",
        "undergrad": "1",
        "undergraduate": "1",
        "碩士班學生": "2",
        "碩士生": "2",
        "碩士": "2",
        "master": "2",
        "博士班學生": "3",
        "博士生": "3",
        "博士": "3",
        "phd": "3",
        "教授": "4",
        "professor": "4",
        "管理員": "5",
        "admin": "5",
    }
    
    # Try exact match first
    if user_type in type_mapping:
        return type_mapping[user_type]
    
    # Try case-insensitive match
    user_type_lower = user_type.lower()
    for key, value in type_mapping.items():
        if key.lower() == user_type_lower:
            return value
    
    # Default to undergrad if not found
    logger.warning(f"Unknown user type '{user_type}', defaulting to 1 (undergrad)")
    return "1"


# ====== Process Applicants from CSV ======
def process_applicants(csv_file="applicants.csv", dry_run=False):
    """
    Process all applicants from CSV file
    
    Args:
        csv_file (str): Path to CSV file with applicant data
        dry_run (bool): If True, only log actions without executing
        
    Returns:
        dict: Statistics of processed accounts
    """
    stats = {
        "total": 0,
        "created": 0,
        "failed": 0,
        "skipped": 0,
        "emails_sent": 0,
        "emails_failed": 0
    }
    
    if not os.path.exists(csv_file):
        logger.error(f"CSV file not found: {csv_file}")
        return stats
    
    logger.info(f"{'[DRY RUN] ' if dry_run else ''}Processing applicants from {csv_file}")
    
    try:
        with open(csv_file, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                stats["total"] += 1
                
                # Map Google Form columns to internal format
                # Try both old format and new Google Form format
                email = row.get("email_ntu", "").strip() or row.get("email", "").strip()
                username = row.get("student_id", "").strip() or row.get("username", "").strip()
                name = row.get("name", "User").strip()
                student_id = row.get("student_id", "").strip()
                
                # Handle user_type from Google Form (需要轉換成group number)
                user_type = row.get("user_type", "").strip()
                group = row.get("group", "").strip()
                
                # Convert user_type to group if group is not provided
                if not group and user_type:
                    group = convert_user_type_to_group(user_type)
                elif not group:
                    group = "1"  # Default to undergrad
                
                professor = row.get("professor", "").strip()
                custom_password = row.get("password", "").strip()  # Optional custom password
                
                if not email or not username:
                    logger.warning(f"Skipping row {stats['total']}: missing email or username")
                    logger.warning(f"  Email: '{email}', Username: '{username}'")
                    stats["skipped"] += 1
                    continue
                
                # Validate group number
                if group not in ['1', '2', '3', '4', '5']:
                    logger.warning(f"Invalid group '{group}' for {username}, defaulting to 1 (undergrad)")
                    group = '1'
                
                # Check professor requirement for master/phd
                if group in ['2', '3'] and not professor:
                    logger.warning(f"Professor name required for master/phd student {username}, skipping")
                    stats["skipped"] += 1
                    continue
                
                logger.info(f"\n{'='*60}")
                logger.info(f"Processing: {name} ({student_id}) - {username}")
                logger.info(f"Email: {email}")
                logger.info(f"Group: {group} ({'undergrad' if group=='1' else 'master' if group=='2' else 'phd' if group=='3' else 'professor' if group=='4' else 'admin'})")
                if professor:
                    logger.info(f"Professor: {professor}")
                logger.info(f"{'='*60}")
                
                if dry_run:
                    logger.info(f"[DRY RUN] Would create account for {username} (group: {group})")
                    logger.info(f"[DRY RUN] Would send email to {email}")
                    stats["created"] += 1
                    stats["emails_sent"] += 1
                    continue
                
                # Create account using add_user.sh script
                password = create_account(username, group, professor, custom_password)
                
                if password is None:
                    logger.error(f"Failed to create account for {username}")
                    stats["failed"] += 1
                    continue
                
                stats["created"] += 1
                
                # Send notification email
                if send_email(email, username, password, name):
                    stats["emails_sent"] += 1
                else:
                    stats["emails_failed"] += 1
                    logger.warning(f"Account created but email failed for {username}")
        
        logger.info(f"\n{'='*60}")
        logger.info("SUMMARY")
        logger.info(f"{'='*60}")
        logger.info(f"Total applicants: {stats['total']}")
        logger.info(f"Accounts created: {stats['created']}")
        logger.info(f"Accounts failed: {stats['failed']}")
        logger.info(f"Skipped: {stats['skipped']}")
        logger.info(f"Emails sent: {stats['emails_sent']}")
        logger.info(f"Emails failed: {stats['emails_failed']}")
        logger.info(f"{'='*60}\n")
        
    except Exception as e:
        logger.error(f"Error processing CSV file: {e}")
    
    return stats


# ====== Main Entry Point ======
def main():
    """Main function to run the HPC account automation"""
    import argparse
    
    parser = argparse.ArgumentParser(description="HPC Account Automation Script")
    parser.add_argument(
        "--csv", 
        default="applicants.csv", 
        help="Path to CSV file with applicant data"
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true", 
        help="Simulate without creating accounts or sending emails"
    )
    
    args = parser.parse_args()
    
    logger.info("Starting HPC Account Automation Script")
    logger.info(f"CSV file: {args.csv}")
    logger.info(f"Dry run: {args.dry_run}")
    
    # Validate environment variables
    required_vars = ["SMTP_SERVER", "SMTP_USER", "SMTP_PASS", "SSH_HOST", "SSH_USER"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please check your .env file")
        return
    
    # Process applicants
    stats = process_applicants(args.csv, args.dry_run)
    
    logger.info("Script completed successfully")


if __name__ == "__main__":
    main()
