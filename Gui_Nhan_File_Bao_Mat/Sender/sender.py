import os
import socket
import base64
import json
import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, DES
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

# Địa chỉ và cổng kết nối đến Receiver
HOST = '127.0.0.1'
PORT = 65432

# File âm thanh cần gửi
FILE_NAME = "voice.wav.wav"

# ==========================
# Tạo khóa RSA cho Sender
# ==========================
if not os.path.exists('sender_private.pem'):
    key = RSA.generate(2048)

    with open('sender_private.pem', 'wb') as f:
        f.write(key.export_key())

    with open('sender_public.pem', 'wb') as f:
        f.write(key.publickey().export_key())

    print("Sender: Đã tạo cặp khóa RSA.")
    time.sleep(2)

# ==========================
# Kết nối Receiver
# ==========================
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.connect((HOST, PORT))

    print(f"Sender: Đã kết nối tới {HOST}:{PORT}")
    time.sleep(2)

    # -----------------------
    # BƯỚC 1: HANDSHAKE
    # -----------------------

    print("Sender: Đang thực hiện BƯỚC 1 - Handshake...")

    s.sendall(b"HELLO")

    print("Sender: Gửi HELLO")
    time.sleep(2)

    data = s.recv(5)

    if data == b"READY":

        print("Sender: Nhận READY từ Receiver")
        time.sleep(2)

    else:

        print("Sender: Handshake thất bại")
        exit()

    # -----------------------
    # Nhận Public Key Receiver
    # -----------------------

    print("Sender: Đang nhận PublicKey...")

    size = int.from_bytes(s.recv(4), "big")

    pub_R_data = s.recv(size)

    with open("receiver_public.pem", "wb") as f:
        f.write(pub_R_data)

    print("Sender: Đã nhận PublicKey Receiver")
    time.sleep(2)

    # Load khóa

    pub_R = RSA.import_key(pub_R_data)

    priv_S = RSA.import_key(
        open("sender_private.pem", "rb").read()
    )

    # -----------------------
    # Metadata
    # -----------------------

    timestamp = int(time.time())

    metadata = f"{FILE_NAME}|{timestamp}"

    print("Sender: Metadata =", metadata)

    # Ký metadata

    h_meta = SHA512.new(metadata.encode())

    signature = pkcs1_15.new(priv_S).sign(h_meta)

    # -----------------------
    # Tạo Session Key DES
    # -----------------------

    session_key = get_random_bytes(8)

    encrypted_session_key = PKCS1_OAEP.new(pub_R).encrypt(session_key)

    print("Sender: SessionKey tạo thành công")

    time.sleep(2)

    # -----------------------
    # Đọc file âm thanh
    # -----------------------

    if not os.path.exists(FILE_NAME):

        print(f"Lỗi: Không tìm thấy {FILE_NAME}")

        exit()

    with open(FILE_NAME, "rb") as f:

        plaintext = f.read()

    print(f"Sender: Đọc {len(plaintext)} bytes")

    time.sleep(2)

    # -----------------------
    # DES Encrypt
    # -----------------------

    iv = get_random_bytes(8)

    cipher = DES.new(
        session_key,
        DES.MODE_CBC,
        iv
    ).encrypt(
        pad(
            plaintext,
            DES.block_size
        )
    )

    print("Sender: DES Encrypt thành công")

    time.sleep(2)
        # -----------------------
    # SHA512 Hash
    # -----------------------

    hash_cipher = SHA512.new(cipher).hexdigest()

    print("Sender: Hash =", hash_cipher)

    time.sleep(2)

    # -----------------------
    # Đóng gói JSON
    # -----------------------

    packet = {

        "esk": base64.b64encode(
            encrypted_session_key
        ).decode(),

        "sig": base64.b64encode(
            signature
        ).decode(),

        "metadata": metadata,

        "iv": base64.b64encode(
            iv
        ).decode(),

        "cipher": base64.b64encode(
            cipher
        ).decode(),

        "hash": hash_cipher

    }

    packet = json.dumps(packet).encode()

    # -----------------------
    # Gửi dữ liệu
    # -----------------------

    print("Sender: Đang gửi dữ liệu...")

    s.sendall(

        len(packet).to_bytes(4, "big")

        + packet

    )

    print("Sender: Đã gửi thành công")

    time.sleep(2)

    # -----------------------
    # Nhận ACK
    # -----------------------

    response = s.recv(4)

    if response == b"ACK":

        print("===================================")
        print("Sender: Receiver xác nhận thành công")
        print("===================================")

    elif response == b"NACK":

        print("===================================")
        print("Sender: Receiver từ chối dữ liệu")
        print("===================================")

    else:

        print("Sender: Phản hồi không xác định")

    time.sleep(2)

print("\nSender kết thúc.")