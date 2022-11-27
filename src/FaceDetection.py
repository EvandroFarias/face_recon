import face_recognition
import cv2
import numpy as np
from MongoConfig import MongoConnectionClient as db


class FaceDetection():

    conn = db('localhost', 27017)
    collection = conn.connect_to_collection('facedetectapp', 'facedetectapp')

    def __init__(self):
        self.known_faces = []
        self.known_names = []
        self.frame_resizing = 0.25
        self.processing = False
        self.catracaOpen = False

    def save_face(self, owner, image_input):

        img = cv2.imread(image_input)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_encodings = face_recognition.face_encodings(rgb_img)[0]

        if len(img_encodings) <= 0:
            raise Exception("No recognizable face on image.")

        record = {
            "owner": owner,
            "face_encoding": img_encodings.tolist()
        }
        self.conn.insert_one(record)

    def load_faces(self):
        for face in self.conn.select_all():
            self.known_faces.append(face['face_encoding'])
            self.known_names.append(face['owner'])

    async def detect_face(self, frame):
        try:
            # frame = cv2.imread(img)
            small_frame = cv2.resize(
                frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
            rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            face_encodings = face_recognition.face_encodings(rgb_frame)

            name = None

            if not self.known_faces:
                self.load_faces()

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(
                    self.known_faces, face_encoding, 0.4)
                face_distances = face_recognition.face_distance(
                    self.known_faces, face_encoding)
                best_match_index = np.argmin(face_distances)

                if True in matches:
                    name = self.known_names[best_match_index]
                    self.catracaOpen = True

            self.processing = False

            return name
        except Exception as ex:
            return ex
