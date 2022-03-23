import os
import datetime
import tempfile
import json as js
import pandas as pd
import re

from flask import Flask, request, jsonify, json
from werkzeug.utils import secure_filename
from flaskr.aws_bucket_manager import AwsBucketManager
from flaskr.rekognition_image_detection import face_from_url, face_from_local_file


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

    @app.route('/rekognition_face_demo')
    def face_demo():
        url = "pexels-kaique-rocha-109919.jpg"
        shoulDisplayImageBoundingBox = True

        return app.response_class(response=face_from_local_file(
            url, shoulDisplayImageBoundingBox),
                                  status=200,
                                  mimetype='application/json')

    @app.route('/rekognition_face/<url>')
    def rekognition_face(url):
        return app.response_class(response=face_from_local_file(url),
                                  status=200,
                                  mimetype='application/json')

    @app.route('/rekognition_face/display_image/<url>')
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

        file_exists = aws_bucket_manager.object_exists(
            os.getenv('BUCKET_NAME'), file.filename)

        if (file_exists):
            result = 'The file already exists.', 400
        else:
            result = await aws_bucket_manager.create_object(
                os.getenv('BUCKET_NAME'), file)

        return result

    @app.route('/delete/<url>', methods=['DELETE'])
    async def remove(url):
        try:
            file_name = url
            result = await aws_bucket_manager.remove_object(
                os.getenv('BUCKET_NAME'), file_name)
        except:
            result = 'Empty filename argument', 400

        return result

    @app.route('/download/<url>', methods=['GET'])
    async def download(url):
        try:
            file_name = url
            result = await aws_bucket_manager.download_object(
                os.getenv('BUCKET_NAME'), file_name)
        except:
            result = 'An error occured.', 400

        return result

    @app.route('/api/generate/sql', methods=['POST'])
    async def generate_sql():
        content = request.get_json(silent=True)

        message = ""

        sql_text = ""

        try:
            if (not content):
                raise Exception('No content')
            if (not "bucket_url" in content or not content["bucket_url"]):
                raise Exception(r'No bucket url given, try to add "bucket_url": "s3://kfc.kentuky.com/nugget.jpg" ')
            if (not "name" in content or not content["name"]):
                raise Exception(r'No name given, try to add "name": "example_1"')
            if (not "hash" in content or not content["hash"]):
                raise Exception(r'No hash given, try to add "hash": "5683b32d9da3fe83cef1e284dc210e768d02b7cf"')
            if (not "ip" in content or not content["ip"]):
                raise Exception(r'No ip given, try to add "ip": "8.8.8.8"')
            if (not "created_at" in content or not content["created_at"]):
                raise Exception(r'No created_at given, try to add "created_at": "2018-12-25 09:27:53"')

            # add single quote before and after str
            def sq(str):
                return repr(str)

            sql_text += "INSERT INTO image VALUES (" + sq(content["bucket_url"]) +  ", " + sq(content["name"]) +  ", " + sq(content["hash"]) +  ");"
            sql_text += "INSERT INTO analyse VALUES (LAST_INSERT_ID(), " + sq(content["ip"])  + ", " + sq("2018/06/18") + ");"

            sql_text += "DECLARE @ANALYSE AS int = LAST_INSERT_ID();";
            for items in content["analyse_content"]:
                sql_text += "INSERT INTO object VALUES (@ANALYSE, 'face');"

                attribute_sql = "INSERT INTO attribute VALUES "

                for key, value in items.items():
                    attribute_sql += "(LAST_INSERT_ID(), " + sq(key) + ", " + sq(json.dumps(value)) + "),"

                sql_text += attribute_sql[:-2] + ";"

            message = [sql_text]
        except Exception as e:
            message = str(e)

        return jsonify({"message": message})

    def get_insert_query_from_df(df, dest_table):
        insert = """
        INSERT INTO `{dest_table}` (
            """.format(dest_table=dest_table)

        columns_string = str(list(df.columns))[1:-1]
        columns_string = re.sub(r' ', '\n        ', columns_string)
        columns_string = re.sub(r'\'', '', columns_string)

        values_string = ''

        for row in df.itertuples(index=False, name=None):
            values_string += re.sub(r'nan', 'null', str(row))
            values_string += ',\n'

        return insert + columns_string + ')\n     VALUES\n' + values_string[:
                                                                            -2] + ';'

    return app
