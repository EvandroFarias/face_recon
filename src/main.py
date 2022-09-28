import cv2
from FaceDetection import FaceDetection
from MongoConfig import MongoConnectionClient as db

fd = FaceDetection()
#fd.load_encoding_images("faces/")

capture = cv2.VideoCapture(0)

while True:
    ret, frame = capture.read()

    print(fd.detect_face(frame))

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break
    
capture.release()
cv2.destroyAllWindows()