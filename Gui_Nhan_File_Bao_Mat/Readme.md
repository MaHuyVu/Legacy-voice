# 🎤 Đề tài 19: Legacy Voice Encryption Migration
## Ứng dụng bảo mật tin nhắn âm thanh với DES (Legacy), AES-GCM và xác thực RSA

![Python](https://img.shields.io/badge/Python-3.10-blue)
![PyCryptodome](https://img.shields.io/badge/PyCryptodome-required-orange)
![Socket](https://img.shields.io/badge/TCP-Socket-green)

---

# 📌 Giới thiệu

Đây là đồ án môn **AN TOAN BẢO MẬT THONG TIN**.

Chương trình mô phỏng quá trình **nâng cấp một hệ thống gửi tin nhắn âm thanh cũ** sử dụng thuật toán **DES** sang hệ thống bảo mật hiện đại sử dụng **AES-GCM** kết hợp **RSA Digital Signature** nhằm tăng cường tính bảo mật và khả năng phát hiện dữ liệu bị chỉnh sửa.

---

# 🎯 Mục tiêu

Hệ thống thực hiện các chức năng sau:

- Gửi và nhận tin nhắn âm thanh.
- Mã hóa âm thanh bằng **DES** (Legacy Mode).
- Mã hóa âm thanh bằng **AES-GCM** (Modern Mode).
- Xác thực người gửi bằng **RSA Digital Signature**.
- Kiểm tra tính toàn vẹn dữ liệu.
- Phát hiện dữ liệu bị chỉnh sửa.
- So sánh hiệu năng giữa DES và AES-GCM.

---

# 🔐 Các chức năng chính

## Legacy Mode

- Mã hóa bằng DES.
- Xác thực RSA.
- Kiểm tra SHA-512.
- Hỗ trợ các hệ thống cũ.

> ⚠ **Cảnh báo:** DES đã lỗi thời và chỉ sử dụng nhằm đảm bảo khả năng tương thích với hệ thống cũ.

---

## Modern Mode

- Mã hóa AES-256-GCM.
- Xác thực RSA.
- Phát hiện chỉnh sửa dữ liệu (Tamper Detection).
- Bảo vệ Metadata.
- Tự động kiểm tra tính toàn vẹn dữ liệu.

---

# 🏗 Kiến trúc hệ thống

```text
                 Sender
                    │
          Ghi âm / Chọn file âm thanh
                    │
          Ký số bằng RSA
                    │
      DES (Legacy) hoặc AES-GCM (Modern)
                    │
             Gửi qua TCP Socket
                    │
                Receiver
                    │
        Xác thực chữ ký RSA
                    │
      Giải mã DES hoặc AES-GCM
                    │
          Lưu và phát lại âm thanh
```

---

# 📂 Cấu trúc thư mục

```text
Gui_Nhan_File_Bao_Mat

│
├── Sender
│   ├── sender.py
│   ├── sender_legacy.py
│   ├── aes_gcm.py
│   ├── record_audio_util.py
│   ├── sender_private.pem
│   ├── sender_public.pem
│   └── voice.wav
│
├── Receiver
│   ├── receiver.py
│   ├── receiver_legacy.py
│   ├── aes_gcm.py
│   ├── receiver_private.pem
│   ├── receiver_public.pem
│   └── received_voice.wav
│
└── README.md
```

---

# ⚙ Yêu cầu

- Python 3.10 trở lên
- Thư viện PyCryptodome

Cài đặt:

```bash
pip install pycryptodome
```

---

# 🚀 Hướng dẫn chạy chương trình

## Bước 1: Mở Terminal

Di chuyển đến thư mục **Legacy-voice**:

```bash
cd F:\HocCNTT-1802\ATBMTT\Legacy-voice
```

---

## Bước 2: Khởi động Receiver

```bash
cd Gui_Nhan_File_Bao_Mat\Receiver
py receiver.py
```

Chương trình sẽ hiển thị:

```text
Receiver: Đợi kết nối tại 0.0.0.0:65432...
```

---

## Bước 3: Mở Terminal mới

Quay lại thư mục gốc:

```bash
cd ..
cd Sender
```

hoặc mở Terminal mới tại thư mục **Legacy-voice** rồi chạy:

```bash
cd Gui_Nhan_File_Bao_Mat\Sender
py sender.py
```

---

## Bước 4: Chọn chế độ mã hóa

```text
=========================================
 Legacy Voice Encryption
=========================================
1. Legacy Mode (DES)
2. Modern Mode (AES-GCM)

Select mode (1/2):
```

- Nhập **1** để sử dụng **Legacy Mode (DES)**.
- Nhập **2** để sử dụng **Modern Mode (AES-GCM)**.

---

## Bước 5: Gửi file âm thanh

Chương trình sẽ hỏi:

```text
Bạn có muốn ghi âm mới không? (y/n):
```

- **y** → Ghi âm mới.
- **n** → Sử dụng file `voice.wav` có sẵn.

---

## Kết quả

Nếu truyền thành công:

**Sender**

```text
Sender: Đã gửi thành công
Sender: Receiver xác nhận thành công
```

**Receiver**

```text
Receiver: AES-GCM Decrypt thành công
Receiver: Đã lưu received_voice.wav
Receiver: Gửi ACK thành công
Receiver: Đang phát âm thanh...
```

---

# 🔄 Quy trình hoạt động

```text
Sender

↓

Ghi âm / Chọn file

↓

Ký số RSA

↓

Mã hóa DES hoặc AES-GCM

↓

Gửi qua TCP Socket

↓

Receiver

↓

Kiểm tra chữ ký RSA

↓

Giải mã

↓

Lưu và phát âm thanh
```

---

# 🔐 So sánh thuật toán

| Tiêu chí | DES | AES-GCM |
|----------|-----|---------|
| Độ dài khóa | 56 bit | 256 bit |
| Bảo mật | Thấp | Cao |
| Xác thực | Không | Có |
| Kiểm tra toàn vẹn | Không | Có |
| Phát hiện chỉnh sửa | Không | Có |
| Khuyến nghị | Không | Có |

---

# 🧪 Kiểm thử

Chương trình hỗ trợ các bài kiểm thử sau:

- ✅ Gửi file âm thanh bằng DES.
- ✅ Gửi file âm thanh bằng AES-GCM.
- ✅ Chỉnh sửa Ciphertext.
- ✅ Chỉnh sửa Metadata.
- ✅ So sánh thời gian xử lý.
- ✅ Kiểm tra cảnh báo Legacy Mode.

---

# 📊 Benchmark

So sánh hiệu năng giữa:

- DES
- AES-GCM

Các thông số đánh giá:

- Thời gian mã hóa.
- Thời gian giải mã.
- Kích thước dữ liệu.
- Hiệu năng xử lý.

---

# ⚠ Cảnh báo Legacy Mode

Khi người dùng chọn chế độ Legacy, chương trình sẽ hiển thị:

```text
==============================
⚠ CẢNH BÁO
DES là thuật toán mã hóa đã lỗi thời.

Chế độ này chỉ được sử dụng nhằm đảm bảo khả năng tương thích với hệ thống cũ.

Khuyến nghị sử dụng AES-GCM.
==============================
```

---

# 📄 Sản phẩm nộp

- Source Code
- File âm thanh mẫu
- Báo cáo Migration
- Test Report
- Video Demo

---

# 👨‍💻 Nhóm thực hiện

**Học phần:** FIT4012 – Secure System Upgrade Challenge

**Đề tài 19:** Legacy Voice Encryption Migration – Ứng dụng bảo mật tin nhắn âm thanh với DES và xác thực RSA