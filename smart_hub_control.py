'''
This basically currently mimics how the photo color picker works inside the app.
It asks the user for a RGB value then gets the closest one on the scale and sets it to that.
'''

import asyncio, sys, struct, time
from bleak import BleakClient, BleakScanner
import colorsys

WRITE_UUID  = "8D96B001-0106-64C2-0001-9ACC4838521C"
NOTIFY_UUID = "8D96B002-0106-64C2-0001-9ACC4838521C"

PWD_TEXT = b"MONKEY"                  # case-sensitive, ≤6 bytes
TEA_KEY  = b"adf78er3haf88ad0"
DELTA    = 0x9E3779B9
QUIET    = "--quiet" in sys.argv
sys.argv[:] = [a for a in sys.argv if a != "--quiet"]

# ───────────── Tiny TEA helper ─────────────
k0, k1, k2, k3 = struct.unpack(">4L", TEA_KEY)
def _enc(v0, v1):
    s = 0
    for _ in range(32):
        s  = (s + DELTA) & 0xFFFFFFFF
        v0 = (v0 + (((v1 << 4) + k0) ^ (v1 + s) ^ ((v1 >> 5) + k1))) & 0xFFFFFFFF
        v1 = (v1 + (((v0 << 4) + k2) ^ (v0 + s) ^ ((v0 >> 5) + k3))) & 0xFFFFFFFF
    return v0, v1
def _dec(v0, v1):
    s = (DELTA * 32) & 0xFFFFFFFF
    for _ in range(32):
        v1 = (v1 - (((v0 << 4) + k2) ^ (v0 + s) ^ ((v0 >> 5) + k3))) & 0xFFFFFFFF
        v0 = (v0 - (((v1 << 4) + k0) ^ (v1 + s) ^ ((v1 >> 5) + k1))) & 0xFFFFFFFF
        s  = (s - DELTA) & 0xFFFFFFFF
    return v0, v1
