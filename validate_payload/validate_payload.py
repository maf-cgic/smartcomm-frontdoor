import json
import boto3
import base64
import logging

dynamodb = boto3.client('dynamodb')
sqs = boto3.client('sqs')
table_name = 'DocumentRetentionTable'

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        template_id = body['lifeproLetter']['id']
        # Retrieve Template Selector ID from DynamoDB
        response = dynamodb.get_item(
            TableName=table_name,
            Key={
                'TemplateID': {'N': str(template_id)}
            }
        )
        if 'Item' in response:
            # Template Selector ID found
            message_body = base64.b64encode(json.dumps(body).encode()).decode()
            sqs.send_message(
                QueueUrl='DocumentGenerationQueue',
                MessageBody=message_body
            )
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Payload validated and sent to DocumentGenerationQueue.'})
            }
        else:
            # Template Selector ID not found
            logging.error("Template Selector ID not found")
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Template Selector ID not found.'})
            }
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error.'})
        }
