#!/usr/bin/env python3
"""
Network diagnostic for SMTP connection issues
"""
import socket
import smtplib
import ssl

SMTP_SERVER = "smtp-mail.outlook.com"
SMTP_PORT = 587

print("=== SMTP Connection Diagnostic ===\n")

# Test 1: DNS Resolution
print("1. Testing DNS resolution...")
try:
    ip = socket.gethostbyname(SMTP_SERVER)
    print(f"   ✅ {SMTP_SERVER} resolves to {ip}")
except Exception as e:
    print(f"   ❌ DNS Error: {e}")
    exit(1)

# Test 2: Port connectivity
print(f"\n2. Testing port {SMTP_PORT} connectivity...")
try:
    sock = socket.create_connection((SMTP_SERVER, SMTP_PORT), timeout=10)
    print(f"   ✅ Port {SMTP_PORT} is accessible")
    sock.close()
except Exception as e:
    print(f"   ❌ Connection Error: {e}")
    exit(1)

# Test 3: SMTP Connection
print(f"\n3. Testing SMTP connection...")
try:
    s = smtplib.SMTP(timeout=10)
    s.connect(SMTP_SERVER, SMTP_PORT)
    print(f"   ✅ SMTP connected")
    code, msg = s.ehlo()
    print(f"   ✅ EHLO successful: {code}")
    s.quit()
except Exception as e:
    print(f"   ❌ SMTP Error: {e}")
    exit(1)

# Test 4: STARTTLS
print(f"\n4. Testing STARTTLS...")
try:
    s = smtplib.SMTP(timeout=10)
    s.connect(SMTP_SERVER, SMTP_PORT)
    s.ehlo()
    if s.has_extn('STARTTLS'):
        print(f"   ✅ Server supports STARTTLS")
        s.starttls()
        print(f"   ✅ STARTTLS successful")
    else:
        print(f"   ❌ Server does not support STARTTLS")
    s.quit()
except Exception as e:
    print(f"   ❌ STARTTLS Error: {e}")
    exit(1)

print("\n=== All tests passed! ===")
print("SMTP connection should work fine.")
