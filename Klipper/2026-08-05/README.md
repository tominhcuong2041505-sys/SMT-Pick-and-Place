# Hướng Dẫn Cài Đặt Hệ Thống OpenPnP - Klipper Bridge

Tài liệu này hướng dẫn chi tiết các bước chuẩn bị môi trường và cài đặt phần mềm cầu nối (Bridge) để giao tiếp giữa OpenPnP và Klipper.

## 1. Các File Và Phần Mềm Cần Chuẩn Bị

Để hệ thống hoạt động, máy tính nhúng (ví dụ: Raspberry Pi) cần được cài đặt đầy đủ firmware **Klipper** và API **Moonraker**.

**Công cụ cài đặt khuyến nghị:**
Bạn nên sử dụng **KIAUH** (Klipper Installation And Update Helper) để cài đặt toàn bộ Klipper, Moonraker và giao diện quản lý một cách sạch sẽ, đầy đủ nhất.
*   **Link tải và hướng dẫn KIAUH:** [KIAUH GitHub Repository](https://github.com/dw-0/kiauh)

**Cài đặt thư viện Python (Dependencies):**
Trước khi chạy script cầu nối, bạn cần cài đặt các thư viện không đồng bộ cho Bridge bằng cách chạy lệnh sau trên Pi:
```bash
pip3 install websockets aiohttp
```

**Công cụ thao tác trên máy tính (Windows):**
*   **WinSCP:** Dùng để kéo/thả truyền file vào Raspberry Pi.
*   **PuTTY:** Terminal dùng để kết nối SSH và chạy lệnh hệ thống.

---

## 2. Nạp Cấu Hình Vào Klipper

Thao tác nạp file cấu hình cơ khí rất đơn giản thông qua giao diện Web:

1. Mở trình duyệt và truy cập vào địa chỉ IP của máy (giao diện Mainsail hoặc Fluidd).
2. Vào mục **Machine** (hoặc Configuration).
3. Tải (Upload) trực tiếp 2 file **`printer.cfg`** và **`macro.cfg`** vào thư mục cấu hình của Klipper.
4. Bấm **Save & Restart** để Klipper khởi động lại và nhận cấu hình mới.

---

## 3. Chuyển File Cầu Nối Bằng WinSCP

Bạn cần đưa file thực thi của Bridge vào đúng thư mục của hệ điều hành trên Pi:

1. Mở phần mềm **WinSCP** và kết nối đến máy đã cài Klipper.
2. Ở cửa sổ bên phải của phần mềm (hiển thị dữ liệu trên Pi), điều hướng đến thư mục: `/home/pi/`.
3. Kéo và thả file script cầu nối (ví dụ: `pnp_klipper_bridge.py`) từ máy tính của bạn sang thư mục `/home/pi/` này.

---

## 4. Thiết Lập Script Khởi Chạy Mặc Định (Auto-start)

Để file Bridge tự động chạy nền mỗi khi bật máy PnP, bạn cần tạo một dịch vụ hệ thống (systemd) thông qua PuTTY:

1. Mở **PuTTY**, kết nối SSH vào Pi và đăng nhập.
2. Mở trình soạn thảo để tạo file dịch vụ bằng lệnh:
   ```bash
   sudo nano /etc/systemd/system/pnp_bridge.service
   ```
3. Copy đoạn script dưới đây và dán vào PuTTY (click chuột phải để dán):
   ```ini
   [Unit]
   Description=OpenPnP to Klipper Bridge
   After=network.target moonraker.service

   [Service]
   Type=simple
   User=pi
   WorkingDirectory=/home/pi
   ExecStart=/usr/bin/python3 /home/pi/pnp_klipper_bridge.py
   Restart=always
   RestartSec=3

   [Install]
   WantedBy=multi-user.target
   ```
4. Lưu file lại bằng cách nhấn **Ctrl + X**, sau đó gõ **Y** và nhấn **Enter**.

5. Kích hoạt dịch vụ để nó tự động chạy cùng hệ thống bằng cụm lệnh sau:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable pnp_bridge
   sudo systemctl start pnp_bridge
   ```
