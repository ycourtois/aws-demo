import json
import logging
import os

import boto3

from handler.utility import DecimalEncoder, my_json_converter
from repository import car_repository

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def list_cars(event, context):
    logger.info("Event : %s", event)
    logger.info("Context is : %s", os.getenv('CONTEXT'))

    logger.info("Retrieving the car list ...")
    result = car_repository.list_all()
    result = sorted(result, key=lambda k: k['id'])
    return {
        "statusCode": 200,
        "body": json.dumps(result, indent=4, cls=DecimalEncoder)
    }


def get_car(event, context):
    logger.info("Event : %s", event)
    logger.info("Context is : %s", os.getenv('CONTEXT'))

    car_id = event['pathParameters']['id']
    logger.info("Retrieving car with id %s ...", car_id)
    result = car_repository.get(car_id)
    return {
        "statusCode": 200,
        "body": json.dumps(result, indent=4, cls=DecimalEncoder)
    }


def list_bucket(event, context):
    logger.info("Event : %s", event)

    bucket = os.getenv('BUCKET')
    s3_client = boto3.client('s3')

    logger.info("Retrieving objects list from bucket %s ...", bucket)
    result = s3_client.list_objects_v2(Bucket=bucket)
    files = result['Contents'] if 'Contents' in result else []

    return {
        "statusCode": 200,
        "body": json.dumps(files, indent=4, default=my_json_converter)
    }
