import requests
import json
from datetime import datetime

import configparser

config = configparser.ConfigParser()
config.read('C:\\etc\\properties.ini')

token = config['notion']['token']

NOTION_TOKEN = token
DATABASE_ID = "1ebe46d2882f807d966cfbc286fe31d1"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}


def upload_to_notion(title, content, tags):
    url = f"https://api.notion.com/v1/pages"

    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Title": {"title": [{"text": {"content": title}}]},
            "Tags": {"multi_select": [{"name": tag} for tag in tags]},
            "Date": {"date": {"start": datetime.now().isoformat()}}
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": content}}]
                }
            }
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    print(response.json())

    return response.json()


if __name__ == "__main__":

    title = "Sample Notion Post"
    content = "This is a sample post uploaded via the Notion API."
    tags = ["sample", "api", "python"]

    result = upload_to_notion(title, content, tags)
    print(f"Page created: {result.get('url', 'Error: Page not created')}")