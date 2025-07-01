# Type-S UnderGlow — 'Fixing' the App with Python 🐒✨
> **TL;DR:** The official iOS/Android app limits your RGB underglow to 49 preset colors and a few built-in effects.  
> I reverse-engineered the Android app, found the BLE UUIDs, TEA-128 encryption key, and packet format, then wrote a Python script to send custom packets—only to discover the lights only respond to preset indexes. Likely, firmware is locked to accept only predefined color commands.

---

## Why bother?

| Problem | Reality |
|--------|---------|
| **App is cripple-ware** | 49 preset colors (0–48), no true RGB values, no desktop support. |
| **Photo color match is fake** | It selects the closest preset, not the actual pixel color. |
| **Hardware is capable** | Uses 5050 SMD RGB strips, but heavily restricted by software (and possibly firmware). |
| **Company is unresponsive** | Emails, Reviews, Instagram — no replies. |

---

## What I did (overview)

| Step | Description | Result |
|------|-------------|--------|
| 1 | Decompiled the Android APK using `jadx` | Found BLE code, UUIDs, encryption |
| 2 | Found BLE UUIDs | `WRITE_UUID` and `NOTIFY_UUID` |
| 3 | Found static TEA key | `adf78er3haf88ad0` — same on all hubs |
| 4 | Rebuilt command structure | 20-byte encrypted packets |
| 5 | Wrote a Python BLE controller | Using Bleak to scan, authenticate, and send commands |
| 6 | Tested raw RGB values | Strip ignores all except official color indexes — likely firmware-locked |

---

## How it works

The Python script uses:
- `Bleak` for BLE communication
- TEA-128 encryption (matching app logic)
- A rolling checksum and 20-byte command frames
- A simple authentication flow (sends `MONKEY` as the password)

Only officially recognized color index values (0–48) trigger color changes, even though the protocol allows sending raw RGB. This strongly suggests the LED controller firmware ignores anything outside its hardcoded lookup.

---

## Limitations Discovered

While the hardware (5050 SMD RGB) supports full-color output, actual color setting is limited to the preconfigured list used in the app. Attempts to send raw RGB packets (using mode `0x01`) are accepted but **ignored** by the hub.  
All confirmed successful color changes only occurred when sending predefined indexes (`mode 0x00`, `color index 0–48`). This shows the **firmware is likely rejecting anything not in its preset list**, despite being capable of more.

---

## Ethical & Legal Notes ⚖️

- This technically violates the Type-S app's Terms of Service.
- However, no DRM or copy protection was bypassed.
- All data was retrieved from a legally obtained APK, used on hardware I own.
- I’m publishing this for educational and personal use; if you replicate this, do so responsibly.

---

## Final Thoughts

This was a fun deep-dive into how much artificial limitation is placed on consumer hardware. The potential is there, but unless Type-S updates the firmware (or someone finds a way to flash it), we're stuck with 49 canned colors.  
Still, understanding and exploring how it works was 100% worth it.
