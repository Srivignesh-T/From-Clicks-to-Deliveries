import json
import boto3
from decimal import Decimal
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def decimal_default(obj): # Function to handle Decimal serialization issues in JSON
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def convert_to_decimal(data): # Function to recursively convert floats to Decimals in nested data structures
    if isinstance(data, dict): # Convert each value in the dictionary
        return {k: convert_to_decimal(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_to_decimal(i) for i in data]
    elif isinstance(data, float): 
        return Decimal(str(data))
    return data

def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")
    try:
        # Check if 'body' exists in the event
        if 'body' not in event:
            raise KeyError("Missing 'body' in event")

        # Check if 'body' is a string or a dict and handle accordingly
        if isinstance(event['body'], str):
            body = json.loads(event['body'], parse_float=Decimal)
        else:
            body = event['body']
        
        body = convert_to_decimal(body)
        
        logger.info(f"Parsed body: {json.dumps(body, default=decimal_default)}")
        
        # Getting the expiration dates for the old records
        Expiration_date = dict()
        for truck in body["trucks"]:
            Expiration_date[truck["Truck_ID"]] = truck["Effective_Date"]

        # Creating a DynamoDB connection
        dynamodb = boto3.resource('dynamodb')
        table_name = 'trucks_table'
        table = dynamodb.Table(table_name)
        
        truck_ids = ["TRK001", "TRK002", "TRK003"]

        for truck in truck_ids:
            # Querying the table to get the existing data
            response = table.query(
                KeyConditionExpression="Truck_ID = :truck_id",
                FilterExpression="is_active = :active",
                ExpressionAttributeValues={
                    ':truck_id': truck,
                    ':active': True
                })
            
            # Updating the existing data to set Expiration date and is_active as False    
            if response['Items']:
                current_record = response['Items'][0]
                table.update_item(
                    Key={'Truck_ID': truck,},
                    UpdateExpression='SET Expiration_Date = :d, is_active = :a',
                    ExpressionAttributeValues={
                        ':d' : Expiration_date[truck],
                        ':a' : False}
                )
                
        # Inserting the new values
        for data in body["trucks"]:
            table.put_item(Item = data)
        
        return {
            'statusCode': 200,
            'headers':{
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({"message":"Data successfully updated"})
        }
    
    except KeyError as e: # Handle missing 'body' field in the event
        logger.error(f"KeyError: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps({"message": f"Bad request: {str(e)}"})
        }
    
    except Exception as e: # General error handling for other exceptions
        logger.error(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({"message":"Internal server error"})
        }
