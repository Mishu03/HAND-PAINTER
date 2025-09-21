import cv2
import mediapipe as mp
import asyncio
import websockets
import threading
import json

# WebSocket server URI
WS_URI = "ws://localhost:8765"

# MediaPipe hands setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    min_detection_confidence=0.7, 
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# OpenCV capture
cap = cv2.VideoCapture(0)  # Change index if needed

# Drawing styles
landmark_style = mp_draw.DrawingSpec(color=(250, 230, 230), thickness=4, circle_radius=5)
connection_style = mp_draw.DrawingSpec(color=(205, 235, 255), thickness=2)

# Thread-safe queue to send coordinates
coord_queue = []

# --- WebSocket sender thread ---
async def send_coords(cx, cy, brush_size):
    try:
        async with websockets.connect(WS_URI) as ws:
            data = {"x": cx, "y": cy, "brushSize": brush_size}
            await ws.send(json.dumps(data))
    except:
        pass

def websocket_sender():
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    while True:
        if coord_queue:
            cx, cy, brush_size = coord_queue.pop(0)
            loop.run_until_complete(send_coords(cx, cy, brush_size))
        else:
            loop.run_until_complete(asyncio.sleep(0.01))

threading.Thread(target=websocket_sender, daemon=True).start()

# --- Brush size calculation ---
def calculate_brush_size(hand_landmarks):
    wrist = hand_landmarks.landmark[0]
    finger_tips = [hand_landmarks.landmark[i] for i in [8, 12, 16, 20]]  # index, middle, ring, pinky
    avg_distance = sum(
        ((wrist.x - tip.x)**2 + (wrist.y - tip.y)**2)**0.5 for tip in finger_tips
    ) / len(finger_tips)

    if avg_distance < 0.1:
        return 5     # pinch → small
    elif avg_distance < 0.18:
        return 10    # medium
    else:
        return 20    # open hand → large

# --- Main OpenCV loop ---
while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                frame, 
                hand_landmarks, 
                mp_hands.HAND_CONNECTIONS,
                landmark_drawing_spec=landmark_style,
                connection_drawing_spec=connection_style
            )

            # Fingertip coordinates
            h, w, _ = frame.shape
            index_finger_tip = hand_landmarks.landmark[8]
            cx, cy = int(index_finger_tip.x * w), int(index_finger_tip.y * h)

            # Draw fingertip circle
            cv2.circle(frame, (cx, cy), 10, (52, 66, 227), -1)

            # Calculate brush size
            brush_size = calculate_brush_size(hand_landmarks)

            # Add to queue for WebSocket sending
            coord_queue.append((cx, cy, brush_size))

    # Show camera feed
    cv2.imshow("Hand Tracker", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()