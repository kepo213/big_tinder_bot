
import cv2


def search_face(file_name: str = "111.jpg"):
    face_cascade_db = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    img = cv2.imread(f"modules/functions/{file_name}")
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade_db.detectMultiScale(img_gray, 1.05, 6)
    faces = len(faces)
    if faces != 0:
        faces = 1
    return faces


#
# import os
# os.environ["TF_CPP_MIN_LOG_LEVEL"] = '3'
# from pixellib.instance import instance_segmentation
#
#
# def search_face(file_name: str = "111.jpg"):
#     segment_image = instance_segmentation()
#     segment_image.load_model(model_path=r'D:\IT\Python_3\Free_lanc\GIT\\12-big_tinder_bot\modules\functions\mask_rcnn_coco.h5.h5')
#
#     target_class = segment_image.select_target_classes(person=True)
#
#     output_file_name = '222.jpg'
#     result = segment_image.segmentImage(
#         image_path=file_name,
#         segment_target_classes=target_class)
#     print(result[0]['scores'])
#
#
# search_face()
