from datetime import date
import datetime
import sys
import re
import shutil
import os
from files.FilesService import FileManipulation

from FaceDetection import FaceDetection

#ORIGINAL_PATH = "C:\\Users\\Sasuk\\Desktop\\EVANDRO CPF154515454.jpg"

ORIGINAL_PATH = ' '.join(sys.argv[1:len(sys.argv)])
CPF_DO_INPUT, _ext = os.path.splitext(ORIGINAL_PATH.split("CPF")[1])
DEST_PATH = os.path.dirname(os.path.abspath(__file__))

fd = FaceDetection()
fs = FileManipulation(DEST_PATH)

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

try:
    img_to_process = None
    img_to_process = shutil.copy(ORIGINAL_PATH, DEST_PATH+"\\processing-image\\")

    os.rename(img_to_process.upper(), multiple_replace(dict, img_to_process.upper()))
    img_to_process = multiple_replace(dict, img_to_process)

    basename = os.path.basename(img_to_process)
    (filename, _ext) = os.path.splitext(basename)

    record = fd.send_face_to_guardian(filename, img_to_process)

    fs.write_file(file=f'\\etl\\single-image\\{CPF_DO_INPUT}.log', text=record)
except Exception as ex:
    fs.write_file(file=f'\\etl\\single-image\\{CPF_DO_INPUT}.log', text=f'ERROR:\n [{datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}]: \n {ex} \n')

finally:
    fs.delete_file(img_to_process)