import logging
import os
from flask import Flask, request
import boto3
from botocore.exceptions import ClientError


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

    @app.route('/picture', methods=['POST'])
    def picture():
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
        json = request.get_json()
        object_name = None

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(json["file_name"])

        # Upload the file
        s3_client = boto3.client('s3')
        try:
            print("File : " + json["file_name"])
            print("Bucket : " + json["bucket"])
            print("Object name : " + object_name)
            response = s3_client.upload_file(json["file_name"], json["bucket"], object_name)
        except ClientError as e:
            logging.error(e)
            return "ERROR"
        return object_name            

    return app
