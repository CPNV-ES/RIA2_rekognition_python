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
    aws_bucket_manager = AwsBucketManager()
    bucket_name = 'ria2.diduno.education'

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

    @app.route('/api/upload', methods=['POST'])
    async def upload():
        if 'file' not in request.files:
            return 'No file.', 400

        file = request.files['file']

        return await aws_bucket_manager.upload_file(bucket_name, file)

    @app.route('/api/delete/<url>', methods=['DELETE'])
    async def remove(url):
        file_name = url
        if await aws_bucket_manager.remove_object(bucket_name=bucket_name, object_name=file_name):
            return 'File deleted successfully.', 200
        else:
            return 'File not found.', 404

    @app.route('/api/download/<url>', methods=['GET'])
    async def download(url):
        file_name = url
        if await aws_bucket_manager.download_object(bucket_name, file_name):
            return 'File downloaded successfully.', 200
        else:
            return 'Impossible to download the file', 400

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

    @app.route('/api/request_analysis', methods=['POST'])
    async def RequestAnalysis(shouldDisplayImage=False):
        if 'file' not in request.files:
            return 'No file.', 400

        file = request.files['file']

        file_exists = aws_bucket_manager.object_exists(file.filename)

        if (file_exists):
            saveResult = 'The file already exists.', 400
        else:
            saveResult = await aws_bucket_manager.create_object(file)

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

    @app.route('/api/display_image/request_analysis', methods=['POST'])
    async def RequestAnalysisShowImage():
        return await RequestAnalysis(True)

    @app.route('/api/generate/sql', methods=['POST'])
    async def generate_sql():
        content = request.get_json(silent=True)

        try:
            if (not content):
                raise Exception("No content")
            df = pd.DataFrame(js.loads(js.dumps(content)))
            sql_text = get_insert_query_from_df(df, 'rekognition_result')

            tmp = tempfile.NamedTemporaryFile(delete=False)

            tmp.write(bytes(sql_text, 'utf-8'))
            generate_sql_filename = datetime.datetime.now().strftime(
                "%Y-%m-%d_%H-%M-%S-%f") + "_MAAAAA.sql"
            object_url = '%s/sql/%s' % (os.getenv("BUCKET_URL"),
                                        generate_sql_filename)
            if (os.path.exists(tmp.name)):
                bucket = AwsBucketManager()
                await bucket.create_object(object_url, tmp.name)

            tmp.close()
            message = object_url
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

    @app.errorhandler(404)
    def handle_404(e):
        return 'This route doesn\'t exist :('

    return app
