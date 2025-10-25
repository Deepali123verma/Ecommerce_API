# test_connection.py (inside app folder)
from database import engine  # <-- remove 'app.'

try:
    connection = engine.connect()
    print("✅ Connection successful!")
    connection.close()
except Exception as e:
    print("❌ Connection failed!")
    print(e)
