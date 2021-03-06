import os

import boto3
from boto3.dynamodb.conditions import Key

context = os.getenv('CONTEXT')
TABLE = os.getenv('TABLE', default='cars')

dynamodb = boto3.resource('dynamodb')

if context == "local":
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1', endpoint_url="http://dynamodb:8000/")

cars_table = dynamodb.Table(TABLE)


def list_all():
    result = cars_table.scan()
    return result['Items']


def get(car_id):
    return cars_table.query(
        KeyConditionExpression=Key('id').eq(car_id)
    )['Items'][0]
