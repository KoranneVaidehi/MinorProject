import cv2
import numpy as np
import os
from mtcnn import MTCNN


# Helper function for readable text
def draw_text(img, text, pos):
    x, y = pos

    # white outline
    cv2.putText(img, text, (x, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 3)

    # black text
    cv2.putText(img, text, (x, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)


# IMAGE: Face Detection + Heatmap + Landmarks
def detect_face(image_path):

    detector = MTCNN()

    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    faces = detector.detect_faces(img_rgb)

    heatmap = np.zeros((img.shape[0], img.shape[1]), dtype=np.float32)

    # Gaussian heatmap
    for face in faces:
        x, y, w, h = face['box']

        cx = x + w // 2
        cy = y + h // 2

        radius = int(max(w, h) / 2)

        for i in range(-radius, radius):
            for j in range(-radius, radius):

                ny = cy + i
                nx = cx + j

                if 0 <= ny < heatmap.shape[0] and 0 <= nx < heatmap.shape[1]:
                    distance = (i**2 + j**2) / (2 * (radius**2))
                    heatmap[ny, nx] += np.exp(-distance)

    # Smooth
    heatmap = cv2.GaussianBlur(heatmap, (51, 51), 0)

    # Normalize
    heatmap = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
    heatmap = heatmap.astype(np.uint8)

    # Color map
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    # Overlay
    overlay = cv2.addWeighted(img, 0.5, heatmap, 0.5, 0)

    # Landmarks + labels
    for face in faces:
        keypoints = face['keypoints']

        left_eye = keypoints['left_eye']
        right_eye = keypoints['right_eye']
        nose = keypoints['nose']
        mouth_left = keypoints['mouth_left']
        mouth_right = keypoints['mouth_right']

        # Draw points
        cv2.circle(overlay, left_eye, 3, (255, 255, 255), -1)
        cv2.circle(overlay, right_eye, 3, (255, 255, 255), -1)
        cv2.circle(overlay, nose, 3, (255, 255, 255), -1)
        cv2.circle(overlay, mouth_left, 3, (255, 255, 255), -1)
        cv2.circle(overlay, mouth_right, 3, (255, 255, 255), -1)

        # Offset for text
        offset = 10

        draw_text(overlay, "Left Eye", (left_eye[0] + offset, left_eye[1] - offset))
        draw_text(overlay, "Right Eye", (right_eye[0] + offset, right_eye[1] - offset))
        draw_text(overlay, "Nose", (nose[0] + offset, nose[1] - offset))
        draw_text(overlay, "Lips", (mouth_left[0] + offset, mouth_left[1] - offset))

    # Save output
    filename = os.path.basename(image_path)
    name, ext = os.path.splitext(filename)

    output_dir = os.path.join("media", "heatmaps")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{name}_heatmap{ext}")
    cv2.imwrite(output_path, overlay)

    return len(faces), f"/media/heatmaps/{name}_heatmap{ext}"


# VIDEO: First frame + Heatmap + Landmarks
def detect_faces_video(video_path):

    detector = MTCNN()

    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return 0, None

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = detector.detect_faces(rgb)

    heatmap = np.zeros((frame.shape[0], frame.shape[1]), dtype=np.float32)

    for face in faces:
        x, y, w, h = face['box']

        cx = x + w // 2
        cy = y + h // 2

        radius = int(max(w, h) / 2)

        for i in range(-radius, radius):
            for j in range(-radius, radius):

                ny = cy + i
                nx = cx + j

                if 0 <= ny < heatmap.shape[0] and 0 <= nx < heatmap.shape[1]:
                    distance = (i**2 + j**2) / (2 * (radius**2))
                    heatmap[ny, nx] += np.exp(-distance)

    heatmap = cv2.GaussianBlur(heatmap, (51, 51), 0)

    heatmap = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
    heatmap = heatmap.astype(np.uint8)

    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    overlay = cv2.addWeighted(frame, 0.5, heatmap, 0.5, 0)

    for face in faces:
        keypoints = face['keypoints']

        left_eye = keypoints['left_eye']
        right_eye = keypoints['right_eye']
        nose = keypoints['nose']
        mouth_left = keypoints['mouth_left']

        cv2.circle(overlay, left_eye, 3, (255, 255, 255), -1)
        cv2.circle(overlay, right_eye, 3, (255, 255, 255), -1)
        cv2.circle(overlay, nose, 3, (255, 255, 255), -1)
        cv2.circle(overlay, mouth_left, 3, (255, 255, 255), -1)

        offset = 10

        draw_text(overlay, "Left Eye", (left_eye[0] + offset, left_eye[1] - offset))
        draw_text(overlay, "Right Eye", (right_eye[0] + offset, right_eye[1] - offset))
        draw_text(overlay, "Nose", (nose[0] + offset, nose[1] - offset))
        draw_text(overlay, "Lips", (mouth_left[0] + offset, mouth_left[1] - offset))

    filename = os.path.basename(video_path)
    name, _ = os.path.splitext(filename)

    output_dir = os.path.join("media", "heatmaps")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{name}_frame_heatmap.jpg")
    cv2.imwrite(output_path, overlay)

    return len(faces), f"/media/heatmaps/{name}_frame_heatmap.jpg"