import json
import logging
import os
os.environ["TZ"] = "UTC"

import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.client('dynamodb', region_name='eu-west-1', endpoint_url="http://localhost:8000")

TABLE_NAME = 'cars'

logger = logging.getLogger()
#logging.basicConfig(level=logging.DEBUG)
logger.setLevel(logging.DEBUG)


def describe_table():
    table = dynamodb.describe_table(
        TableName=TABLE_NAME
    )

    print("Table status:", table)


if __name__ == '__main__':
    describe_table()
