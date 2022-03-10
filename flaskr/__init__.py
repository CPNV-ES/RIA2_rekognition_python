import os

from flask import Flask
from flaskr.rekognition_image_detection import RekognitionImage
from flaskr.rekognition_image_detection import usage_demo, face_demo, celebrity_demo


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

    @app.route('/rekognition_demo')
    def rekognition_usage_demo():
        return usage_demo()

    @app.route('/rekognition_face_demo')
    def rekognition_face_demo():
        return face_demo()

    # Test
    @app.route('/rekognition_celebrity_demo')
    def rekognition_celebrity_demo():
        return celebrity_demo()
    return app