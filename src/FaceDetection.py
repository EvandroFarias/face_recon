from email.mime import image
import face_recognition
import cv2
import os
import glob
import numpy as np
from MongoConfig import MongoConnectionClient as db
import re


class FaceDetection():

    conn = db('localhost', 27017)
    collection = conn.connect_to_collection('facedetectapp', 'facedetectapp')

    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.frame_resizing = 0.25

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
        for face in self.conn.select_all():
            self.known_face_encodings.append(face['face_encoding'])
            self.known_face_names.append(face['owner'])


    def detect_face(self, frame):
        small_frame = cv2.resize(
            frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_encodings = face_recognition.face_encodings(rgb_frame)

        face_locations = face_recognition.face_locations(rgb_frame)
        face_locations = np.array(face_locations)
        face_locations = face_locations / self.frame_resizing

        name = None


        if not self.known_face_encodings:
            self.load_faces()

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, 0.5)
            face_distances = face_recognition.face_distance(
                self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)


            if True in matches:
                name = self.known_face_names[best_match_index]
            
        
        return name