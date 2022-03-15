import os
import datetime
import tempfile
import json as js
import pandas as pd

from flask import Flask, request, jsonify
from flaskr.aws_bucket_manager import AwsBucketManager
import datetime
import os
from flask_restx import Api, Resource
from werkzeug.utils import secure_filename


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    api = Api(app)
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
    
    # a simple page that says hello
    @api.route('/hello', endpoint='hello')
    class HelloWorld(Resource):
        def get():
            return 'Hello, World!'

    @api.route('/upload', methods=['POST'])
    class Image(Resource):
        async def post():
            if 'file' not in request.files:
                return 'No file.', 400
        
            file = request.files['file']

            result = await aws_bucket_manager.create_object(os.getenv('BUCKET_NAME'), file) 

            return result

    @api.route('/api/generate/sql', methods=['POST'])
    class SQL(Resource):
        async def post():
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
                if(os.path.exists(tmp.name)):
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

            return insert + columns_string + ')\n     VALUES\n' + values_string[:-2] + ';'

    return app
