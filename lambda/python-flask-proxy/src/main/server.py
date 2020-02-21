import logging
import os
import sys

from flask import Flask
from flask_cors import CORS

import routes
from exception import exception_handling
from exception.simple_exceptions import GenericException, ErrorCode
from utility import CustomJSONEncoder


def create_app():
    print("STARTING APPLICATION ...")

    app = Flask(__name__, instance_relative_config=True)
    app.json_encoder = CustomJSONEncoder
    app.config['JSON_SORT_KEYS'] = False

    _init_config(app)
    _init_logging(app)

    CORS(app, expose_headers=['Content-Type', 'Authorization', 'Range'],
         allow_headers=['Content-Type', 'Authorization', 'Range'])

    # Exception handling
    exception_handling.register_exception_handlers(app)

    # Routes
    routes.register_routes(app)

    return app


def _init_logging(app):
    environment = app.config["ENVIRONMENT"]

    log_format = "[%(asctime)s | %(levelname)5s | %(filename)s.%(funcName)s#%(lineno)d] %(message)s"
    logging.basicConfig(format=log_format, level=logging.DEBUG if environment != "prod" else logging.INFO)

    if app.env == "production":
        app.logger.propagate = False
        if app.logger.handlers:
            for handler in app.logger.handlers:
                app.logger.removeHandler(handler)

    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(logging.Formatter(log_format))
    app.logger.addHandler(handler)


def _init_config(app):
    environment = os.getenv('ENVIRONMENT')

    if app.env == 'production':
        application = os.getenv('APPLICATION')
        project = os.getenv('PROJECT')
        app.config.from_mapping(
            DEBUG=1 if environment != "prod" else 0,
            PROPAGATE_EXCEPTIONS=environment != "prod",
            PROJECT=project,
            ENVIRONMENT=environment,
            APPLICATION=application,
            REGION=os.getenv('REGION'),
            BUCKET=os.getenv('BUCKET', f"{project}-{application}"),
            TABLE=os.getenv('TABLE', f"{project}-{application}")
        )
    else:
        app.config.from_object("config.default")
        app.config.from_object(f"config.{environment}")
        app.config.from_pyfile("local.py", silent=True)

    print('Config:', app.config)

    verify_mandatory_vars_or_fail(app.config, [
        'PROJECT',
        'ENVIRONMENT',
        'APPLICATION',
        'REGION',
        'BUCKET',
        'TABLE'
    ])


def verify_mandatory_vars_or_fail(config, env_vars: list):
    for env_var in env_vars:
        if env_var not in config or config[env_var] is None:
            raise GenericException(error_code=ErrorCode.INITIALISATION_ERROR,
                                   message=f"Env variable {env_var} is mandatory")


if __name__ == '__main__':
    create_app().run(debug=True, port=3000)
