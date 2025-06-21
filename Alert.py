import cv2
import numpy as np
import time
import threading
import winsound

# Eye Aspect Ratio calculation function
def calculate_ear(eye):
    if len(eye) >= 6:
        A = np.linalg.norm(eye[1] - eye[5])
        B = np.linalg.norm(eye[2] - eye[4])
        C = np.linalg.norm(eye[0] - eye[3])
        ear = (A + B) / (2.0 * C)
        return ear
    return 0  # Return 0 if there are not enough points

# EAR threshold and frame count
EAR_THRESHOLD = 0.25
CONSEC_FRAMES = 20
frame_count = 0
beep_event = threading.Event()

# Previous state tracking for terminal output
prev_state = None

# Function to simulate beep logging in terminal
def beep_log():
    while beep_event.is_set():
        print("🔔 BEEPING SOUND SWITCHED ON (Drowsiness Detected)")
        time.sleep(3)  # Wait before printing again

# Use DirectShow to avoid MSMF issues
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
time.sleep(2)  # Camera initialization

if not cap.isOpened():
    print("❌ Error: Could not open camera.")
    exit()

print("✅ Driver Alert System Running...")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Error: Couldn't read frame from camera.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape

    # Define eye region manually (Adjust values based on face size in frame)
    left_eye = gray[int(height * 0.35):int(height * 0.45), int(width * 0.25):int(width * 0.35)]
    right_eye = gray[int(height * 0.35):int(height * 0.45), int(width * 0.65):int(width * 0.75)]

    # Detect edges for better eye contouring
    left_eye_edges = cv2.Canny(left_eye, 50, 150)
    right_eye_edges = cv2.Canny(right_eye, 50, 150)

    # Find contours in left and right eye
    left_eye_contours, _ = cv2.findContours(left_eye_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    right_eye_contours, _ = cv2.findContours(right_eye_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    left_ear, right_ear = 0, 0

    if left_eye_contours:
        left_eye_hull = cv2.convexHull(max(left_eye_contours, key=cv2.contourArea))
        if len(left_eye_hull) >= 6:
            left_ear = calculate_ear(left_eye_hull[:, 0, :])
            cv2.polylines(frame, [left_eye_hull], True, (0, 255, 0) if left_ear >= EAR_THRESHOLD else (0, 0, 255), 2)

    if right_eye_contours:
        right_eye_hull = cv2.convexHull(max(right_eye_contours, key=cv2.contourArea))
        if len(right_eye_hull) >= 6:
            right_ear = calculate_ear(right_eye_hull[:, 0, :])
            cv2.polylines(frame, [right_eye_hull], True, (0, 255, 0) if right_ear >= EAR_THRESHOLD else (0, 0, 255), 2)

    # Average EAR from both eyes
    ear = (left_ear + right_ear) / 2.0

    # Sleep Alert Logic
    if ear > 0:
        if ear < EAR_THRESHOLD:
            frame_count += 1
            if frame_count >= CONSEC_FRAMES:
                cv2.putText(frame, "SLEEP ALERT!", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

                # Log only when state changes
                if prev_state != "SLEEP ALERT":
                    print("🚨 SLEEP ALERT! - EAR:", round(ear, 2))
                    prev_state = "SLEEP ALERT"

                # Trigger beep logging
                if not beep_event.is_set():
                    beep_event.set()
                    threading.Thread(target=beep_log, daemon=True).start()

        else:
            frame_count = 0
            cv2.putText(frame, "AWAKE", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

            # Log only when state changes
            if prev_state != "AWAKE":
                print("✅ AWAKE - EAR:", round(ear, 2))
                prev_state = "AWAKE"

            beep_event.clear()

    # Display the processed frame
    cv2.imshow('Driver Alert System', frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
beep_event.clear()
