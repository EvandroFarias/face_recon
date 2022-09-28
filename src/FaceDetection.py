import glob
import os
from typing import Coroutine
import face_recognition
import cv2
import asyncio
import numpy as np
from MongoConfig import MongoConnectionClient as db

class FaceDetection():

    conn = db('localhost', 27017)
    collection = conn.connect_to_collection('facedetectapp', 'facedetectapp')

    def __init__(self, img_path):
        self.known_faces = []
        self.known_names = []
        self.frame_resizing = 0.25
        self.processing = False
        self.imgs_path = glob.glob(os.path.join(
            img_path, "*.*"))

    def save_face(self, owner, image_input):
        try:
            img = cv2.imread(image_input)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_encodings = face_recognition.face_encodings(rgb_img)[0]

            record = {
                "owner": owner,
                "face_encoding": img_encodings.tolist()
            }
            self.conn.insert_one(record)
        except Exception as ex:
            return ex

    def load_faces(self):
        for person in self.conn.select_all():
            self.known_faces.append(person['face_encoding'])
            self.known_names.append(person['owner'])

    def detect_face(self, img):
        img = self.imgs_path[0]
        frame = cv2.imread(img)
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

        self.processing = True

        return name
