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

    def search_face_on_db(self, frame):
        small_frame = cv2.resize(
            frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_encodings = face_recognition.face_encodings(rgb_frame)

        face_locations = face_recognition.face_locations(rgb_frame)
        face_locations = np.array(face_locations)
        face_locations = face_locations / self.frame_resizing


        faces_encodings_on_db = []
        face_owners = []

        face_names = []

        for face in self.conn.select_all():
            faces_encodings_on_db.append(face['face_encoding'])
            face_owners.append(face['owner'])
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(faces_encodings_on_db, face_encoding, 0.5)
            face_distances = face_recognition.face_distance(
                faces_encodings_on_db, face_encoding)
            best_match_index = np.argmin(face_distances)
            if True in matches:
                name = face_owners[best_match_index]
                face_names.append(name)
        
        return face_locations.astype(int), face_names
 
            


    def load_encoding_images(self, images_path):
        images_path = glob.glob(os.path.join(images_path, "*.*"))

        print(f"{len(images_path)} images to encode found.")

        for img_path in images_path:

            os.rename(img_path, img_path.replace("Ç", "C").replace("Ã", "A"))
            img_path = img_path.replace("Ç", "C").replace("Ã", "A")

            img = cv2.imread(img_path)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            basename = os.path.basename(img_path)
            (filename, ext) = os.path.splitext(basename)
            outravariavel = face_recognition.face_encodings(rgb_img)
            if(outravariavel):
                img_encoding = outravariavel[0]
                self.known_face_encodings.append(img_encoding)
                self.known_face_names.append(filename)
            else:
                print(f"{filename} has no recognizable face on image")
        print(f"{len(self.known_face_encodings)} images encode loaded")


    def detect_known_faces(self, frame):
        small_frame = cv2.resize(
            frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)

        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_small_frame, face_locations)

        face_names = []

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(
                self.known_face_encodings, face_encoding, 0.4)
            name = None

            face_distances = face_recognition.face_distance(
                self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
            face_names.append(name)

        face_locations = np.array(face_locations)
        face_locations = face_locations / self.frame_resizing
        return face_locations.astype(int), face_names
