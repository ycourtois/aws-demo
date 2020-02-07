from flask import (make_response, jsonify, Flask)

from .simple_exceptions import GenericException


def register_exception_handlers(app: Flask):
    @app.errorhandler(404)
    def not_found(error):
        app.logger.error(str(error))
        return make_response(jsonify({'message': 'Not found'}), 404)

    @app.errorhandler(GenericException)
    def special_exception_handler(error: GenericException):
        app.logger.error(str(error))
        status_code = error.error_code.value.get("status_code")
        return make_response(jsonify(error.format()), status_code)

    @app.errorhandler(Exception)
    def special_exception_handler(error):
        app.logger.error(str(error))
        return make_response(jsonify({'message': 'Internal Server Error'}), 500)
