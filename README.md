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

---

## Reversing the Encryption 🔓

The Type-S app encrypts all BLE commands using **TEA (Tiny Encryption Algorithm)**. Inside the APK, we found a 'Tea.java' class that handled both encryption and decryption, with a hardcoded 16-byte key:

```
private static byte[] g = {97, 100, 102, 55, 56, 101, 114, 51, 104, 97, 102, 56, 56, 97, 100, 48};
// => b"adf78er3haf88ad0"
```

The code uses **TEA-128** in ECB mode, operating on 8-byte blocks for both 'tea_encrypt()' and 'tea_decrypt()'. Each command sent to the hub is a 20-byte frame, padded and encrypted with this static key. Decryption uses a 32-round loop and a delta constant of '0x9E3779B9', confirming it's a textbook TEA implementation.

After porting this logic to Python using 'struct' and masking to simulate 32-bit wrapping, we could successfully encrypt and decrypt packets exactly as the app does. No dynamic keys, no pairing logic — just symmetric crypto with a shared hardcoded key.

Once reversed, we built helper functions like 'tea_enc()' and 'tea_dec()' to support constructing and interpreting the hub’s protocol.

> ⚠️ **Note:** This key appears to be the same across all Type-S hubs. There is no per-device authentication.


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

The main reason I started this project was to get **proper red/blue flashing**, something the stock app likely intentionally avoids. Even with all the limitations, I was able to alternate between red and blue by controlling each hub independently—flashing for a cool looking alternating strobe effect. It’s not perfect, but it works exactly how I wanted.

