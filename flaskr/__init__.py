from enum import Enum
import os
import datetime
import tempfile
import json as js
import pandas as pd
import re
from pypika import MySQLQuery as Query, Table, CustomFunction
from flask import Flask, request, jsonify, json
from werkzeug.utils import secure_filename
from flaskr.aws_bucket_manager import AwsBucketManager
from flaskr.rekognition_image_detection import face_from_url, face_from_local_file


class AttributeType(Enum):
    STRING = 0
    NUMBER = 1
    BOOLEAN = 2
    NONE = -1

    @classmethod
    def type(cls, value):
        if (value is str):
            return AttributeType.STRING
        elif (value is float or value is int):
            return AttributeType.NUMBER
        elif (value is bool):
            return AttributeType.BOOLEAN
        else:
            return AttributeType.NONE


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    aws_bucket_manager = AwsBucketManager()

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

    @app.route('/api/detect/face/<url>')
    def rekognition_face(url):
        return app.response_class(response=face_from_local_file(url),
                                  status=200,
                                  mimetype='application/json')
      
    @app.route('/api/detect/face/<url>/<args>')
    def rekognition_face_args(url, args):
        return app.response_class(response=face_from_local_file(url, False, args),
                                  status=200,
                                  mimetype='application/json')

    @app.route('/api/detect/face/display_image/<url>')
    def rekognition_face_show_image(url):
        return app.response_class(response=face_from_local_file(url, True),
                                  status=200,
                                  mimetype='application/json')

    @app.errorhandler(404)
    def handle_404(e):
        return 'This route doesn\'t exist :('

    @app.route('/upload', methods=['POST'])
    async def upload():
        if 'file' not in request.files:
            return 'No file.', 400

        file = request.files['file']

        await aws_bucket_manager.upload_file(file)

        # ISSUE : Always return False but it's working
        """ if await aws_bucket_manager.upload_file(file):
            return 'File uploaded successfully.', 200
        else:
            return 'Upload failed.', 400 """

        return 'File uploaded successfully.', 200

        # TODO send link to face detector, facedetect(link, params)

    @app.route('/api/request_analysis', methods=['POST'])
    async def RequestAnalysis(shouldDisplayImage=False):
        if 'file' not in request.files:
            return 'No file.', 400

        file = request.files['file']

        file_exists = aws_bucket_manager.object_exists(
            os.getenv('BUCKET_NAME'), file.filename)

        if (file_exists):
            saveResult = 'The file already exists.', 400
        else:
            saveResult = await aws_bucket_manager.create_object(
                os.getenv('BUCKET_NAME'), file)

        print(saveResult)

        # If the insert is a success
        if saveResult == True:
            downloadResult = await download(file.filename)
        else:
            return app.response_class('Impossible to download the file', 500)

        # If the download is a success
        if downloadResult == True:
            return app.response_class(response=face_from_local_file(file.filename, shouldDisplayImage),
                                      status=200,
                                      mimetype='application/json')
        else:
            return app.response_class('Impossible to rekognise the face', 500)

        return app.response_class('An error has occured', 500)

    @app.route('/api/display_image/request_analysis', methods=['POST'])
    async def RequestAnalysisShowImage():
        return await RequestAnalysis(True)

    @app.route('/delete/<url>', methods=['DELETE'])
    async def remove(url):
        file_name = url
        if await aws_bucket_manager.remove_object(file_name):
            return 'File deleted successfully.', 200
        else:
            return 'File not found.', 404

    @app.route('/download/<url>', methods=['GET'])
    async def download(url):
        file_name = url
        if await aws_bucket_manager.download_object(file_name):
            return 'File downloaded successfully.', 200
        else:
            return 'Impossible to download the file', 400

    @app.route('/api/generate/sql', methods=['POST'])
    async def generate_sql():
        content = request.get_json(silent=True)

        message = ""

        sql_text = ""

        try:
            if (not content):
                raise Exception('No content')
            if (not "bucket_url" in content or not content["bucket_url"]):
                raise Exception(
                    r'No bucket url given, try to add "bucket_url": "s3://kfc.kentuky.com/nugget.jpg" ')
            if (not "name" in content or not content["name"]):
                raise Exception(
                    r'No name given, try to add "name": "example_1"')
            if (not "hash" in content or not content["hash"]):
                raise Exception(
                    r'No hash given, try to add "hash": "5683b32d9da3fe83cef1e284dc210e768d02b7cf"')
            if (not "ip" in content or not content["ip"]):
                raise Exception(r'No ip given, try to add "ip": "8.8.8.8"')
            if (not "created_at" in content or not content["created_at"]):
                raise Exception(
                    r'No created_at given, try to add "created_at": "2018-12-25 09:27:53"')

            image = Table('image')
            analysis = Table('analysis')
            object = Table('object')
            attribute = Table('attribute')

            q = Query.into(image).columns('url', 'name', 'hash').insert(
                content["bucket_url"], content["name"], content["hash"])

            sql_text = str(q) + ";"

            sql_text += "SET @IMAGE = LAST_INSERT_ID();"

            ip_sql_function = CustomFunction('INET_ATON', ['ip'])
            apocalypse_now_sql_function = CustomFunction('NOW')

            q = Query.into(analysis).columns('image_id', 'ip', 'created_at', 'updated_at').insert('@IMAGE',
                                                                                                  ip_sql_function(content["ip"]), content["created_at"], apocalypse_now_sql_function())
            # workaround to remove default quote wrapper to use @IMAGE variable
            sql_text += str(q).replace("'@IMAGE'", "@IMAGE") + ";"

            sql_text += "SET @ANALYSIS = LAST_INSERT_ID();"

            for analyzed_item in content["analysis_content"]:
                q = Query.into(object).columns('analysis_id', 'name', 'category').insert(
                    '@ANALYSIS', 'face_object', 'face')
                sql_text += str(q).replace("'@ANALYSIS'", "@ANALYSIS") + ";"
                sql_text += "SET @OBJECT = LAST_INSERT_ID();"

                for object_key, object_value in analyzed_item.items():

                    object_value_type = type(object_value)

                    def get_attribute_insert_query(name, type: AttributeType, value):
                        value_array = [None] * 3
                        value_array[type.value] = str(
                            value) if value is not None else None
                        q = Query.into(attribute).columns('object_id', 'name', 'value_type', 'value_string', 'value_number', 'value_boolean').insert(
                            '@OBJECT', name, type.name.lower(), value_array[0], value_array[1], value_array[2])
                        return str(q).replace("'@OBJECT'", "@OBJECT") + ";"

                    if (object_value_type is dict):
                        for attribute_key, attribute_value in object_value.items():
                            attribute_value_type = AttributeType.type(
                                type(attribute_value))

                            name = object_key + '.' + attribute_key
                            sql_text += get_attribute_insert_query(
                                name, attribute_value_type, attribute_value)
                    elif object_value_type is list:
                        for subobject_key in range(0, len(object_value)):
                            if type(object_value[subobject_key]) is dict:
                                for attribute_key, attribute_value in object_value[subobject_key].items():
                                    attribute_value_type = AttributeType.type(
                                        type(attribute_value))

                                    name = object_key + '.' + \
                                        str(subobject_key) + \
                                        '.' + attribute_key
                                    sql_text += get_attribute_insert_query(
                                        name, attribute_value_type, attribute_value)
                            else:
                                attribute_value_type = AttributeType.type(
                                    type(object_value[subobject_key]))

                                name = object_key
                                sql_text += get_attribute_insert_query(
                                    name, attribute_value_type, object_value[subobject_key])
                    else:

                        attribute_value_type = AttributeType.type(
                            object_value_type)
                        name = object_key
                        sql_text += get_attribute_insert_query(
                            name, attribute_value_type, object_value)
            message = sql_text

        except Exception as e:
            message = str(e)

        return message

    return app
