import cv2
import mediapipe as mp

# Initialize MediaPipe Hand tracking
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Open default webcam (0)
cap = cv2.VideoCapture(0)

print("Starting camera... Press 'q' on the camera window to exit.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    # Flip image horizontally for intuitive mirror view
    frame = cv2.flip(frame, 1)
    
    # Convert BGR image to RGB for MediaPipe processing
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    # Draw hand landmarks if detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Show video window
    cv2.imshow("Hand Tracking Test", frame)

    # Press 'q' to stop script
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()