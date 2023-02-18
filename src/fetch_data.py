import datetime
import json
import os
from MongoConfig import MongoConnectionClient as db

ORIGINAL_PATH = f"{os.path.dirname(os.path.abspath(__file__))}"

conn = db('localhost', 27017)
conn.connect_to_collection('guardian', 'guardianface')

the_date = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

def save_log(ex = None, method = None, filename = "upsert.bool"):
    with open(f'{ORIGINAL_PATH}\\etl\\logs\\{filename}', method) as f:
        if not ex:
            f.write(f'SUCCESS\n')
        else:
            f.write(f'ERROR:\n {ex} \n')
            

try:
    with open(f"{ORIGINAL_PATH}\\etl\\upsert.json", 'r') as f:
            record_list = f.read().split("|")
            for i in record_list[:len(record_list)-1]:
                j = json.loads(i)
                conn.insert_one(j)
                
            save_log(method='w')
except Exception as ex:
    save_log(ex, method='a', filename=f"error-{the_date}.log")
finally:
    if os.path.isfile(f'{ORIGINAL_PATH}\\etl\\upsert.json'):
        os.remove(f'{ORIGINAL_PATH}\\etl\\upsert.json')

# for file in os.listdir(ORIGINAL_PATH):
#     iter = os.path.join(ORIGINAL_PATH, file)
#     if ".log" in file:
#         with open(iter,'r') as f:
#             record = json.loads(f.read())
#             # fd.save_to_mongo_collection(record)