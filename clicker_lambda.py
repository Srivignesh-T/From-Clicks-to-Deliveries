import json
import boto3
from datetime import datetime
import base64

# Creating a DynamoDB connection
dynamodb = boto3.resource('dynamodb')
table_name = 'clicks_table'
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    for record in event['Records']:
        try:
            # Data from Kinesis are base64 encoded. Decoding the data before loading it into DynamoDB
            payload = base64.b64decode(record['kinesis']['data']).decode('utf-8')
            payload = json.loads(payload)

            # Formatting the timestamp
            timestamp = payload["Timestamp"]
            
            # Prepare item for DynamoDB
            item = {
                "UUID" : payload["UUID"],
                "tstamp": timestamp,  # Ensure correct format
                "Item_ID": payload["Item_ID"],
                "Item_Name": payload["Item_Name"],
                "Click_Counts": payload["Click_Counts"]
            }

            # Inserting the item into DynamoDB
            table.put_item(Item=item)

        except Exception as e:
            print(f"Error processing record: {e}")
            return {
                'statusCode': 500,
                'body': json.dumps(f"Error: {e}")
            }

    return {
        'statusCode': 200,
        'body': json.dumps('Data inserted successfully')
    }

