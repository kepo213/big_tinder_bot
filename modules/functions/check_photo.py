import cv2


def search_face(file_name: str = "111.jpg"):
    face_cascade_db = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    img = cv2.imread(f"modules/functions/{file_name}")
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade_db.detectMultiScale(img_gray, 1.1, 19)
    return len(faces)


# from imutils import paths
# import face_recognition
# import pickle
# import cv2
# import os
#
# # в директории Images хранятся папки со всеми изображениями
#
# imagePaths = list(paths.list_images('Images'))
# knownEncodings = []
# knownNames = []
# # перебираем все папки с изображениями
# for (i, imagePath) in enumerate(imagePaths):
#     # загружаем изображение и конвертируем его из BGR (OpenCV ordering)
#     # в dlib ordering (RGB)
#     image = cv2.imread(imagePath)
#     rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     # используем библиотеку Face_recognition для обнаружения лиц
#     boxes = face_recognition.face_locations(rgb, model='hog')
#     # вычисляем эмбеддинги для каждого лица
#     encodings = face_recognition.face_encodings(rgb, boxes)
#     # loop over the encodings
#     for encoding in encodings:
#         knownEncodings.append(encoding)
#         knownNames.append(name)
# # сохраним эмбеддинги вместе с их именами в формате словаря
# data = {"encodings": knownEncodings, "names": knownNames}
# # для сохранения данных в файл используем метод pickle
# f = open("face_enc", "wb")
# f.write(pickle.dumps(data))
# f.close()