import boto3
from flask import Flask, jsonify

from repository import cars_repository


def register_routes(app: Flask):
    table = app.config["TABLE"]
    bucket = app.config["BUCKET"]

    @app.route('/cars', methods=['GET'])
    def get_cars():
        app.logger.info("Retrieving the car list ...")
        result = cars_repository.list_all(table)
        result = sorted(result, key=lambda k: k['id'])
        return jsonify(result)

    @app.route('/cars/car/<string:car_id>', methods=['GET'])
    def get_car(car_id: str):
        app.logger.info("Retrieving car with id %s ...", car_id)
        result = cars_repository.get(table, car_id)
        return jsonify(result)

    @app.route('/cars/files', methods=['GET'])
    def get_car_by_brand():
        app.logger.info("Retrieving cars files from bucket %s ...", bucket)
        s3_client = boto3.client('s3')
        result = s3_client.list_objects_v2(Bucket=bucket)
        files = result['Contents'] if 'Contents' in result else []
        return jsonify(files)
