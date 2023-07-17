import re
import face_recognition
import cv2
import numpy as np
import json

from MongoConfig import MongoConnectionClient as db


class FaceDetection():

    conn = db('localhost', 27017)
    collection = conn.connect_to_collection('guardian', 'guardianface')

    def __init__(self):
        self.known_faces = []
        self.known_names = []
        self.known_cpfs = []

        self.frame_resizing = 0.25

    def send_face_to_guardian(self, owner, image_input):

        img = cv2.imread(image_input)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_encodings = face_recognition.face_encodings(rgb_img)[0]

        if len(img_encodings) <= 0:
            raise Exception("No recognizable face on image.")

        (name, cpf) = self.adjust_data(owner)

        record = {
            "cpf": cpf,
            "face_encoding": img_encodings.tolist()
        }

        return json.dumps(record)
        
    def save_to_mongo_collection(self, record):
        self.conn.insert_one(record)

    def load_faces(self):
        for face in self.conn.select_all():
            self.known_faces.append(face['face_encoding'])
            self.known_cpfs.append(face['cpf'])

    def detect_face(self, frame):
        try:
            # frame = cv2.imread(img)
            small_frame = cv2.resize(
                frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
            rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            face_encodings = face_recognition.face_encodings(rgb_frame)

            cpf = None

            if not self.known_faces:
                self.load_faces()

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(
                    self.known_faces, face_encoding, 0.4)
                face_distances = face_recognition.face_distance(
                    self.known_faces, face_encoding)
                best_match_index = np.argmin(face_distances)

                if True in matches:
                    cpf = self.known_cpfs[best_match_index]

            return cpf
        except Exception as ex:
            return ex

    def adjust_data(self, data: str):
        if not re.search(r'(?i)cpf', data):
            raise Exception('Incorrect file name (Missing "CPF")')
        (name, cpf) = re.split(r'(?i)cpf', data,2)
        return name, cpf