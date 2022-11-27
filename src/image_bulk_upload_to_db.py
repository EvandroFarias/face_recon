import re
import glob
import os
import face_recognition
import cv2
from FaceDetection import FaceDetection

fd = FaceDetection()

dict = {
    "Ç": "C",
    "Ã": "A",
    "Á": "A",
    "Â": "A",
    "ÃO": "AO",
    "É": "E",
    "Í": "I",
    "Ó": "O",
    "Ô" : "O",
    "Õ": "O",
    "Ú": "U",
    "´":" ",
    "`": " ",
}

def multiple_replace(dict, text):
    regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))
    return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text)


# raw_img = cv2.imread(r'C:\Users\Sasuk\Desktop\face_recon\faces\EVANDRO CPF6516516541.jpg')
# rgb_frame = cv2.cvtColor(raw_img, cv2.COLOR_BGR2RGB)
# face_encodings = face_recognition.face_encodings(rgb_frame)[0]
# fd.save_face("Evandro",face_encodings)
images_path = glob.glob(os.path.join(
     r'C:\Users\Sasuk\Desktop\face_recon\faces', "*.*"))

for image in images_path:
    try:
        os.rename(image.upper(), multiple_replace(dict, image.upper()))

        image = multiple_replace(dict, image)

        img = cv2.imread(image)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        basename = os.path.basename(image)
        (filename, _ext) = os.path.splitext(basename)

        outravariavel = face_recognition.face_encodings(rgb_img)
        if (outravariavel):
            img_encoding = outravariavel[0]
            fd.save_face(filename, img_encoding.tolist())
            print(image)
        else:
            print(f"{filename} has no recognizable face on image")
    except Exception as ex:
        print(ex, filename)
