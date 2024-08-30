import requests
import json
import sys

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
    except:
        return None

    
    return type_value

if len(sys.argv) == 1:
    print("First argument must be a serial Number!")
    exit(1)  

serialNumber = sys.argv[1]
serialNumber = serialNumber.replace("-", "")


response = getProductData(serialNumber)
print("Product Data Response:")
print(json.dumps(response, indent=4, sort_keys=True))

machineType = getTypeFromJson(response)

if machineType == None:
    print("Machine type was not found!")
    exit(1)

print("\nMachine Type: " + machineType + "\n")

response = getData(serialNumber, machineType)
print("Data Response:")
print(json.dumps(response, indent=4, sort_keys=True))