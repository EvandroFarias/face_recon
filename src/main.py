import os
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

while capture.isOpened():

    _ret, frame = capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_Cascade.detectMultiScale(gray,1.1,4)
    if len(faces) >= 1:
        if not fd.processing and not fd.catracaOpen:
            fd.processing = True
            cpf = asyncio.run(fd.detect_face(frame))
            if cpf:
                altera_arquivo_output(cpf)
            else:
                altera_arquivo_output(UNK_PRS)
        for x,y,h,w in faces:
            cv2.rectangle(frame,(x,y), (x+w,y+h),(237,157,9),1)
    else:
        altera_arquivo_output(NO_PRS)
        

    cv2.imshow("Guardian Face", frame)
    
    key = cv2.waitKey(1)
    if key == 115: #IF S is pressed
        print('Ending application due safe exit key')
        altera_arquivo_output(" ")
        with open(f'{DEFAULT_PATH}\\logs\\{datetime.datetime.now().strftime("%d-%m-%Y-%H%M%S")}.log', "w+") as f:
            f.write(f'Aplication ended due safe exit key \nEND OF PROCESSING AT {datetime.datetime.now().strftime("%H:%M:%S")}')
        break

    if key == 99: #IF C is pressed
        print('Guardian variable set to False')
        fd.catracaOpen = False
        altera_arquivo_output(NO_PRS)
        continue

capture.release()
cv2.destroyAllWindows()