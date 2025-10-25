import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import crud, schemas, utils, models
from app.database import Base, get_db

# Load environment variables from .env
load_dotenv()

# ---------------- DATABASE SETUP ----------------
DATABASE_URL = os.getenv("DATABASE_URL")

# If running locally and DATABASE_URL contains 'db', replace with localhost
if "db" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("db", "localhost")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables (if not exist)
Base.metadata.create_all(bind=engine)

# ---------------- TEST ----------------
def test_security():
    db = SessionLocal()

    print("==== TESTING PASSWORD HASHING ====")
    plain_password = "mypassword123"
    hashed = utils.hash_password(plain_password)
    print("Plain Password:", plain_password)
    print("Hashed Password:", hashed)
    print("Verify Correct:", utils.verify_password(plain_password, hashed))
    print("Verify Wrong:", utils.verify_password("wrongpass", hashed))

    print("\n==== TESTING EMAIL ENCRYPTION ====")
    original_email = "deepali@example.com"
    encrypted = utils.encrypt_data(original_email)
    decrypted = utils.decrypt_data(encrypted)
    print("Original Email:", original_email)
    print("Encrypted Email:", encrypted)
    print("Decrypted Email:", decrypted)

    print("\n==== TESTING CRUD OPERATIONS ====")
    # Create user
    new_user = schemas.UserCreate(name="Deepali", email=encrypted, password=hashed)
    user = crud.create_user(db, new_user)
    print("Created User ID:", user.id)

    # Fetch user
    fetched_user = crud.get_user(db, user.id)
    print("Fetched User Name:", fetched_user.name)
    print("Fetched User Email (Encrypted):", fetched_user.email)
    print("Decrypted Email:", utils.decrypt_data(fetched_user.email))

    # Clean up
    crud.delete_user(db, user.id)
    print("User deleted successfully")

    db.close()


if __name__ == "__main__":
    test_security()
