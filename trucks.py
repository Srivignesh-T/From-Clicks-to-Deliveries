import random
import requests
import json
import time
from datetime import datetime

# API URL to trigger the Lambda function
url = "https://74qy8n62db.execute-api.us-east-1.amazonaws.com/trucks_dev"

# Generating random data
truck_ids = ["TRK001", "TRK002", "TRK003"]
odometer_reading = [102345.6, 88342.1, 120567.9]
lat = [34 + round(random.random(), 6), 25 + round(random.random(), 6), 44 + round(random.random(), 6)]
lon = [100 + round(random.random(), 6), -118 + round(random.random(), 6), 128 + round(random.random(), 6)]
counter = 0

while True:
    data = {"trucks" : list()}
    tire_pressure = [i for i in range(101,131)]

    for truck in range(len(truck_ids)):
        speed = float(random.choice([i for i in range(20, 70, 5)]))
        truck_data = {
            "Truck_ID": truck_ids[truck],
            "gps_location": {
                "latitude": lat[truck] + counter,
                "longitude": lon[truck] + counter,
                "altitude": float(random.choice([i for i in range(81, 91)])),
                "speed": speed
                },
            "vehicle_speed": speed,
            "engine_diagnostics": {
                "engine_rpm": random.choice([i for i in range(2000, 3500, 100)]),
                "fuel_level": float(random.choice([i for i in range(25, 105, 5)])),
                "temperature": float(random.choice([i for i in range(85, 100, 5)])),
                "oil_pressure": float(random.choice([i for i in range(30, 50, 5)])),
                "battery_voltage": float(random.choice([i for i in range(10, 25, 5)]))
                },
            "odometer_reading": odometer_reading[truck] + counter,
            "fuel_consumption": float(random.choice([i for i in range(10, 25, 5)])),
            "vehicle_health_and_maintenance": {
                "brake_status": random.choice(["Good", "Operational", "Needs Inspection"]),
                "tire_pressure": {
                    "front_left": float(random.choice(tire_pressure)),
                    "front_right": float(random.choice(tire_pressure)),
                    "rear_left": float(random.choice(tire_pressure)),
                    "rear_right": float(random.choice(tire_pressure))
                    },
                "transmission_status": random.choice(["Good", "Operational", "Needs Inspection"])
                },
            "environmental_conditions": {
                "temperature": float(random.choice([i for i in range(15, 30)])),
                "humidity": float(random.choice([i for i in range(40, 71)])),
                "atmospheric_pressure": random.choice([1012.0, 1012.25, 1012.5, 1012.75, 1013.0, 1013.25, 1013.5])
                },
            "Effective_Date" : datetime.now().isoformat(),
            "Expiration_Date" : None,
            "is_active" : True
        }
        data["trucks"].append(truck_data)

    # Print the data structure being sent
    print("Data being sent:")
    print(json.dumps(data, indent=2))

    headers = {'Content-Type': 'application/json'}
    
    # Posting the data to the API
    response = requests.post(url, json=data, headers=headers)
    print(f"Status code: {response.status_code}")

    if response.status_code == 200:
        try:
            print(response.json())
        except json.JSONDecodeError:
            print(response.text)

        counter += 1
        time.sleep(60)
    else:
        print(f"Failed to send data. Status code: {response.status_code}")
        break