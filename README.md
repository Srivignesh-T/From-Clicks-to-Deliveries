# From-Clicks-to-Deliveries
As an e-commerce company, our success hinges on seamlessly integrating our online platform with efficient logistics management to ensure optimal customer satisfaction and operational efficiency. To achieve this synergy, we aim to leverage real-time data streams from both our website and fleet of delivery trucks.

# Tools used
* Python
* Boto3
* API Gateway
* AWS Kinesis
* AWS Lambda Function
* AWS DynamoDB

---

# Online Platform Optimization
We analyze clickstream data to understand customer preferences, enhance user experience, and optimize marketing strategies for key product categories such as mobile phones, laptops, and watches. The following data is collected in real-time for 3 items:
* Item ID
* Item Name
* Click Count
> [!NOTE]
>  All data used here are randomly generated and simulated using the Python file 'clicker.py'

# Fleet Management and Logistics Optimization
We monitor and analyze real-time telemetry data from our fleet of delivery trucks, utilizing IoT sensors installed in each vehicle. This data helps optimize routes, reduce fuel consumption, proactively address maintenance issues, and ensure the safety and reliability of our delivery operations. For 3 trucks in the fleet, the following data is collected near real-time (data is sent every 1 minute):
* Truck ID: 3 unique IDs
* GPS Location: Latitude, Longitude, Altitude, Speed
* Vehicle Speed: Real-time speed of the vehicle
* Engine Diagnostics: Engine RPM, Fuel Level, Temperature, Oil Pressure, Battery Voltage
* Odometer Reading: Total distance traveled
* Fuel Consumption: Fuel usage over time
* Vehicle Health and Maintenance: Brake status, Tire pressure, Transmission status
* Environmental Conditions: Temperature, Humidity, Atmospheric Pressure
> [!NOTE]
> All data used here are randomly generated and simulated using the Python file 'trucks.py'

---

# Workflow
1. Clickstream Data Collection:
  * The Clickstream data is collected in real-time using AWS Kinesis.
  * Data is sent to a Lambda function for processing and storing in DynamoDB.
2. Truck IoT Data Collection:
  * Truck IoT data is collected once every minute.
  * Data is posted to an API which triggers a Lambda function and stores the data in DynamoDB.

---

> [!CAUTION]
> * Before executing the code, ensure you have the necessary packages installed in your environment.
> * Make sure you've properly edited and provided your credentials wherever required
> * All data used in this project are randomly generated using Python files.

