import cv2
from FaceDetection import FaceDetection
from MongoConfig import MongoConnectionClient as db

fd = FaceDetection(r'C:\Users\Sasuk\Desktop\face_recon\faces')
#fd.load_encoding_images("faces/")

capture = cv2.VideoCapture(0)
face_Cascade = cv2.CascadeClassifier(r'C:\Users\Sasuk\Desktop\face_recon\eyes\haarcascade_frontface.xml')

processing = fd.processing

while capture.isOpened():
    _ret, frame = capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_Cascade.detectMultiScale(gray,1.1,4)
    print(' ')
    if not processing and len(faces) >= 1:
        print('Saving the image')
        cv2.imwrite('./faces/teste.jpeg', frame)
        foo = fd.detect_face(frame)
        print(foo)

    print('Is not saving the image')

    cv2.imshow("Frame", frame)
    
    key = cv2.waitKey(1)
    if key == 27:
        break

capture.release()
cv2.destroyAllWindows()