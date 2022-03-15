import os
from pickle import FALSE
from flask import Flask, request
from flaskr.rekognition_image_detection import face_from_url, face_from_local_file
from flask import json


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/rekognition_face_demo')
    def face_demo():
        url = "pexels-kaique-rocha-109919.jpg"
        shoulDisplayImageBoundingBox = True

        return app.response_class(
            response=face_from_local_file(url, shoulDisplayImageBoundingBox),
            status=200,
            mimetype='application/json'
        )

    @app.route('/rekognition_face/<url>')
    def rekognition_face(url):
        return app.response_class(
            response=face_from_local_file(url),
            status=200,
            mimetype='application/json'
        )

    @app.route('/rekognition_face/<url>/DisplayImage')
    def rekognition_face_show_image(url):
        return app.response_class(
            response=face_from_local_file(url, True),
            status=200,
            mimetype='application/json'
        )

    @app.errorhandler(404)
    def handle_404(e):
        return 'This route doesn\'t exist :('

    return app