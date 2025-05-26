import requests
import configparser

# Get Reference to Properties
config = configparser.ConfigParser()
config.read('C:\\etc\\properties.ini')


def ask_live_grok_something(prompt):

    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config['Xai']['api_key']}"
    }
    payload = {
        "messages": [
            {
                "role": "system",
                "content": "State today's date at beginning. Provide a few X citations only. Be very concise. ",

                "role": "user",
                "content": prompt
            }
        ],
        "search_parameters": {
            "mode": "on"
        },
        "model": "grok-3-latest"
    }

    response = requests.post(url, headers=headers, json=payload)
    print(response.json())

    jsont = response.json()

    return jsont['choices'][0]['message']['content']


if __name__ == "__main__":

    prompt = "How is the weather looking for Memorial Day 2025 ? US Northeast only. Is it a good day for a BBQ? "

    answer = ask_live_grok_something(prompt)

    if answer:
        print(answer)