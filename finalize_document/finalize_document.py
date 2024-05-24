import json
import boto3
import base64
import logging

dynamodb = boto3.resource('dynamodb')
table_name = 'DocumentRetentionTable'

def lambda_handler(event, context):
    try:
        table = dynamodb.Table(table_name)
        for record in event['Records']:
            body = base64.b64decode(record['body']).decode()
            payload = json.loads(body)
            table.put_item(Item=payload)
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Metadata stored in DynamoDB.'})
        }
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error.'})
        }
