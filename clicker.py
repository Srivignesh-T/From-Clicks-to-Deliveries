import boto3
import json
import random
import os
from dotenv import load_dotenv
import time
from datetime import datetime
import uuid

# Load environment variables from .env file
load_dotenv()

access_key_id = os.getenv('ACCESS_KEY_ID')
secret_key_id = os.getenv('SECRET_ACCESS_KEY')
region = os.getenv('REGION')

# Creating a session for Kinesis
session = boto3.Session(
    aws_access_key_id=access_key_id,
    aws_secret_access_key=secret_key_id,
    region_name=region
)

client = session.client('kinesis')

# Sample data 
products = [
    {"Item_ID" : 'W1',
    "Item_Name" : "Samsung Galaxy Watch Ultra"},
    {"Item_ID" : 'W2',
    "Item_Name" : "Apple Watch Series 10"},
    {"Item_ID" : 'M1',
    "Item_Name" : "Apple IPhone 16 Pro"},
    {"Item_ID" : 'M2',
    "Item_Name" : "Asus Rog phone 6"},
    {"Item_ID" : 'L1',
    "Item_Name" : "Lenovo Legion 9i"}, 
    {"Item_ID" : 'L2',
    "Item_Name" : "Apple MacBook Air 13' 2024"}
]

# Adding random click counts and timestamp to data
while True:
    for product in products:
        Click_Counts = random.randint(5,100)
        unique_id = str(uuid.uuid4())
        payload = {
            "UUID" : unique_id,
            "Item_ID" : product["Item_ID"],
            "Item_Name" : product["Item_Name"],
            "Click_Counts" : Click_Counts,
            "Timestamp": datetime.now().isoformat()
        }
        
        # Streaming the data into kinesis
        response = client.put_record(
            StreamName = "clicksdata",
            StreamARN = "arn:aws:kinesis:us-east-1:311070527371:stream/clicksdata",
            PartitionKey = 'Item_ID',
            Data = json.dumps(payload).encode('utf-8')
        )
        
        print(f'Sent data to Kinesis: {payload}')

        # To slow down the data transmission
        time.sleep(1)