import os
from notion_client import Client

notion = Client(auth=os.environ["NOTION_TOKEN"])

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
    page_id = "your_page_id_here"
    new_content = {
        "title": "Updated Page Title",
        "content": "This is the updated content of the page."
    }

    update_page(page_id, new_content)
    publish_page(page_id)

    print(f"Page {page_id} has been updated and published.")

if __name__ == "__main__":
    main()