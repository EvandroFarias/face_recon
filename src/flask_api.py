import json, os
from flask import Flask, jsonify, request
from flask_cors import CORS
from shutil import copyfile
from json import dumps
from FaceDetection import FaceDetection

fd = FaceDetection()

# instantiate the app
app = Flask(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/recognition', methods=['POST'])
def recognition():
    
    image_encode = request.get_json(force=True)['image_encode']
    
    return image_encode


if __name__ == '__main__':
    app.run()