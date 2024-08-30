import requests
import json
import sys
import csv
import os

def getData(serialNumber, machineType):
    url = "https://pcsupport.lenovo.com/us/en/api/v4/upsell/redport/getIbaseInfo"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Content-Type": "application/json"
    }
    data = {
        "serialNumber": serialNumber,
        "machineType": machineType,
        "country": "us",
        "language": "en"
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def getProductData(serialNumber):
    url = f"https://pcsupport.lenovo.com/us/en/api/v4/mse/getproducts?productId={serialNumber}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd"
    }
    
    response = requests.get(url, headers=headers)
    return response.json()

def getTypeFromJson(response_json):
    try:
        id_field = response_json[0]['Name']
        
        last_type_index = id_field.rfind("Type")
        
        if last_type_index == -1:
            raise ValueError("No 'Type' field found in 'Name'")
        
        type_value = id_field[last_type_index:].split()[1].strip()
        
        return type_value
    except (IndexError, KeyError, AttributeError, ValueError) as e:
        print(f"Error extracting machine type: {e}")
        return None

def get_last_processed_serial(updated_file_path):
    if not os.path.exists(updated_file_path):
        return None
    
    with open(updated_file_path, mode='r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        if rows:
            return rows[-1]['SerialNumber']
    return None

if len(sys.argv) != 2:
    print("Usage: python script.py <csv_file_path>")
    exit(1)

csv_file_path = sys.argv[1]
updated_file_path = 'updated_' + csv_file_path

last_processed_serial = get_last_processed_serial(updated_file_path)
resuming = False if last_processed_serial is None else True

with open(csv_file_path, mode='r') as input_file, open(updated_file_path, mode='a', newline='') as output_file:
    reader = csv.DictReader(input_file)
    fieldnames = ['SerialNumber', 'Model', 'StartDate']
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)

    if not resuming:
        writer.writeheader()

    for row in reader:
        serialNumber = row['SerialNumber'].replace("-", "")
        
        if resuming:
            if row['SerialNumber'] == last_processed_serial:
                resuming = False
            print(serialNumber + " was skipped, as it was processed already")
            continue

        row['Model'] = '/'
        row['StartDate'] = '/'

        # Get product data
        product_response = getProductData(serialNumber)
        machineType = getTypeFromJson(product_response)

        if machineType:
            row['Model'] = machineType
            # Get additional data
            data_response = getData(serialNumber, machineType)

            if data_response.get("msg", {}).get("desc") == "Success":
                try:
                    row['StartDate'] = data_response["data"]["baseWarranties"][0]["startDate"]
                except (KeyError, IndexError):
                    row['StartDate'] = '/'

        writer.writerow(row)
        print(serialNumber + " was processed")

print("CSV file updated successfully.")
