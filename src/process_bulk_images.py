import glob
import re
import os
from FaceDetection import FaceDetection
from files.FilesService import FileManipulation

DEFAULT_PATH = os.path.dirname(os.path.abspath(__file__))

fd = FaceDetection()
fs = FileManipulation(DEFAULT_PATH)

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

path_to_lookup = glob.glob(os.path.join(DEFAULT_PATH+"\\Pictures", "*.jp*"))

success_text = []
errors = []

for image in path_to_lookup:
    try:
        os.rename(image.upper(), multiple_replace(dict, image.upper()))
        image = multiple_replace(dict, image)
        basename = os.path.basename(image)
        (filename, _ext) = os.path.splitext(basename)

        record = fd.send_face_to_guardian(owner=filename, image_input=image)
        success_text.append(record+"|")
    except Exception as ex:
        errors.append(f"{filename}: {ex}\n")
    finally:
        os.remove(image)
       
fs.create_file(file="bulk-image_ended.bool")

if success_text:
    fs.write_nlines_file(file="ready4db.txt", text=success_text, method="a")
if errors:
    fs.write_nlines_file(file=f'Logs\\bulk\\error.log', text=errors, method="a")