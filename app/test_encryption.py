from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

# Initialize Fernet
fernet = Fernet(ENCRYPTION_KEY)

# Original text to encrypt
original_text = "This is a secret message!"
print("Original Text:", original_text)

# Encrypt
encrypted_text = fernet.encrypt(original_text.encode())
print("Encrypted Text:", encrypted_text)

# Decrypt
decrypted_text = fernet.decrypt(encrypted_text).decode()
print("Decrypted Text:", decrypted_text)
