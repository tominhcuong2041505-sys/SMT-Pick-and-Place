import asyncio
import websockets
import json
import aiohttp

# Cấu hình IP Moonraker (Localhost cho Pi chạy chung Klipper)
MOONRAKER_URL = "http://127.0.0.1:7125" 
MOONRAKER_WS  = "ws://127.0.0.1:7125/websocket"
OPENPNP_LISTEN_PORT = 25001

class KlipperBridge:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.e = 0.0
        self.active_writer = None
        self.session = None

    async def init_http(self):
        self.session = aiohttp.ClientSession()

    async def get_klipper_position(self):
        try:
            async with self.session.get(f"{MOONRAKER_URL}/printer/objects/query?toolhead=position") as res:
                data = await res.json()
                pos = data['result']['status']['toolhead']['position']
                
                # GIA CỐ BẢO MẬT MẢNG: Tránh lỗi IndexError nếu Klipper chưa cấu hình trục
                self.x = pos[0] if len(pos) > 0 else 0.0
                self.y = pos[1] if len(pos) > 1 else 0.0
                self.z = pos[2] if len(pos) > 2 else 0.0
                self.e = pos[3] if len(pos) > 3 else 0.0
        except Exception as err:
            print(f"Lỗi đọc tọa độ HTTP: {err}")

    async def handle_gcode_command(self, cmd):
        cmd_clean = cmd.strip()
        
        # 1. Lọc bỏ các xung nhiễu / lệnh rỗng từ OpenPnP
        if not cmd_clean:
            return "ok\n"
            
        # KHỐI BỌC THÉP FAILSAFE: Đảm bảo 100% mọi lệnh đều trả về 'ok' cho OpenPnP
        try:
            # 2. Xử lý hàm nội suy tọa độ (M114)
            if cmd_clean.startswith("M114"):
                await self.get_klipper_position()
                return f"X:{self.x:.4f} Y:{self.y:.4f} Z:{self.z:.4f} E:{self.e:.4f}\nok\n"
                
            # 3. Lệnh Homing (G28) - Kèm M400 để đợi cơ khí dừng hẳn
            elif cmd_clean.startswith("G28"):
                script_cmd = f"{cmd_clean}\nM400"
                async with self.session.post(f"{MOONRAKER_URL}/printer/gcode/script", json={"script": script_cmd}) as res:
                    await res.read()
                await self.get_klipper_position()
                
            # 4. Tất cả các lệnh còn lại (G0/G1 di chuyển, M42 bật tắt bơm/van/LED, v.v.)
            else:
                async with self.session.post(f"{MOONRAKER_URL}/printer/gcode/script", json={"script": cmd_clean}) as res:
                    await res.read()
                    
        except Exception as e:
            # Bắt mọi ngoại lệ từ Klipper/Moonraker, in ra Console để debug nhưng KHÔNG LÀM TREO OPENPNP
            print(f"[CẢNH BÁO MẠCH LOGIC] Klipper từ chối lệnh '{cmd_clean}' - Lỗi: {e}")
            
        # CHỐT CHẶN SINH TỬ: Luôn thông mạch, trả về 'ok' chính xác để OpenPnP tiếp tục đẩy lệnh
        return "ok\n"

    # Đồng bộ WebSocket (Bắt tọa độ Real-time và Log Console)
    async def stream_klipper_console(self):
        while True:
            try:
                async with websockets.connect(MOONRAKER_WS) as ws:
                    sub_msg = {
                        "jsonrpc": "2.0",
                        "method": "printer.objects.subscribe",
                        "params": {
                            "objects": {"toolhead": ["position"]},
                            "connection_id": 1
                        },
                        "id": 1
                    }
                    await ws.send(json.dumps(sub_msg))
                    
                    while True:
                        msg = await ws.recv()
                        data = json.loads(msg)
                        
                        # Bắt sự kiện cập nhật vị trí cơ khí
                        if data.get("method") == "notify_status_update":
                            params = data.get("params", [{}])
                            if params and "toolhead" in params[0] and "position" in params[0]["toolhead"]:
                                pos = params[0]["toolhead"]["position"]
                                self.x = pos[0] if len(pos) > 0 else self.x
                                self.y = pos[1] if len(pos) > 1 else self.y
                                self.z = pos[2] if len(pos) > 2 else self.z
                                self.e = pos[3] if len(pos) > 3 else self.e
                                
                        # Đẩy Log Console về OpenPnP
                        elif data.get("method") == "notify_gcode_response":
                            params = data.get("params", [])
                            for line in params:
                                if self.active_writer and not self.active_writer.is_closing():
                                    self.active_writer.write(f"{line}\n".encode('utf-8'))
                                    await self.active_writer.drain()
            except Exception as err:
                print(f"Lỗi WebSocket, thử kết nối lại... {err}")
                await asyncio.sleep(2)

bridge = KlipperBridge()

async def handle_client(reader, writer):
    bridge.active_writer = writer
    writer.write("OPENPNP KLIPPER BRIDGE READY!\nok\n".encode('utf-8'))
    await writer.drain()

    try:
        while True:
            data = await reader.readline()
            if not data:
                break
            cmd = data.decode('utf-8')
            response = await bridge.handle_gcode_command(cmd)
            writer.write(response.encode('utf-8'))
            await writer.drain()
    except Exception:
        pass
    finally:
        bridge.active_writer = None

async def main():
    await bridge.init_http()
    server = await asyncio.start_server(handle_client, '0.0.0.0', OPENPNP_LISTEN_PORT)
    print(f"Bridge listening on port {OPENPNP_LISTEN_PORT}...")
    await asyncio.gather(
        server.serve_forever(),
        bridge.stream_klipper_console()
    )

if __name__ == '__main__':
    asyncio.run(main())