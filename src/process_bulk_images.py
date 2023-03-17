import datetime
import glob
import re
import os
from FaceDetection import FaceDetection
from files.FilesService import FileManipulation

DEFAULT_PATH = os.path.dirname(os.path.abspath(__file__))

fd = FaceDetection()
fs = FileManipulation(DEFAULT_PATH)

the_date = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

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

path_to_lookup = glob.glob(os.path.join(DEFAULT_PATH+"\\Fotos", "*.jp*"))

to_create_file = []

for image in path_to_lookup:
    try:
        os.rename(image.upper(), multiple_replace(dict, image.upper()))
        image = multiple_replace(dict, image)

        basename = os.path.basename(image)
        (filename, _ext) = os.path.splitext(basename)

        record = fd.send_face_to_guardian(owner=filename, image_input=image)
        to_create_file.append(record+"|")
    except Exception as ex:
        fs.write_file(file=f'logs\\{filename.replace(" ","")}-{the_date}.log', text=f'{basename}: {str(ex)}')
        
fs.write_nlines_file(file="ready_for_db.txt", text=to_create_file)
