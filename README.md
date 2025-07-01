# typesled-hack
Frustrated by the Type-S underglow app's 49-color limit and lack of customization, I decompiled the Android APK to find the BLE UUIDs, static TEA-128 key, and 20-byte command format. I then wrote a Python script using Bleak to authenticate, build encrypted packets, and unlock full control of the lights, including red/blue strobes.
