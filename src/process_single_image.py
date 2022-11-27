from datetime import date
import sys
import re
import shutil
import os

from FaceDetection import FaceDetection

ORIGINAL_PATH = sys.argv[1]
DEST_PATH = 'guardianface\\process_single_image\\processing-image\\'

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

filename = date.today()

def multiple_replace(dict, text):
    regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))
    return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text)

excGiven = False

try:
    img_to_process = None
    img_to_process = shutil.copy(ORIGINAL_PATH, DEST_PATH)

    os.rename(img_to_process.upper(), multiple_replace(dict, img_to_process.upper()))
    img_to_process = multiple_replace(dict, img_to_process)

    basename = os.path.basename(img_to_process)
    (filename, _ext) = os.path.splitext(basename)

    fd.save_face(filename, img_to_process)
except Exception as ex:
    excGiven = ex
finally:
    f = open(f'{DEST_PATH}logs\\{filename}.log',"w+")
    if excGiven:
        f.write(f"\nERROR:\n {excGiven}")
    else:
        f.write(f"SUCCESS")
    
    f.close()

    if img_to_process:
        os.remove(img_to_process)