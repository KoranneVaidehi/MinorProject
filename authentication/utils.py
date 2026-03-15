import cv2
from mtcnn import MTCNN


def detect_face(image_path):

    detector = MTCNN()

    img = cv2.imread(image_path)

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    faces = detector.detect_faces(img_rgb)

    return len(faces)


import cv2
from mtcnn import MTCNN


def detect_faces_video(video_path):

    detector = MTCNN()

    cap = cv2.VideoCapture(video_path)

    ret, frame = cap.read()

    cap.release()

    if not ret:
        return 0

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    faces = detector.detect_faces(rgb)

    return len(faces)