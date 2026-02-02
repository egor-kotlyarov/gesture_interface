import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

hand_connections = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (0, 17), (17, 18), (18, 19), (19, 20)
]

lines_color = (248, 3, 252)
points_color = (255, 0, 0)

def main():
    model_path = "hand_landmarker.task"

    base_options = python.BaseOptions(model_asset_path=model_path)
    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        num_hands=2
    )
    detector = vision.HandLandmarker.create_from_options(options)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera not opened! Check macOS camera permissions.")
        return

    print("Camera started. Press 'Esc' to exit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

        result = detector.detect(mp_image)

        if result.hand_landmarks:
            height, width, _ = frame.shape

            for hand_idx, landmarks in enumerate(result.hand_landmarks):

                hand_side = "?"
                if result.handedness and len(result.handedness) > hand_idx:
                    hand_side = result.handedness[hand_idx][0].category_name

                print(f"Hand #{hand_idx} ({hand_side}):")

                for connection in hand_connections:
                    start_idx, end_idx = connection
                    start_lm = landmarks[start_idx]
                    end_lm   = landmarks[end_idx]

                    start_point = (int(start_lm.x * width), int(start_lm.y * height))
                    end_point   = (int(end_lm.x   * width), int(end_lm.y   * height))

                    cv2.line(frame, start_point, end_point, lines_color, 2)

                for lm in landmarks:
                    x_px = int(lm.x * width)
                    y_px = int(lm.y * height)
                    cv2.circle(frame, (x_px, y_px), 5, points_color, -1)

                for j, lm in enumerate(landmarks):
                    print(f"  Landmark {j:2d}: x={lm.x:.3f}, y={lm.y:.3f}, z={lm.z:.3f}")

        cv2.imshow("Camera", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()