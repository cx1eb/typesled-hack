# Type-S UnderGlow — 'Fixing' the App with Python 🐒✨
> **TL;DR:** The official iOS/Android app locks a fully-RGB LED strip to 49 preset colours and a handful of animations.  
> I pulled the APK apart, found the BLE protocol + TEA-128 key, and wrote a Python driver that finally unlocks any colour (yes, even red/blue strobes).

---

## Why bother?

| Problem | Reality |
|---------|---------|
| **App is cripple-ware** | 48-colour wheel ('0-48', so 49 slots total), zero custom RGB, no desktop client. |
| **Photo match is fake** | It samples a pixel then rounds to the nearest preset colour. |
| **Hardware can do millions** | The strip is plain 5050 SMD RGB; limitations are 100 % software (plus a sprinkle of MCU firmware). |
| **Company ghosts users** | Reviews, emails, tweets — all ignored. |

---

## What I did (high level)

| # | Step | Key Finds |
|---|------|-----------|
| 1 | Decompile APK via 'jadx' | Full Java source, inc. BLE service class |
| 2 | Locate BLE UUIDs | 'WRITE_UUID 8D96B001…' & 'NOTIFY_UUID 8D96B002…' |
| 3 | Reverse protocol | 20-byte command frame, rolling checksum, TEA-128 encryption |
| 4 | Extract crypto | Static TEA key 'adf78er3haf88ad0' (same on every hub) |
| 5 | Write driver | Python 3 + 'Bleak' to scan, auth, and send commands |

---

## Quick start

'''bash
# 1) Pull deps
python -m pip install bleak

# 2) Run it — pass MAC(s) or let it auto-scan
python types_underglow.py                    # scans for 'Smart Exterior Kit'
python types_underglow.py 12:34:56:78:9A:BC  # explicit hub
'''

*Supports two hubs at once (front + rear). Add '--quiet' for no hex dumps.*

---

## How the script works

1. **TEA helpers**  
   'tea_enc()' / 'tea_dec()' wrap Tiny-Encryption-Algorithm in 8-byte ECB blocks (exact match to the app).

2. **Frame builder**  
   '_frame(cmd_id, body)' stuffs your payload into a 20-byte template:  

0 0x45 # constant header 'E'
1 seq-num # rolls 0-255
2 cmd-id # 0x00 colour, 0x01 login, etc.
3-18 body
19 checksum # sum of bytes 1-18

…then TEA-encrypts the lot.

3. **Authentication**  
'authenticate()' subscribes to 'NOTIFY_UUID', sends a password frame (cmd 0x01, body 'MONKEY'), waits for a 0x01/0x12 response. 'dec[3]==0x00' ⇒ pass accepted.

4. **Colour commands**  
*Static colour* (cmd 0x00, mode 0): '[mode, bri, speed, index, len]'  
'''python
colour_pkt(32, 100)   # bright blue
colour_pkt(0, 0)      # off
'''
*Closest-match helper* 'rgb_to_closest_color(r,g,b)' converts arbitrary RGB → nearest preset using the same HSV maths the apk uses.

5. **Drive loop**  
'drive(mac, tag)' connects → login → runs a rainbow test → lights off.

---

## Extending it

* **True 24-bit RGB** — MCU accepts 'mode 1' raw-RGB: '[1, bri, R, G, B]'. Skeleton ('rgb_pkt') is already in the code; uncomment and party.
* **Custom animations** — app motions are cmd 0x05 with different bodies. Sniff them over BLE, clone, or craft new ones.
* **More hubs** — shove MACs into a list and 'asyncio.gather' multiple 'drive()' calls.

---

## Ethical & legal bits ⚖️

* **ToS** — yes, this breaks the Type-S EULA.  
* **Ownership** — hardware is mine; no DRM bypass.  
* **Risk** — a cease-and-desist is possible; publish at your own comfort level.  
* **Safety** — flashing emergency red/blue on public roads is illegal in NZ.

---

## FAQ

> **Will this brick my controller?**  
> Nope. Protocol mirrors the official app; worst case pull the fuse and reboot.

> **Can I run this without Python?**  
> Not yet. A C# + WinBTLE port would be trivial. PRs welcome!

> **Why only 49 colours in the stock app?**  
> Marketing simplicity. The MCU clearly supports raw RGB; the devs just nerfed the UI.

---

## Credits

* **Bleak** — cross-platform Bluetooth awesomeness.  
* Tiny-TEA ref impl — Markku-Joshi.  
* Type-S™ / Winplus® — not affiliated, please don’t sue.
