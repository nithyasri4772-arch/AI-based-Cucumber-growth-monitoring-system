# 🔌 Child-Level Hardware Connection Guide

This is a very simple guide to connecting your wires. Follow it pin by pin.

### 📍 1. Servo Motor (Moves the Camera)
| Servo Wire Color | Connection Point | Pin Number |
| :--- | :--- | :--- |
| **ORANGE (Signal)** | ESP32 GPIO | **Digital Pin 13** |
| **RED (Power)** | External Battery (+) | **5V High Power** |
| **BROWN (Ground)** | ESP32 GND & Battery (-) | **GND** |

### 📍 2. Fan Relay (Blows the Leaves)
| Relay Pin | ESP32 Connection | Pin Number |
| :--- | :--- | :--- |
| **IN / Signal** | ESP32 GPIO | **Digital Pin 12** |
| **VCC** | ESP32 Power | **3.3V or 5V** |
| **GND** | ESP32 Ground | **GND** |

### 📍 3. DHT Sensor (Temperature & Humidity)
| Sensor Pin | ESP32 Connection | Pin Number |
| :--- | :--- | :--- |
| **DATA** | ESP32 GPIO | **Digital Pin 4** |
| **VCC** | ESP32 Power | **3.3V** |
| **GND** | ESP32 Ground | **GND** |

---

### ⚠️ IMPORTANT: The "Common Ground" Rule
To make everything work, you **MUST** connect all **GND (Ground)** wires together.
1. Connect the Battery (-) to the ESP32 GND.
2. Connect the Servo Ground to that same point.
3. Connect the Relay Ground to that same point.
**If you don't do this, the motors will not move!**

### 🔋 Powering the Robot
- **DO NOT** use the ESP32 to power the Fan or Servo. They are too strong.
- **DO** use a separate Battery Pack (4 x AA batteries or a 5V power adapter).
- Plug the USB cable into the ESP32 just for the code and data.

---

### 📷 Camera Setup
- If using a **USB Webcam**: Plug it into your Computer (PC).
- If using an **ESP32-CAM**: It must be powered and on the same WiFi as your PC.
- Point the camera at your plant and make sure the **Servo** can turn it to see the Left and Right sides.
