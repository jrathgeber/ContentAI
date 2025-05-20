import requests
import json
import os

import configparser

config = configparser.ConfigParser()
config.read('C:\\etc\\properties.ini')

NOTION_API_KEY=config['notion']['token']
NOTION_DATABASE_ID = "1a1e46d2882f806e840af4bb89a23475"


def create_notion_page(parent_page_id, title, content=None):

    # Get Notion API token from environment variable
    notion_token = NOTION_API_KEY

    if not notion_token:
        raise ValueError("NOTION_API_TOKEN environment variable not set")

    # Notion API endpoint for creating pages
    url = "https://api.notion.com/v1/pages"

    # Headers required for Notion API
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"  # Use the current Notion API version
    }

    # Basic payload structure
    payload = {
        "parent": {
            "page_id": parent_page_id
        },
        "properties": {
            "title": {
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            }
        }
    }

    # Add content if provided
    if content:
        payload["children"] = [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": content
                            }
                        }
                    ]
                }
            }
        ]

    # Make the API request
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Check for errors
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

    return response.json()


def main():

    # Example usage
    # You'll need to replace these values with your actual Notion page IDs
    parent_id = NOTION_DATABASE_ID
    page_title = "20250520"
    page_content = "We will  get rich"

    # Create the page
    if not page_content:
        result = create_notion_page(parent_id, page_title)
    else:
        result = create_notion_page(parent_id, page_title, page_content)

    if result:
        print(f"Page created successfully!")
        print(f"Page URL: https://notion.so/{result['id'].replace('-', '')}")
    else:
        print("Failed to create page.")


if __name__ == "__main__":
    main()