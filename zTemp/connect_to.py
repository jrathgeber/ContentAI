import os
from notion_client import Client

notion = Client(auth=os.environ["NOTION_API_KEY"])

def duplicate_page(page_id):
    original_page = notion.pages.retrieve(page_id)
    
    new_page = notion.pages.create(
        parent={"database_id": original_page["parent"]["database_id"]},
        properties=original_page["properties"]
    )
    
    original_blocks = notion.blocks.children.list(page_id)
    for block in original_blocks["results"]:
        notion.blocks.children.append(
            block_id=new_page["id"],
            children=[{
                "object": "block",
                "type": block["type"],
                **block[block["type"]]
            }]
        )
    
    return new_page["id"]

if __name__ == "__main__":
    original_page_id = "your-page-id-here"
    new_page_id = duplicate_page(original_page_id)
    print(f"New page created with ID: {new_page_id}")