def tea_enc(b: bytes) -> bytes:
    buf = bytearray(b)
    for o in range(0, len(buf)//8*8, 8):
        buf[o:o+8] = struct.pack(">2L", *_enc(*struct.unpack(">2L", buf[o:o+8])))
    return bytes(buf)
def tea_dec(b: bytes) -> bytes:
    buf = bytearray(b)
    for o in range(0, len(buf)//8*8, 8):
        buf[o:o+8] = struct.pack(">2L", *_dec(*struct.unpack(">2L", buf[o:o+8])))
    return bytes(buf)
hx = lambda b: " ".join(f"{x:02X}" for x in b)

# ───────────── Frame builders ─────────────
_sn = 0
def _next():              # cyclic command-sequence
    global _sn; _sn = (_sn + 1) & 0xFF; return _sn

def _frame(cmd_id: int, body: bytes) -> bytes:
    pkt = bytearray(20)
    pkt[0] = 0x45          # ‘E’
    pkt[1] = _next()
    pkt[2] = cmd_id
    pkt[3:3+len(body)] = body
    pkt[19] = sum(pkt[1:19]) & 0xFF
    out = tea_enc(pkt)
    if not QUIET:
        print(f"  TX {cmd_id:02X} plain: {hx(pkt)}")
        print(f"  TX {cmd_id:02X} enc  : {hx(out)}")
    return out

def pwd_pkt():                       # cmd-id 0x01
    return _frame(0x01, PWD_TEXT)

def colour_pkt(col_idx: int, brightness: int = 100) -> bytes:
    """Static-colour cmd-id 0x00   byte layout: [mode,brightness,speed,colorIdx,length]"""
    body = bytes([0x00, brightness, 0x00, col_idx, 0x00])
    return _frame(0x00, body)

# ───────────── BLE helpers ─────────────
async def authenticate(cli: BleakClient) -> bool:
    got = asyncio.Event()
    def cb(_, data: bytes):
        dec = tea_dec(data)
        if not QUIET:
            print(f"  RX enc: {hx(data)}")
            print(f"  RX dec: {hx(dec)}")
        if len(dec) >= 4 and dec[2] in (0x01, 0x12):      # pwd-response cmd-id
            got.result = (dec[3] == 0x00)
            got.set()

    await cli.start_notify(NOTIFY_UUID, cb)
    await cli.write_gatt_char(WRITE_UUID, pwd_pkt())
    try:
        await asyncio.wait_for(got.wait(), 6)
        return got.result
    except asyncio.TimeoutError:
        print("  ⏰ Password response timeout.")
        return False
    finally:
        await cli.stop_notify(NOTIFY_UUID)




# Define color index constants based on the LEDColor enum
COLOR_INDEX = {
    "red": 0,          # COLOR_0
    "orange": 4,       # COLOR_4
    "yellow": 8,       # COLOR_8
    "green": 16,       # COLOR_16
    "teal": 20,        # COLOR_20
    "cyan": 24,        # COLOR_24
    "blue": 32,        # COLOR_32
    "purple": 36,      # COLOR_36
    "magenta": 40,     # COLOR_40
    "pink": 44,        # COLOR_44
    "white": 48,       # COLOR_48
    "off": 0           # Use brightness=0 for off
}

def color_by_index(name, brightness=100):
    """Send a color by name using the color index system"""
    index = COLOR_INDEX.get(name.lower(), 0)
    return colour_pkt(index, brightness if name.lower() != "off" else 0)

def closest_color_index(r, g, b):
    """
    Find the closest color index to the given RGB value.
    
    This uses the same HSV calculation as the Java code to generate
    all 48 colors, then finds the closest match to the requested RGB.
    """
    import colorsys
    
    # Convert target RGB to HSV
    h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
    h *= 360  # Convert to degrees
    s *= 100  # Convert to percentage
    
    # Generate all 48 colors using the same algorithm as the Java code
    best_index = 0
    best_distance = float('inf')
    
    for i in range(48):
        # Calculate HSV values as in the Java code
        java_h = (i // 4) * 30.0
        java_s = (4 - (i % 4)) / 4.0 * 100
        java_v = 100  # Value is always 1.0 in the Java code
        
        # Calculate distance in HSV space (weighted to prioritize hue)
        h_diff = min(abs(h - java_h), 360 - abs(h - java_h))
        distance = (h_diff * 1.0) + (abs(s - java_s) * 0.8)
        
        if distance < best_distance:
            best_distance = distance
            best_index = i
    
    return best_index

def rgb_to_closest_color(r, g, b, brightness=100):
    """Convert RGB to the closest available color index and send it"""
    index = closest_color_index(r, g, b)
    return colour_pkt(index, brightness)


# In your drive function, use this approach:
async def drive(mac: str, tag: str):
    print(f"[{time.strftime('%H:%M:%S')}] Connecting → {tag}")
    async with BleakClient(mac, timeout=6) as cli:
        if not cli.is_connected:
            print("❌  BLE connect failed")
            return
        print("✓  BLE connected")
        if not await authenticate(cli):
            print("❌  PASSWORD REJECTED")
            return
        print("✅  Password accepted – testing color index approach")

        test_colors = [
            (255, 0, 0),    # Red
            (0, 255, 0),    # Green
            (0, 0, 255),    # Blue
            (255, 165, 0),  # Orange
            (255, 255, 0),  # Yellow
            (128, 0, 128),  # Purple
            (255, 192, 203) # Pink
        ]
        
        for r, g, b in test_colors:
            print(f"Setting RGB({r},{g},{b})")
            await cli.write_gatt_char(WRITE_UUID, rgb_to_closest_color(r, g, b))
            await asyncio.sleep(2)
        
        # Turn off
        await cli.write_gatt_char(WRITE_UUID, colour_pkt(0, 0))
        print("✓  Done – disconnecting\n")

async def main():
    macs = [a for a in sys.argv[1:] if ":" in a]
    if not macs:
        print(f"[{time.strftime('%H:%M:%S')}] Scanning for Smart Exterior Kit hubs …")
        devs = await BleakScanner.discover(timeout=6)
        macs = [d.address for d in devs if d.name and d.name.startswith("Smart Exterior Kit")]
    if not macs:
        print("No hubs found.")
        return

    macs = macs[:2]      # support up to two hubs
    for i, m in enumerate(macs):
        try:
            await drive(m, f"hub#{i+1} {m}")
        except Exception as e:
            print(f"❌  hub#{i+1} {m} failed – {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass



