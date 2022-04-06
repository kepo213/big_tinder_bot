import cv2


def search_face(file_name: str = "111.jpg"):
    face_cascade_db = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    img = cv2.imread(f"modules/functions/{file_name}")
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade_db.detectMultiScale(img_gray, 1.1, 19)
    return len(faces)
