import json
import boto3

# Initialize the DynamoDB resource outside the handler to leverage container reuse
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('cloud-resume-stats')

def lambda_handler(event, context):
    """
    Increments the visitor count using an atomic update expression
    and returns a CORS-compliant JSON payload.
    """
    try:
        response = table.update_item(
            Key={'ID': 'visitors'},
            UpdateExpression='ADD #c :val',
            ExpressionAttributeNames={'#c': 'count'},
            ExpressionAttributeValues={':val': 1},
            ReturnValues='UPDATED_NEW'
        )
        
        # Extract the native Decimal/Integer value from the DynamoDB attribute response
        new_count = int(response['Attributes']['count'])
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET,OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'count': new_count})
        }
        
    except Exception as e:
        print(f"Error updating item: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET,OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'error': 'Internal Server Error'})
        }