from http import HTTPStatus
import json
from flask import Blueprint, jsonify, make_response
from flasgger import swag_from
from flaskr.api.managers.rekognition_image_detection import face_from_url, face_from_local_file

detection_api = Blueprint('detection', __name__)


@detection_api.route('/face/<url>', methods=['GET'])
def rekognition_face(url):
    content = face_from_local_file(url)
    print(content)
    return make_response(jsonify(content), 200)
