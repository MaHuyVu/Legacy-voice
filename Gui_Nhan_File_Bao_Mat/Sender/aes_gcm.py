from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Tạo khóa AES 256-bit
def generate_key():
    return get_random_bytes(32)

# Mã hóa AES-GCM
def encrypt_file(data, key):
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data)

    return {
        "nonce": cipher.nonce,
        "ciphertext": ciphertext,
        "tag": tag
    }

# Giải mã AES-GCM
def decrypt_file(ciphertext, key, nonce, tag):
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext