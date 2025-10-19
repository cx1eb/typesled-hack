# 🔧 Type S Smart LED Firmware Reference

> 🗂️ Source: `resources/com.types.apk/res/xml/remote_config_defaults.xml`  
> 📦 Firebase Project: **type-s-led-bc47f**  
> ☁️ Storage Bucket: `gs://type-s-led-bc47f.appspot.com`  
> 🧠 Extracted from the official Type S Android app for research & documentation.

---

## 🟣 CBY Switch / Smart Hub Underglow (Exterior LED Kit)

### 🔹 `cby_sw02_sw03_OTA_Info`
**Description:** Production firmware for Smart Hub control and switch modules.  
**Release Date:** 2024-11-22  

| Type | MCU | Version | File | URL |
|------|------|----------|------|----|
| Control | PY32F003 | V000F | `ctrl_py32f003_app_V000F.bin` | [Download](https://firebasestorage.googleapis.com/v0/b/type-s-led-bc47f.appspot.com/o/ota_files%2Fcby_sw02_sw03%2Fctrl_py32f003_app_V000F.bin?alt=media&token=5e12ce7f-0d2f-46f2-96b9-bcee4888da06) |
| Switch | PY32F030 | V000C | `switch_py32f030_app_V000C.bin` | [Download](https://firebasestorage.googleapis.com/v0/b/type-s-led-bc47f.appspot.com/o/ota_files%2Fcby_sw02_sw03%2Fswitch_py32f030_app_V000C.bin?alt=media&token=e51eeb09-4f55-4aa3-bc30-334ee33ef152) |

---

### 🔹 `cby_sw02_sw03_OTA_Info_v1`
**Description:** Newer control-module build (PY32F040 MCU, “new_version_1” folder).  
**Release Date:** 2024-11-22  

| Type | MCU | Version | File | URL | Notes |
|------|------|----------|------|------|-------|
| Control | PY32F040 | V0012 | `ctrl_PY32F040_APP_0708v000120hex.bin` | [Download](https://firebasestorage.googleapis.com/v0/b/type-s-led-bc47f.appspot.com/o/ota_files%2Fcby_sw02_sw03%2Fnew_version_1%2Fctrl_PY32F040_APP_0708v000120hex.bin?alt=media&token=f78fcfa3-61c4-4acd-a2ac-71e3b6dedd30) | ⚠️ Requires Firebase App Check (token invalid) |
| Switch | PY32F030 | V000C | `switch_py32f030_app_V000C.bin` | [Download](https://firebasestorage.googleapis.com/v0/b/type-s-led-bc47f.appspot.com/o/ota_files%2Fcby_sw02_sw03%2Fswitch_py32f030_app_V000C.bin?alt=media&token=e51eeb09-4f55-4aa3-bc30-334ee33ef152) | Same as production switch firmware |

---

### 🔹 `cby_sw02_sw03_OTA_Info_for_test`
**Description:** Internal / test OTA build — still publicly accessible.  
**Release Date:** 2025-04-29  

| Type | MCU | Version | File | URL |
|------|------|----------|------|----|
| Control | PY32F040 | V0012 | `ctrl_py32f040_app_V0012 (2).bin` | [Download](https://firebasestorage.googleapis.com/v0/b/type-s-led-bc47f.appspot.com/o/ota_files%2Fcby_sw02_sw03%2Ffor_test%2Fctrl_py32f040_app_V0012%20(2).bin?alt=media&token=4af4e313-f4a2-4b19-a667-4fe4db4a946c) |
| Switch | PY32F030 | V000F | `switch_py32f030_app_V000F.bin` | [Download](https://firebasestorage.googleapis.com/v0/b/type-s-led-bc47f.appspot.com/o/ota_files%2Fcby_sw02_sw03%2Ffor_test%2Fswitch_py32f030_app_V000F.bin?alt=media&token=b199c817-bbea-456c-be55-d3c5563932a8) |

---

## 🟡 Video Light Kit

### 🔹 `videoLight_OTA_Info`
**Description:** Firmware for Type S Smart Video Light (Bluetooth camera-linked kit).  
**Version:** 150104ac8000020B02  
**Updated:** 2022-11-28 07:20:12  

| Type | File | URL |
|------|------|------|
| Controller MCU | `150104ac8000020B02.bin` | [Download](https://firebasestorage.googleapis.com/v0/b/type-s-led-bc47f.appspot.com/o/ota_files%2Fvidoe_light%2F150104ac8000020B02.bin?alt=media&token=14e7bdbb-97df-47eb-bffb-8eadb712b318) |

---

## 🟢 Firebase Project Information

| Field | Value |
|--------|--------|
| **Project ID** | `type-s-led-bc47f` |
| **Database URL** | `https://type-s-led-bc47f.firebaseio.com` |
| **Storage Bucket** | `type-s-led-bc47f.appspot.com` |
| **Used By** | Type S LED App (Android package `com.types`) |
| **Remote Config Source** | `res/xml/remote_config_defaults.xml` |
| **Notes** | All `.bin` firmware files are hosted via Firebase Storage. Newer App Check restrictions may block future access. |

---

## ⚠️ Disclaimer
These URLs and metadata were publicly embedded inside the official Type S Android app.  
They are shared **for educational and reverse-engineering documentation only**.  
Do **not** redistribute or modify proprietary firmware; use this list solely for **research and hardware identification**.
