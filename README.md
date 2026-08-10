# 4-DOF Hand Gesture Controlled Robotic Arm

A real-time gesture tracking system for a 4-DOF robotic arm using a regular webcam, OpenCV, MediaPipe, and an Arduino driver.

## How It Works

1. **Webcam capture:** OpenCV grabs camera frames and MediaPipe tracks 21 hand landmarks in 3D space.
2. **Gesture Mapping:**
   - **Base:** Moves left/right based on hand X-position across the screen.
   - **Shoulder:** Moves up/down based on hand Y-position.
   - **Elbow:** Moves based on hand distance to the camera (depth calculation via palm scale).
   - **Gripper:** Opens/closes depending on the distance between thumb tip and index finger tip.
3. **Serial Transfer:** Python packages angles as `base,shoulder,elbow,gripper\n` strings and sends them over USB Serial (9600 Baud).
4. **Servo Control:** An Arduino reads the string, parses angles, and sends PWM signals to a PCA9685 driver.

---

## Hardware Setup

### Parts Needed
- 4-DOF Robotic Arm Kit (with 4 servos like SG90 or MG996R)
- Arduino Uno or ESP32
- PCA9685 16-Channel PWM Driver
- 5V External DC Power Supply (for servos)
- USB Webcam

### Wiring Diagram

**Arduino to PCA9685:**
- Arduino `5V` ➔ PCA9685 `VCC`
- Arduino `GND` ➔ PCA9685 `GND`
- Arduino `A4 (SDA)` ➔ PCA9685 `SDA`
- Arduino `A5 (SCL)` ➔ PCA9685 `SCL`

**PCA9685 Servo Channels:**
- Channel `0`: Base Servo
- Channel `1`: Shoulder Servo
- Channel `2`: Elbow Servo
- Channel `3`: Gripper Servo

> **Important:** Connect your external 5V power supply to the screw terminals on the PCA9685 driver. Do not run all 4 servos off the Arduino's 5V pin directly.

---

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt