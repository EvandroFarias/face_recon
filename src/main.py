import cv2
import asyncio
from FaceDetection import FaceDetection
from MongoConfig import MongoConnectionClient as db

capture = cv2.VideoCapture(0)
face_Cascade = cv2.CascadeClassifier(r'C:\Users\Sasuk\Desktop\face_recon\eyes\haarcascade_frontface.xml')

fd = FaceDetection()
fd.load_faces()

while capture.isOpened():

    _ret, frame = capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_Cascade.detectMultiScale(gray,1.1,4)
    for x,y,h,w in faces:
        cv2.rectangle(frame,(x,y), (x+w,y+h),(255,0,0),3)    
    if not fd.processing and not fd.catracaOpen:
        fd.processing = True
        cv2.imwrite('./faces/teste.jpeg', frame)
        asyncio.run(fd.detect_face(r'C:\Users\Sasuk\Desktop\face_recon\faces\teste.jpeg'))

    cv2.imshow("Frame", frame)
    
    key = cv2.waitKey(1)
    if key == 27:
        break

    if key == ord('c'):
        fd.catracaOpen = False
        continue


capture.release()
cv2.destroyAllWindows()