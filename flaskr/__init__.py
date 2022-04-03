from flask import Flask
from flasgger import Swagger
from flaskr.api.routes.generation import generate_api
from flaskr.api.routes.detection import detection_api


def create_app():
    app = Flask(__name__)

    app.config['SWAGGER'] = {
        'title': 'RIA2 AWS rekognition API',
        'version': '1.0.0',
    }
    swagger = Swagger(app)

    base_api_url = '/api/v1'

    app.register_blueprint(generate_api, url_prefix=base_api_url + '/generate')

    app.register_blueprint(detection_api, url_prefix=base_api_url + '/detect')

    return app


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000,
                        type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app = create_app()

    app.run(host='0.0.0.0', port=port)
