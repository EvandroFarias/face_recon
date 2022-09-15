import cv2
from FaceDetection import FaceDetection
from MongoConfig import MongoConnectionClient as db

fd = FaceDetection()
#fd.load_encoding_images("faces/")

capture = cv2.VideoCapture(0)

while True:
    ret, frame = capture.read()

    #face_locations, face_names = fd.detect_known_faces(frame)
    face_locations, face_names = fd.search_face_on_db(frame)
    for face_loc, name in zip(face_locations, face_names):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

        if not name:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)
        else:
            cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 155, 0), 4)

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break
    
capture.release()
cv2.destroyAllWindows()


converted_image = r"C:\Users\Sasuk\Desktop\face_recon\faces\Evandro.jpg"
fd.save_face("Evandro", converted_image)
# fd.search_face_on_db(converted_image)
# database = db('localhost', 27017)
# database.connect_to_collection('facedetectapp','facedetectapp')
# print(database.select_all()['face_encoding'])

