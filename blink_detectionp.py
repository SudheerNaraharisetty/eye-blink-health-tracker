import cv2
import mediapipe as mp
import time
import math
import winsound      # For beep sound (Windows only)
import pyttsx3       # For text-to-speech alerts

# -------------------------------
# Initialize Text-to-Speech Engine
# -------------------------------
engine = pyttsx3.init()

# -------------------------------
# Helper Function: Compute Eye Aspect Ratio (EAR)
# -------------------------------
def eye_aspect_ratio(landmarks, eye_indices, img_width, img_height):
    """
    Compute the eye aspect ratio (EAR) for one eye.
    The EAR is defined as:
      EAR = (||p2 - p6|| + ||p3 - p5||) / (2 * ||p1 - p4||)
    where the points are defined by the indices provided in `eye_indices`.
    """
    points = []
    for idx in eye_indices:
        lm = landmarks[idx]
        x, y = int(lm.x * img_width), int(lm.y * img_height)
        points.append((x, y))
    
    p1, p2, p3, p4, p5, p6 = points

    def euclidean(ptA, ptB):
        return math.hypot(ptA[0] - ptB[0], ptA[1] - ptB[1])
    
    A = euclidean(p2, p6)
    B = euclidean(p3, p5)
    C = euclidean(p1, p4)
    
    ear = (A + B) / (2.0 * C)
    return ear

# -------------------------------
# Initialize Mediapipe Face Mesh
# -------------------------------
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

# -------------------------------
# Define Eye Landmark Indices (Based on Mediapipe Face Mesh)
# -------------------------------
LEFT_EYE_INDICES = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_INDICES = [263, 387, 385, 362, 380, 373]

# -------------------------------
# Blink Detection & Alert Parameters
# -------------------------------
EAR_THRESHOLD = 0.2         # Below this, the eye is considered closed.
max_time_without_blink = 15  # Seconds without blinking to trigger an alert.
sound_alert_triggered = False  # Flag to prevent continuous beeping.

# Blink counters and state.
blink_count = 0
eye_closed = False
last_blink_time = time.time()

# -------------------------------
# Session Tracking Parameters
# -------------------------------
session_start_time = time.time()
session_blink_count = 0
session_duration_threshold = 15 * 60  # 15 minutes session duration.
last_summary_message = ""
summary_display_until = 0

# -------------------------------
# Start Video Capture (Using Device Camera)
# -------------------------------
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise IOError("Cannot open webcam. Ensure your webcam is connected.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # ----------- Low-Light Enhancement -----------
    # Convert to grayscale and check average brightness.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if cv2.mean(gray)[0] < 80:  # Adjust threshold as needed.
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        gray_eq = clahe.apply(gray)
        frame = cv2.cvtColor(gray_eq, cv2.COLOR_GRAY2BGR)
    # ---------------------------------------------

    # Flip frame for mirror view.
    frame = cv2.flip(frame, 1)
    img_h, img_w = frame.shape[:2]

    # Convert the frame to RGB for Mediapipe.
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        face_landmarks = results.multi_face_landmarks[0]
        
        # (Optional) Draw face mesh on the frame.
        mp_drawing.draw_landmarks(
            image=frame,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=drawing_spec
        )

        landmarks = face_landmarks.landmark

        # Compute EAR for both eyes and take the average.
        left_ear = eye_aspect_ratio(landmarks, LEFT_EYE_INDICES, img_w, img_h)
        right_ear = eye_aspect_ratio(landmarks, RIGHT_EYE_INDICES, img_w, img_h)
        ear = (left_ear + right_ear) / 2.0

        # ------------- Blink Detection Logic -------------
        if ear < EAR_THRESHOLD:
            if not eye_closed:
                # Eyes have just closed.
                eye_closed = True
        else:
            if eye_closed:
                # Eyes have just opened; count as a blink.
                blink_count += 1
                session_blink_count += 1
                last_blink_time = time.time()  # Reset timer.
                eye_closed = False
                sound_alert_triggered = False  # Reset beep flag.
        # --------------------------------------------------

        # Calculate time since the last blink.
        time_since_last_blink = time.time() - last_blink_time

        # Trigger beep and display alert if no blink for the threshold period.
        if time_since_last_blink > max_time_without_blink:
            cv2.putText(frame, 'Please Blink!', (30, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            if not sound_alert_triggered:
                winsound.Beep(1000, 500)  # 1000 Hz for 500 ms.
                sound_alert_triggered = True

        # ------------- Display Real-Time Information -------------
        cv2.putText(frame, f'Blink Count: {blink_count}', (30, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(frame, f'EAR: {ear:.2f}', (30, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(frame, f'Time since last blink: {time_since_last_blink:.1f}s', (30, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        # --------------------------------------------------------

        # ------------- Session Timer Display -------------
        session_elapsed = time.time() - session_start_time
        session_minutes = int(session_elapsed // 60)
        session_seconds = int(session_elapsed % 60)
        cv2.putText(frame, f'Session Time: {session_minutes}m {session_seconds}s', (30, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
        # ---------------------------------------------------

        # ------------- Session Summary (Every 15 Minutes) -------------
        if session_elapsed >= session_duration_threshold:
            blink_rate = session_blink_count / (session_elapsed / 60.0)  # Blinks per minute.
            if blink_rate < 15:
                assessment = "below the normal range, which may lead to eye strain and dryness."
            elif blink_rate > 20:
                assessment = "above the normal range, which is great for keeping your eyes lubricated!"
            else:
                assessment = "within the normal range."
            summary_message = (
                f"In the past {session_minutes} minutes, you blinked {session_blink_count} times, "
                f"averaging {blink_rate:.1f} blinks per minute. This is {assessment}"
            )
            # Provide voice feedback.
            engine.say(summary_message)
            engine.runAndWait()
            print(summary_message)
            # Display summary on-screen for 5 seconds.
            last_summary_message = summary_message
            summary_display_until = time.time() + 5
            # Reset session counters.
            session_start_time = time.time()
            session_blink_count = 0

        if time.time() < summary_display_until:
            cv2.putText(frame, last_summary_message, (30, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        # ------------------------------------------------------------
    
    # Show the processed frame.
    cv2.imshow('Blink Detection', frame)
    
    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
