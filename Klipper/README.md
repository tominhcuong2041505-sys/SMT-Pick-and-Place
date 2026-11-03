## 1. Cài đặt file Bridge

Cài đặt thư viện `websockets` cho Python:

```bash
sudo apt update
sudo apt install python3-websockets -y
```

Copy file `lboizbridge.py` vào thư mục `/home/pi`.

**Cấp quyền thực thi:**

```bash
chmod +x /home/pi/lboizbridge.py
```

**Tạo service để tự khởi chạy:**

```bash
sudo nano /etc/systemd/system/lboizbridge.service
```

Dán nội dung sau vào file:

```ini
[Unit]
Description=LboizBridge Python Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/lboizbridge.py
WorkingDirectory=/home/pi
Restart=always
User=pi
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

**Reload systemd và khởi động service:**

```bash
sudo systemctl daemon-reload
sudo systemctl start lboizbridge
sudo systemctl enable lboizbridge
```

**Kiểm tra trạng thái service:**

```bash
sudo systemctl status lboizbridge
```

## 2. Cấu hình Klipper

**Cấu hình `printer.cfg`:**

Copy toàn bộ nội dung file `printer.cfg` trong repo và dán vào file `config/printer.cfg` trên máy in.

**Upload file macro:**

Upload file `macro.pnp.cfg` vào thư mục `config`.

> **Lưu ý:** Đảm bảo `printer.cfg` có dòng `[include macro.pnp.cfg]` để Klipper nạp file macro. Sau khi lưu, nhấn **Save & Restart** (hoặc chạy `FIRMWARE_RESTART`) để áp dụng cấu hình.
