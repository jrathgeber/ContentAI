import os
from notion_client import Client
from datetime import date
import configparser


config = configparser.ConfigParser()
config.read('C:\\etc\\properties.ini')

NOTION_API_KEY=config['notion']['token']
NOTION_PAGE_ID = "237e46d2882f80a8a3a0ec88704600fe"

# Get today's Date
today = date.today()
formatted_date = today.strftime("%Y%m%d")
print("Processing " + formatted_date)

notion = Client(NOTION_API_KEY)

def update_page(page_id, new_content):
    notion.pages.update(
        page_id=page_id,
        properties={
            "title": {"title": [{"text": {"content": new_content["title"]}}]},
            "Content": {"rich_text": [{"text": {"content": new_content["content"]}}]}
        }
    )

def publish_page(page_id):
    notion.pages.update(
        page_id=page_id,
        properties={
            "Public": {"checkbox": True}
        }
    )

def main():
    page_id = NOTION_PAGE_ID
    new_content = {
        "title": "Updated Page Title",
        "content": "This is the updated content of the page."
    }

    update_page(page_id, new_content)
    publish_page(page_id)

    print(f"Page {page_id} has been updated and published.")

if __name__ == "__main__":
    main()