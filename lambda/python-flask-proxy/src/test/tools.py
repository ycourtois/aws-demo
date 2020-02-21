import logging
import os
os.environ["TZ"] = "UTC"

import boto3

context = os.getenv('CONTEXT')
TABLE = os.getenv('TABLE', default='cars')

if context == "local":
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1', endpoint_url="http://dynamodb:8000/")

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)


def describe_table():
    table = dynamodb.describe_table(
        TableName=TABLE
    )

    logger.info("Table status: ", table)


if __name__ == '__main__':
    describe_table()
