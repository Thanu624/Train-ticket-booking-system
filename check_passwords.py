import sys
sys.path.insert(0, 'backend')

from app.config.database import engine
from app.config.security import verify_password, get_password_hash
from sqlalchemy import text

with engine.connect() as conn:
    users = conn.execute(text('SELECT email, password FROM users')).fetchall()

test_cases = [
    ('admin@railbook.com', 'Admin@123'),
    ('pattbhi@railbook.com', 'Pattbhi@123'),
    ('reshma@gmail.com', 'reshma123'),
    ('reshma@gmail.com', 'Reshma@123'),
    ('reshma@gmail.com', '12345678'),
    ('reshma@gmail.com', 'reshma'),
    ('pattabhichenchulakshmi@gmai.com', '12345678'),
    ('pattabhichenchulakshmi@gmai.com', 'Pattabhi@123'),
]

print("Password verification results:")
for email, pwd in test_cases:
    for row in users:
        if row[0] == email:
            result = verify_password(pwd, row[1])
            status = 'OK' if result else 'FAIL'
            print(f"  {status} | {email} / {pwd}")
