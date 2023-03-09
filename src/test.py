from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import os
import time
import cv2
from FaceDetection import FaceDetection
from files.FilesService import FileManipulation

DEFAULT_PATH = os.path.dirname(os.path.abspath(__file__))

UNK_PRS = "PESSOA NÃO RECONHECIDA"
NO_PRS = "SEM PESSOA"

CATRACA_CLOSED = "catraca_is_closed.bool"
CATRACA_OPENED = "catraca_is_opened.bool"
APP_STARTED = "app_started.bool"

FACE_OUT = "faceoutput.txt"

capture = cv2.VideoCapture(0)
face_Cascade = cv2.CascadeClassifier(f'{DEFAULT_PATH}\\haarcascade_frontalface_default.xml')

fs = FileManipulation(DEFAULT_PATH)
fd = FaceDetection()
fd.load_faces()

fs.delete_nfiles(CATRACA_CLOSED, CATRACA_OPENED, APP_STARTED)

def recognize_face(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_Cascade.detectMultiScale(gray,1.1,4)
    if len(faces) > 0 and not fs.check_file(CATRACA_OPENED):
        cpf = fd.detect_face(frame)
        if cpf:
            fs.write_file(file=FACE_OUT, text=cpf)
            fs.create_file(CATRACA_OPENED)
        else:
            fs.write_file(file=FACE_OUT, text=UNK_PRS)       
    for x, y, h, w in faces:
        if cpf:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        else:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 3)
    return frame

def handle_camera():
    while True:
        _success, frame = capture.read()
        if not _success:
            # Ignorando frame vazio
            continue
        frame = cv2.flip(cv2.resize(frame, [300, 300]), 1)
        frame = recognize_face(frame)
        cv2.imshow("GuardianFace", frame)
        if not fs.check_file(APP_STARTED):
            time.sleep(1)
            fs.create_file(APP_STARTED)
        if fs.check_file(CATRACA_CLOSED):
            fs.write_file(file=FACE_OUT, text=NO_PRS)
            fs.write_file(file=f"\\logs\\{datetime.now().strftime('%d-%m-%Y-%H%M%S')}.log",
                          text="Aplication ended due safe exit key\nPROCCESS ENDED")
            break
        cv2.waitKey(1)
        
with ThreadPoolExecutor(max_workers=2) as executor:
    executor.submit(handle_camera)
    executor.submit(fd.load_faces)

fs.delete_nfiles(CATRACA_OPENED, APP_STARTED, CATRACA_CLOSED)

capture.release()
cv2.destroyAllWindows()
