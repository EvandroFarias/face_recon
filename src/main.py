import os
import time
import cv2
import asyncio
from FaceDetection import FaceDetection
import datetime


UNK_PRS = "PESSOA NÃO RECONHECIDA"
NO_PRS = "SEM PESSOA"

DEFAULT_PATH = os.path.dirname(os.path.abspath(__file__))

capture = cv2.VideoCapture(0)
face_Cascade = cv2.CascadeClassifier(f'{DEFAULT_PATH}\\haarcascade_frontalface_default.xml')

fd = FaceDetection()
fd.load_faces()

def altera_arquivo_output(input):
    with open(f"{DEFAULT_PATH}\\faceoutput.txt",'w+') as f:
        f.write(input)

altera_arquivo_output(NO_PRS)

if os.path.isfile(f'{DEFAULT_PATH}\\catraca_is_closed.bool'):
    os.remove(f'{DEFAULT_PATH}\\catraca_is_closed.bool')
if os.path.isfile(f'{DEFAULT_PATH}\\catraca_is_opened.bool'):
    os.remove(f'{DEFAULT_PATH}\\catraca_is_opened.bool')
if os.path.isfile(f'{DEFAULT_PATH}\\app_started.bool'):
    os.remove(f'{DEFAULT_PATH}\\app_started.bool')

while capture.isOpened():

    catraca_open = os.path.isfile(f'{DEFAULT_PATH}\\catraca_is_opened.bool')
    app_started = os.path.isfile(f'{DEFAULT_PATH}\\app_started.bool')
    shutdown_the_app = os.path.isfile(f'{DEFAULT_PATH}\\catraca_is_closed.bool')

    _ret, frame = capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_Cascade.detectMultiScale(gray,1.1,4)
    if len(faces) >= 1:
        if not fd.processing and not catraca_open:
            fd.processing = True
            cpf = asyncio.run(fd.detect_face(frame))
            if cpf:
                altera_arquivo_output(cpf)
                with open(f'{DEFAULT_PATH}\\catraca_is_opened.bool', 'x') as f:
                    f.close
            else:
                altera_arquivo_output(UNK_PRS)
        for x,y,h,w in faces:
            cv2.rectangle(frame,(x,y), (x+w,y+h),(237,157,9),1)
    cv2.imshow("GuardianFace", cv2.resize(frame, [300,300]))

    if not app_started:
        time.sleep(1)
        with open(f'{DEFAULT_PATH}\\app_started.bool', 'x') as f:
            f.close        
    
    if shutdown_the_app:
        altera_arquivo_output(" ")
        with open(f'{DEFAULT_PATH}\\logs\\{datetime.datetime.now().strftime("%d-%m-%Y-%H%M%S")}.log', "w+") as f:
            f.write(f'Aplication ended due safe exit key \nPROCCESS ENDED AT {datetime.datetime.now().strftime("%H:%M:%S")}')
        break

    key = cv2.waitKey(1)
    # if key == 115: #IF S is pressed
    #     print('Ending application due safe exit key')
    #     altera_arquivo_output(" ")
    #     with open(f'{DEFAULT_PATH}\\logs\\{datetime.datetime.now().strftime("%d-%m-%Y-%H%M%S")}.log', "w+") as f:
    #         f.write(f'Aplication ended due safe exit key \nPROCCESS ENDED AT {datetime.datetime.now().strftime("%H:%M:%S")}')
    #     break
    # if key == 99: #IF C is pressed
    #     print('Guardian variable set to False')
    #     fd.catracaOpen = False
    #     altera_arquivo_output(NO_PRS)
    #     continue

if os.path.isfile(f'{DEFAULT_PATH}\\app_started.bool'):
    os.remove(f'{DEFAULT_PATH}\\app_started.bool')
if os.path.isfile(f'{DEFAULT_PATH}\\catraca_is_opened.bool'):
    os.remove(f'{DEFAULT_PATH}\\catraca_is_opened.bool')

capture.release()
cv2.destroyAllWindows()