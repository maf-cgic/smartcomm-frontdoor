import json
import boto3
import base64
import requests
import logging

sqs = boto3.client('sqs')
queue_url = 'FinalizeQueue'

def lambda_handler(event, context):
    try:
        for record in event['Records']:
            body = base64.b64decode(record['body']).decode()
            payload = json.loads(body)
            response = requests.post(
                'https://api.smartcomm.com/generate',
                json=payload
            )
            if response.status_code == 200:
                # SmartComm API dumps the document directly to S3
                sqs.send_message(
                    QueueUrl=queue_url,
                    MessageBody=base64.b64encode(json.dumps(payload).encode()).decode()
                )
                return {
                    'statusCode': 200,
                    'body': json.dumps({'message': 'Document generated and sent to FinalizeQueue.'})
                }
            else:
                logging.error(f"SmartComm API error: {response.text}")
                return {
                    'statusCode': 400,
                    'body': json.dumps({'message': 'Document generation failed.'})
                }
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error.'})
        }
