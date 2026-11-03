import asyncio
import websockets
import json

MOONRAKER_WS = "ws://127.0.0.1:7125/websocket"
OPENPNP_LISTEN_PORT = 25001

class KlipperBridge:
    def __init__(self):
        self.pos = {'x': 0.0, 'y': 0.0, 'z': 0.0, 'c': 0.0}
        self.ws = None
        self.openpnp_writer = None
        self.req_id = 1
        self.pending_requests = {} 
        self.is_calibrating = False

    async def connect_moonraker(self):
        """Duy trì một đường ống WebSocket duy nhất với Klipper"""
        while True:
            try:
                async with websockets.connect(MOONRAKER_WS) as ws:
                    self.ws = ws
                    # Đăng ký nhận tọa độ thời gian thực (Push notification)
                    sub_msg = {
                        "jsonrpc": "2.0", "method": "printer.objects.subscribe",
                        "params": {"objects": {"toolhead": ["position"]}, "connection_id": 1},
                        "id": self.req_id
                    }
                    await ws.send(json.dumps(sub_msg))
                    
                    async for msg in ws:
                        data = json.loads(msg)
                        method = data.get("method")
                        
                        # MỞ KHÓA LUỒNG: Nếu nhận được ID tương ứng từ Moonraker
                        if "id" in data and data["id"] in self.pending_requests:
                            future = self.pending_requests.pop(data["id"])
                            if not future.done():
                                future.set_result(data)
                                
                        # 1. Bắt tọa độ và lưu ngay vào RAM (Cache)
                        if method == "notify_status_update":
                            try:
                                p = data["params"][0]["toolhead"]["position"]
                                self.pos.update({
                                    'x': p[0] if len(p) > 0 else self.pos['x'],
                                    'y': p[1] if len(p) > 1 else self.pos['y'],
                                    'z': p[2] if len(p) > 2 else self.pos['z'],
                                    'c': p[3] if len(p) > 3 else self.pos['c']
                                })
                            except (KeyError, IndexError):
                                pass
                                
                        # 2. Bắt Log/Output đẩy ngược về Console OpenPnP
                        elif method == "notify_gcode_response":
                            if self.openpnp_writer and not self.openpnp_writer.is_closing():
                                for line in data.get("params", []):
                                    self.openpnp_writer.write(f"{line}\n".encode('utf-8'))
                                await self.openpnp_writer.drain()
                                
            except Exception as e:
                print(f"Mất kết nối Moonraker: {e}. Thử lại sau 2s...")
                self.ws = None
                await asyncio.sleep(2)

    async def send_gcode(self, cmd, wait=False):
        """Gửi lệnh G-code trực tiếp qua WebSocket với tùy chọn Blocking"""
        if not self.ws:
            return
        self.req_id += 1
        payload = {
            "jsonrpc": "2.0", "method": "printer.gcode.script",
            "params": {"script": cmd}, "id": self.req_id
        }
        
        if wait:
            loop = asyncio.get_running_loop()
            future = loop.create_future()
            self.pending_requests[self.req_id] = future
            await self.ws.send(json.dumps(payload))
            await future # Khóa luồng này, ép OpenPnP phải chờ Klipper báo done
        else:
            await self.ws.send(json.dumps(payload))

bridge = KlipperBridge()

async def handle_openpnp(reader, writer):
    bridge.openpnp_writer = writer
    writer.write("OPENPNP KLIPPER BRIDGE READY!\nok\n".encode('utf-8'))
    await writer.drain()

    try:
        while True:
            line = await reader.readline()
            if not line: break
            cmd = line.decode('utf-8').strip()
            if not cmd: continue

            # [GIỮ NGUYÊN] 1. M114 (Đọc tọa độ)
            if cmd.startswith("M114"):
                p = bridge.pos
                writer.write(f"X:{p['x']:.4f} Y:{p['y']:.4f} Z:{p['z']:.4f} C:{p['c']:.4f}\nok\n".encode('utf-8'))
                
            # [THÊM MỚI] 2. Bẫy lệnh M220 để bật/tắt cơ chế Block luồng
            elif cmd.startswith("M220"):
                # Nếu tỷ lệ khác 100%, máy đang chạy Calibration
                if "S100" not in cmd: 
                    bridge.is_calibrating = True
                else:
                    bridge.is_calibrating = False
                await bridge.send_gcode(cmd, wait=False)
                writer.write("ok\n".encode('utf-8'))

            # [GIỮ NGUYÊN] 3. G28 và M400 (BẮT BUỘC CHỜ - BLOCKING)
            elif cmd.startswith("G28") or "M400" in cmd:
                if cmd.startswith("G28") and "M400" not in cmd:
                    cmd += "\nM400"
                await bridge.send_gcode(cmd, wait=True) 
                writer.write("ok\n".encode('utf-8'))
                
            # [CẬP NHẬT] 4. G0/G1: Rẽ nhánh tối ưu
            elif cmd.startswith("G0") or cmd.startswith("G1"):
                if bridge.is_calibrating:
                    # Đang đo Calibrate: Chèn M400, ép Klipper phanh lại và chờ hoàn tất
                    sync_cmd = cmd + "\nM400"
                    await bridge.send_gcode(sync_cmd, wait=True)
                else:
                    # Đang gắp thực tế: Bắn thẳng vào Planner Buffer, không chờ
                    await bridge.send_gcode(cmd, wait=False)
                writer.write("ok\n".encode('utf-8')) 
                
            # [CẬP NHẬT] 5. Các lệnh G-code khác (M42, M226...)
            else:
                await bridge.send_gcode(cmd, wait=False)
                writer.write("ok\n".encode('utf-8')) 
                
            await writer.drain()
            
    except Exception as e:
        print(f"OpenPnP disconnect: {e}")
    finally:
        bridge.openpnp_writer = None
        writer.close()

async def main():
    asyncio.create_task(bridge.connect_moonraker())
    server = await asyncio.start_server(handle_openpnp, '0.0.0.0', OPENPNP_LISTEN_PORT)
    print(f"Bridge G-code tốc độ cao sẵn sàng tại Port {OPENPNP_LISTEN_PORT}...")
    await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())