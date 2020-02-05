import datetime
import decimal
import json
import logging
import os

import boto3

from repository import car_repository

# import ptvsd

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def list_cars(event, context):
    # ptvsd.enable_attach(address=('0.0.0.0', 5590), redirect_output=True)
    # ptvsd.wait_for_attach()

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
    # ptvsd.enable_attach(address=('0.0.0.0', 5590), redirect_output=True)
    # ptvsd.wait_for_attach()

    logger.info("Event : %s", event)
    logger.info("Context is : %s", os.getenv('CONTEXT'))

    car_id = event['pathParameters']['id']
    logger.info("Retrieving car with id %s ...", car_id)
    result = car_repository.get(car_id)
    return {
        "statusCode": 200,
        "body": json.dumps(result, indent=4, cls=DecimalEncoder)
    }


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def my_json_converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


def list_bucket(event, context):
    logger.info("Event : %s", event)

    bucket = os.getenv('BUCKET')
    s3_client = boto3.client('s3')

    logger.info("Retrieving objects list from bucket %s ...", bucket)
    result = s3_client.list_objects_v2(Bucket=bucket)

    return {
        "statusCode": 200,
        "body": json.dumps(result['Contents'], indent=4, default=my_json_converter)
    }
