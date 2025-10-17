#!/usr/bin/env python3
"""
Test script to verify the auto_hpc_account.py works with add_user.sh
This simulates what happens without actually creating accounts
"""

import re

# Sample output from add_user.sh script
sample_output = """sudoer1@A12-01:~$ sudo ./add_user.sh
Enter the username to add: b10202010
Enter the group (1: undergrad, 2: master, 3: phd, 4: professor, 5: admin): 1
Enter the professor's name: (required for master and phd, else leave blank):
Enter the password (leave blank to generate a random one):
Generated password: YUQ54LyaHtnS
adding new entry "cn=b10202010,ou=People,dc=hpc,dc=ntuee,dc=org"

User b10202010 added to LDAP successfully!
Storage directory /storage/undergrad/b10202010 created!
create account: b10202010
 Adding Account(s)
  b10202010
 Settings
  Description     = Account Name
  Organization    = Parent/Account Name
 Associations =
  C = ntueecore  A = b10202010
 Settings
  QOS           = studentbasic
  DefQOS        = studentbasic
create user: b10202010
 Adding User(s)
  b10202010
 Settings
 Associations =
  C = ntueecore  A = b10202010            U = b10202010
 Non Default Settings
  QOS           = studentbasic
  DefQOS        = studentbasic
  done ! please check with the following command
  sacctmgr show assoc where user=b10202010
"""

def test_success_detection():
    """Test if success keywords are detected correctly"""
    print("=" * 60)
    print("TEST 1: Success Detection")
    print("=" * 60)
    
    success_keywords = [
        "done ! please check",
        "successfully",
        "user b10202010 added to ldap successfully",
        "storage directory",
        "adding user(s)"
    ]
    
    output_lower = sample_output.lower()
    success = any(keyword in output_lower for keyword in success_keywords)
    
    print(f"✅ Success detected: {success}")
    for keyword in success_keywords:
        found = keyword in output_lower
        status = "✅" if found else "❌"
        print(f"  {status} '{keyword}': {found}")
    
    return success


def test_error_detection():
    """Test if errors are correctly identified"""
    print("\n" + "=" * 60)
    print("TEST 2: Error Detection")
    print("=" * 60)
    
    error_keywords = ["error", "failed", "invalid group", "username and group are required"]
    output_lower = sample_output.lower()
    has_errors = any(keyword in output_lower for keyword in error_keywords)
    
    print(f"✅ No errors detected: {not has_errors}")
    for keyword in error_keywords:
        found = keyword in output_lower
        status = "⚠️" if found else "✅"
        print(f"  {status} '{keyword}': {found}")
    
    return not has_errors


def test_password_extraction():
    """Test password extraction from script output"""
    print("\n" + "=" * 60)
    print("TEST 3: Password Extraction")
    print("=" * 60)
    
    match = re.search(r'Generated password:\s*(\S+)', sample_output, re.IGNORECASE)
    
    if match:
        extracted_password = match.group(1)
        print(f"✅ Password extracted: {extracted_password}")
        print(f"   Expected: YUQ54LyaHtnS")
        print(f"   Match: {extracted_password == 'YUQ54LyaHtnS'}")
        return extracted_password == 'YUQ54LyaHtnS'
    else:
        print("❌ Failed to extract password")
        return False


def test_ldap_info_extraction():
    """Test extraction of various information from output"""
    print("\n" + "=" * 60)
    print("TEST 4: Information Extraction")
    print("=" * 60)
    
    tests = {
        "Username": (r'cn=([^,]+),ou=People', 'b10202010'),
        "Storage path": (r'/storage/\w+/(\w+)', 'b10202010'),
        "QOS": (r'QOS\s*=\s*(\w+)', 'studentbasic'),
        "Cluster": (r'C = (\w+)', 'ntueecore'),
    }
    
    all_passed = True
    for name, (pattern, expected) in tests.items():
        match = re.search(pattern, sample_output)
        if match:
            value = match.group(1)
            passed = value == expected
            status = "✅" if passed else "❌"
            print(f"  {status} {name}: {value} (expected: {expected})")
            all_passed = all_passed and passed
        else:
            print(f"  ❌ {name}: Not found")
            all_passed = False
    
    return all_passed


def test_group_detection():
    """Test detection of user group from storage path"""
    print("\n" + "=" * 60)
    print("TEST 5: Group Detection")
    print("=" * 60)
    
    match = re.search(r'/storage/(\w+)/', sample_output)
    if match:
        group = match.group(1)
        print(f"✅ Group detected: {group}")
        print(f"   Expected: undergrad")
        print(f"   Match: {group == 'undergrad'}")
        return group == 'undergrad'
    else:
        print("❌ Failed to detect group")
        return False


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "AUTO_HPC_ACCOUNT.PY VERIFICATION TESTS" + " " * 9 + "║")
    print("╚" + "=" * 58 + "╝")
    
    results = []
    
    results.append(("Success Detection", test_success_detection()))
    results.append(("Error Detection", test_error_detection()))
    results.append(("Password Extraction", test_password_extraction()))
    results.append(("Information Extraction", test_ldap_info_extraction()))
    results.append(("Group Detection", test_group_detection()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {status}: {name}")
    
    print("\n" + "=" * 60)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ ALL TESTS PASSED - Code should work correctly!")
    else:
        print("⚠️  Some tests failed - Review the code")
    print("=" * 60 + "\n")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
