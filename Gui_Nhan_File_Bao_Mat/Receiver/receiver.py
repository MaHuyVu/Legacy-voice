import os
import socket
import base64
import json
import time

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, DES
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA512
from Crypto.Util.Padding import unpad

HOST = "127.0.0.1"
PORT = 65432

OUTPUT_FILE = "received_voice.wav"

# =====================================
# Tạo khóa RSA cho Receiver
# =====================================

if not os.path.exists("receiver_private.pem"):

    key = RSA.generate(2048)

    with open("receiver_private.pem", "wb") as f:
        f.write(key.export_key())

    with open("receiver_public.pem", "wb") as f:
        f.write(key.publickey().export_key())

    print("Receiver: Đã tạo cặp khóa RSA.")

    time.sleep(2)

# =====================================
# Chờ Sender kết nối
# =====================================

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.bind((HOST, PORT))

    s.listen(1)

    print(f"Receiver: Đợi kết nối tại {HOST}:{PORT}...")

    conn, addr = s.accept()

    with conn:

        print("Receiver: Đã kết nối với", addr)

        time.sleep(2)

        # -----------------------------
        # Handshake
        # -----------------------------

        print("Receiver: Đang Handshake...")

        hello = conn.recv(5)

        if hello != b"HELLO":

            print("Handshake lỗi")

            exit()

        conn.sendall(b"READY")

        print("Receiver: READY")

        time.sleep(2)

        # -----------------------------
        # Gửi Public Key
        # -----------------------------

        pub = open(
            "receiver_public.pem",
            "rb"
        ).read()

        conn.sendall(

            len(pub).to_bytes(4, "big")

            + pub

        )

        print("Receiver: Đã gửi Public Key")

        time.sleep(2)

        # -----------------------------
        # -----------------------------
        # Nhận Packet
        # -----------------------------

        size = int.from_bytes(
            conn.recv(4),
            "big"
        )

        packet = b""

        while len(packet) < size:

            chunk = conn.recv(
                min(4096, size - len(packet))
            )

            if not chunk:
                break

            packet += chunk

        print(f"Receiver: Đã nhận {len(packet)}/{size} bytes")

        data = json.loads(packet)

        esk = base64.b64decode(data["esk"])
        sig = base64.b64decode(data["sig"])
        iv = base64.b64decode(data["iv"])
        cipher = base64.b64decode(data["cipher"])

        metadata = data["metadata"]
        hash_sender = data["hash"]

        print("Receiver: Đã nhận dữ liệu")

        time.sleep(2)

        # -----------------------------
        # Load RSA Keys
        # -----------------------------

        private_key = RSA.import_key(
            open(
                "receiver_private.pem",
                "rb"
            ).read()
        )

        sender_public = RSA.import_key(
            open(
                "sender_public.pem",
                "rb"
            ).read()
        )

        # -----------------------------
        # Verify Signature
        # -----------------------------

        try:

            h = SHA512.new(

                metadata.encode()

            )

            pkcs1_15.new(

                sender_public

            ).verify(

                h,

                sig

            )

            print("Receiver: Signature hợp lệ")

        except Exception:

            print("Receiver: Signature lỗi")

            conn.sendall(b"NACK")

            exit()

        time.sleep(2)

                # -----------------------------
        # Giải mã Session Key
        # -----------------------------

        session_key = PKCS1_OAEP.new(

            private_key

        ).decrypt(

            esk

        )

        print("Receiver: Đã giải mã SessionKey")

        time.sleep(2)

        # -----------------------------
        # Kiểm tra Hash
        # -----------------------------

        hash_receiver = SHA512.new(

            cipher

        ).hexdigest()

        if hash_receiver != hash_sender:

            print("===================================")
            print("Receiver: HASH KHÔNG HỢP LỆ")
            print("===================================")

            conn.sendall(b"NACK")

            exit()

        print("Receiver: Hash hợp lệ")

        time.sleep(2)

        # -----------------------------
        # DES Decrypt
        # -----------------------------

        plaintext = DES.new(

            session_key,

            DES.MODE_CBC,

            iv

        ).decrypt(

            cipher

        )

        plaintext = unpad(

            plaintext,

            DES.block_size

        )
        print("Receiver: DES Decrypt thành công")

        print(f"Cipher length = {len(cipher)} bytes")
        print(f"Plaintext length = {len(plaintext)} bytes")

        time.sleep(2)

        

        # -----------------------------
        # Lưu file âm thanh
        # -----------------------------

        with open(

            OUTPUT_FILE,

            "wb"

        ) as f:

            f.write(

                plaintext

            )

        print(f"Receiver: Đã lưu {OUTPUT_FILE}")

        time.sleep(2)

        # -----------------------------
        # Phát âm thanh (Windows)
        # -----------------------------

        try:

            import winsound

            winsound.PlaySound(

                OUTPUT_FILE,

                winsound.SND_FILENAME

            )

            print("Receiver: Đang phát âm thanh...")

        except Exception as e:

            print("Receiver: Không thể phát âm thanh:", e)

        # -----------------------------
        # Gửi ACK
        # -----------------------------

        conn.sendall(

            b"ACK"

        )

        print("===================================")
        print("Receiver: Gửi ACK thành công")
        print("===================================")

        time.sleep(2)

print("\nReceiver kết thúc.")