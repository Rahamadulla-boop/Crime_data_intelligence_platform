import requests
import json
from datetime import datetime
import time
import os

URL = "https://data.police.uk/api/crimes-street/all-crime?lat=52.629729&lng=1.131592"

BRONZE_PATH = "data_lake/bronze/crime/"   \

def extract_crime_data():

    
    os.makedirs(BRONZE_PATH, exist_ok=True)

    file_names = []

    for i in range(50):

        response = requests.get(URL)
        data = response.json()

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        file_name = f"crime_raw_{timestamp}_{i}.json"
        full_path = os.path.join(BRONZE_PATH, file_name)

        
        with open(full_path, "w") as f:
            json.dump(data, f)

        print(f"Created in Bronze: {full_path}")

        file_names.append(full_path)

        time.sleep(0.1)

    return file_names