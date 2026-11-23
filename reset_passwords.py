"""
Reset ALL user passwords to a simple default for testing.
Run this whenever you need to regain access.
"""
import sys
sys.path.insert(0, 'backend')

from app.config.database import engine
from app.config.security import get_password_hash
from sqlalchemy import text

DEFAULT_PASSWORD = "Test@1234"
hashed = get_password_hash(DEFAULT_PASSWORD)

with engine.begin() as conn:
    result = conn.execute(text("SELECT id, email FROM users"))
    users = result.fetchall()
    
    for user in users:
        conn.execute(
            text("UPDATE users SET password = :pwd WHERE id = :uid"),
            {"pwd": hashed, "uid": user[0]}
        )
        print(f"  Reset: {user[1]} -> {DEFAULT_PASSWORD}")

print(f"\nAll passwords reset to: {DEFAULT_PASSWORD}")
print("You can now login with any account using this password.")
