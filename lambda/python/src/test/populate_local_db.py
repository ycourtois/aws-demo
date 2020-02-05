import json
import logging
import os
os.environ["TZ"] = "UTC"

import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb', region_name='eu-west-1', endpoint_url="http://localhost:8000")

TABLE_NAME = 'cars'

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)


def insert_cars():
    table = dynamodb.Table(TABLE_NAME)
    with open("cars.json") as json_file:
        cars = json.load(json_file)
        for car in cars:
            logger.info("Adding car: %s", car['model'])
            table.put_item(
                Item=car
            )


def create_table():
    table = dynamodb.create_table(
        TableName=TABLE_NAME,
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            }
        ],
        BillingMode='PAY_PER_REQUEST'
    )

    print("Table status:", table.table_status)


if __name__ == '__main__':
    try:
        create_table()
    except ClientError as ce:
        if ce.response['Error']['Code'] == 'ResourceInUseException':
            logger.warning(f"Table [{TABLE_NAME}] may already exist, skipping ...")
        else:
            logger.error(ce)

    insert_cars()
