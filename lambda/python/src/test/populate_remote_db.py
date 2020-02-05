import json
import logging
import os

os.environ["TZ"] = "UTC"

import boto3

dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')

TABLE_NAME = 'tsv-bdx-demo-car'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def insert_cars():
    table = dynamodb.Table(TABLE_NAME)
    with open("cars.json") as json_file:
        cars = json.load(json_file)
        for car in cars:
            logger.info("Adding car: %s", car['model'])
            table.put_item(
                Item=car
            )


if __name__ == '__main__':
    insert_cars()
