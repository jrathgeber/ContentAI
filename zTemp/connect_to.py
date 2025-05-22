import requests
import json

API_KEY = "your_api_key_here"
BASE_URL = "https://api.bluewave.com/v1"

def make_phone_call(from_number, to_number, message):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "from": from_number,
        "to": to_number,
        "text": message
    }
    
    response = requests.post(f"{BASE_URL}/calls", headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        call_data = response.json()
        return call_data["call_id"]
    else:
        raise Exception(f"Failed to make call: {response.status_code} - {response.text}")

if __name__ == "__main__":
    from_number = "+1234567890"
    to_number = "+9876543210"
    message = "Hello, this is a test call from Bluewave API."
    
    try:
        call_id = make_phone_call(from_number, to_number, message)
        print(f"Call initiated successfully. Call ID: {call_id}")
    except Exception as e:
        print(f"Error: {str(e)}")