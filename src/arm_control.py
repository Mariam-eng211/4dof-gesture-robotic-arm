import cv2
import mediapipe as mp
import serial
import time
import math

# --- SERIAL SETUP ---
COM_PORT = 'COM8'  # Update to match your actual Arduino COM port (e.g., 'COM3', 'COM4')
BAUD_RATE = 9600

try:
    arduino = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
    print(f"Connected to Arduino on {COM_PORT}")
except Exception as e:
    print(f"Could not connect to {COM_PORT}: {e}")
    print("Running in simulation mode (no serial data sent).")
    arduino = None

# --- MEDIAPIPE SETUP ---
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    base_angle = 90
    shoulder_angle = 90
    elbow_angle = 90
    gripper_angle = 0

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # 1. Base Servo (Hand X Position: Left/Right)
            wrist_x = hand_landmarks.landmark[0].x
            base_angle = int(wrist_x * 180)
            base_angle = max(0, min(180, base_angle))

            # 2. Shoulder Servo (Hand Y Position: Up/Down)
            wrist_y = hand_landmarks.landmark[0].y
            shoulder_angle = int((1.0 - wrist_y) * 180)
            shoulder_angle = max(0, min(180, shoulder_angle))

            # 3. Elbow Servo (Wrist to Middle Finger MCP Distance: Depth/Reach)
            wrist = hand_landmarks.landmark[0]
            middle_mcp = hand_landmarks.landmark[9]
            reach_dist = math.hypot((middle_mcp.x - wrist.x) * w, (middle_mcp.y - wrist.y) * h)
            elbow_angle = int(((reach_dist - 50) / (180 - 50)) * 180)
            elbow_angle = max(0, min(180, elbow_angle))

            # 4. Gripper Servo (Pinch distance between Thumb #4 & Index #8)
            thumb_tip = hand_landmarks.landmark[4]
            index_tip = hand_landmarks.landmark[8]
            px1, py1 = int(thumb_tip.x * w), int(thumb_tip.y * h)
            px2, py2 = int(index_tip.x * w), int(index_tip.y * h)
            pinch_dist = math.hypot(px2 - px1, py2 - py1)

            gripper_angle = int(((pinch_dist - 20) / (150 - 20)) * 180)
            gripper_angle = max(0, min(180, gripper_angle))

            # On-screen text for all 4 joints
            cv2.line(frame, (px1, py1), (px2, py2), (255, 0, 0), 3)
            cv2.putText(frame, f"Base: {base_angle} deg", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.putText(frame, f"Shoulder: {shoulder_angle} deg", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.putText(frame, f"Elbow: {elbow_angle} deg", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.putText(frame, f"Gripper: {gripper_angle} deg", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # Send formatted data string: "base,shoulder,elbow,gripper\n"
            if arduino and arduino.is_open:
                data_string = f"{base_angle},{shoulder_angle},{elbow_angle},{gripper_angle}\n"
                arduino.write(data_string.encode('utf-8'))

    cv2.imshow("4-DOF Robotic Arm Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

if arduino:
    arduino.close()
cap.release()
cv2.destroyAllWindows()