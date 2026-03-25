import requests
import json
import os
import random
import time
from datetime import datetime


BRONZE_PATH = "data_lake/bronze/crime/"


os.makedirs(BRONZE_PATH, exist_ok=True)


locations = [
    (52.629729, 1.131592),
    (51.5074, -0.1278),   
    (53.4808, -2.2426),  
    (55.9533, -3.1883),   
    (52.4862, -1.8904)    
]


months = [
    "2023-01", "2023-02", "2023-03",
    "2023-04", "2023-05", "2023-06"
]

def extract_and_store_bronze():

    file_paths = []

    for i in range(50):  

        try:
           
            lat, lng = random.choice(locations)
            month = random.choice(months)

            url = f"https://data.police.uk/api/crimes-street/all-crime?lat={lat}&lng={lng}&date={month}"

            response = requests.get(url)

            
            if response.status_code != 200:
                print(f"❌ API failed for {lat},{lng} {month}")
                continue

            data = response.json()

            
            if not data:
                print(f"⚠️ Empty data for {lat},{lng} {month}")
                continue

           
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            file_name = f"crime_raw_{timestamp}_{i}.json"

            full_path = os.path.join(BRONZE_PATH, file_name)

            
            with open(full_path, "w") as f:
                json.dump(data, f)

            print(f"✅ Stored: {file_name} | {lat},{lng} | {month}")

            file_paths.append(full_path)

            
            time.sleep(0.2)

        except Exception as e:
            print(f"❌ Error: {e}")
            continue

    print(f"\n🔥 Total files stored in Bronze: {len(file_paths)}")

    return file_paths


if __name__ == "__main__":
    extract_and_store_bronze()