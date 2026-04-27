"""
generate_hashes.py — Run this ONCE to create correct bcrypt hashes
then update your seed.sql or run the UPDATE queries it prints.

Usage:
    python generate_hashes.py
"""
import bcrypt


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


passwords = {
    'admin':      'admin123',
    'dr_ahmed':   'admin123',
    'dr_fatima':  'admin123',
    'dr_omar':    'admin123',
    'nurse_sara': 'admin123',
    'nurse_ali':  'admin123',
    'billing1':   'admin123',
}

print("-- Run these UPDATE statements in SSMS after running seed.sql:\n")
for username, password in passwords.items():
    h = hash_password(password)
    print(f"UPDATE Users SET password_hash = '{h}' WHERE username = '{username}';")

print("\nGO")
print("\n-- Done!")
