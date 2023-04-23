import datetime
import json
import os
from MongoConfig import MongoConnectionClient as db
from files.FilesService import FileManipulation

ORIGINAL_PATH = f"{os.path.dirname(os.path.abspath(__file__))}"

fs = FileManipulation(ORIGINAL_PATH)

conn = db('localhost', 27017)
conn.connect_to_collection('guardian', 'guardianface')

the_date = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            
try:
    with open(f"{ORIGINAL_PATH}\\etl\\fetch-data\\upsert.json", 'r') as f:
        record_list = f.read().split("|")
        for i in record_list[:len(record_list)-1]:
            j = json.loads(i)
            conn.insert_one(j)
                
    fs.write_file(file="\\etl\\fetch-data\\upsert.log", text='SUCCESS')
except Exception as ex:
    fs.write_file(file="\\etl\\fetch-data\\upsert.log", text=f'ERROR:\n {ex} \n')

finally:
    fs.delete_file(f'{ORIGINAL_PATH}\\etl\\fetch-data\\upsert.json')