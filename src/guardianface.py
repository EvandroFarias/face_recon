from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import os
import time
import cv2
from FaceDetection import FaceDetection
from files.FilesService import FileManipulation

DEFAULT_PATH = os.path.dirname(os.path.abspath(__file__))

#LARGURA x ALTURA
#SIZES = [150,300]

with open(f'{DEFAULT_PATH}\\sizes.cfg') as f:
    SIZES = f.readline().split(',')
    for index, size in enumerate(SIZES):
         SIZES[index] = int(size)
         if int(size) < 150:
              SIZES[index] = 150

UNK_PRS = "PESSOA NÃO RECONHECIDA"
NO_PRS = "SEM PESSOA"

APP_CLOSED = "app_closed.bool"
FACE_LOCATED = "face_located.bool"
APP_STARTED = "app_started.bool"

FACE_OUT = "faceoutput.txt"

capture = cv2.VideoCapture(0)
face_Cascade = cv2.CascadeClassifier(f'{DEFAULT_PATH}\\haarcascade_frontalface_default.xml')

fs = FileManipulation(DEFAULT_PATH)
fd = FaceDetection()
fd.load_faces()

fs.delete_nfiles(APP_CLOSED,FACE_LOCATED,APP_STARTED)

def read_qr_code(frame):
          detect = cv2.QRCodeDetector()
          value, points, straight_qrcode = detect.detectAndDecode(frame)

          if value != None:
               return value

while capture.isOpened():

     _success, frame = capture.read()

     if not _success:
          # Ignorando frame vazio
          continue

     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
     faces = face_Cascade.detectMultiScale(gray,1.1,4)
     if len(faces) > 1:
          if not fs.check_file(FACE_LOCATED):
               cpf = fd.detect_face(frame)
               if cpf:
                    fs.write_file(file=FACE_OUT, text=cpf)
                    fs.create_file(FACE_LOCATED)
               else:
                    fs.write_file(file=FACE_OUT, text=UNK_PRS)

          for x,y,h,w in faces:
               if cpf:
                    cv2.rectangle(frame,(x,y), (x+w,y+h),(0,255,10),3)
               else:
                    cv2.rectangle(frame,(x,y), (x+w,y+h),(0,0,255),3)

     print(read_qr_code(frame))
                    
     cv2.imshow("GuardianFace", cv2.flip(cv2.resize(frame, SIZES),1))

     if not fs.check_file(APP_STARTED):
          time.sleep(1)
          fs.create_file(APP_STARTED)


     # SHUTDOWN THE APP
     if fs.check_file(APP_CLOSED):
          fs.write_file(file=FACE_OUT, text=NO_PRS)
          fs.write_file(file=f"\\logs\\app\\{datetime.now().strftime('%d-%m-%Y-%H%M%S')}.log",text="Aplication ended due safe exit key\nPROCCESS ENDED")
          break

    
     cv2.waitKey(1)

fs.delete_nfiles(FACE_LOCATED, APP_STARTED, APP_CLOSED)


capture.release()
cv2.destroyAllWindows()