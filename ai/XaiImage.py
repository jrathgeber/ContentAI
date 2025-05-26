import requests
import configparser

config = configparser.ConfigParser()
config.read('C:\\etc\\properties.ini')


api_key = config['Xai']['api_key']
url = "https://api.x.ai/v1/images/generations"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
payload = {
    "model": "grok-2-image-1212",
    "prompt": "Memorial Day 2025 US Flag Happy Family having a BBQ",
    "n": 1
}

response = requests.post(url, headers=headers, json=payload)
if response.status_code == 200:
    data = response.json()
    print("Image URL:", data["data"][0]["url"])
else:
    print(f"Error: {response.status_code}")
