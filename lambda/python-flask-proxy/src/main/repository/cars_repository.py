import os

import boto3
from boto3.dynamodb.conditions import Key

context = os.getenv('CONTEXT')

dynamodb = boto3.resource('dynamodb')

if context == "local":
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1', endpoint_url="http://dynamodb:8000/")


def list_all(table: str):
    cars_table = dynamodb.Table(table)
    result = cars_table.scan()
    return result['Items']


def get(table: str, car_id: str):
    cars_table = dynamodb.Table(table)
    return cars_table.query(
        KeyConditionExpression=Key('id').eq(car_id)
    )['Items'][0]
