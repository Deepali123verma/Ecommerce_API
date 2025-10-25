# test_decrypt.py
from app.utils import encrypt_data, decrypt_data

def test_encryption():
    original_text = "This is a secret message from project!"
    encrypted_text = encrypt_data(original_text)
    decrypted_text = decrypt_data(encrypted_text)

    print("Original Text:", original_text)
    print("Encrypted Text:", encrypted_text)
    print("Decrypted Text:", decrypted_text)

    assert original_text == decrypted_text, "Decrypted text does not match original!"

if __name__ == "__main__":
    test_encryption()
    print("✅ Encryption & decryption test passed!")
