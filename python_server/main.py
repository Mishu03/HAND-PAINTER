import cv2
import mediapipe as mp

# Mediapipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# OpenCV camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Windows DirectShow backend

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Flip horizontally for mirror effect
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Get index fingertip coordinates (landmark 8)
            h, w, _ = frame.shape
            x = int(hand_landmarks.landmark[8].x * w)
            y = int(hand_landmarks.landmark[8].y * h)
            
            cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)
            print(f"Index finger: x={x}, y={y}")

    cv2.imshow("Hand Tracker", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()