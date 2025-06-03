import os
import random
from notion_client import Client


import configparser

config = configparser.ConfigParser()
config.read('C:\\etc\\properties.ini')

NOTION_API_KEY=config['notion']['token']
NOTION_DATABASE_ID = "1ebe46d2882f807d966cfbc286fe31d1"

# Option 2: Hardcode (less secure, use for quick testing only)
# NOTION_API_KEY = "secret_YOUR_INTEGRATION_TOKEN"
# NOTION_DATABASE_ID = "YOUR_DATABASE_ID"

# --- Field Names in your Notion Database ---
# IMPORTANT: These MUST match the exact names of your properties in Notion.
# Case-sensitive!

TITLE_FIELD = "Name"        # Or "Title", "Topic", etc. - The main title property
DATE_FIELD = "Date"         # The name of your Date property
TAGS_FIELD = "Tags"         # The name of your Multi-select property for tags
TWEET_FIELD = "Tweet"       # The name of your Rich Text or Text property for the tweet
AUTHOR_FIELD = "Author"     # The name of your Rich Text or Text property for the tweet


def get_property_value(page_properties, prop_name, prop_type):
    """Helper function to safely extract property values."""
    prop = page_properties.get(prop_name)
    if not prop:
        # print(f"Warning: Property '{prop_name}' not found.")
        return None

    if prop_type == "title":
        return prop["title"][0]["plain_text"] if prop["title"] else None
    elif prop_type == "date":
        return prop["date"]["start"] if prop["date"] else None
    elif prop_type == "multi_select":
        return [tag["name"] for tag in prop["multi_select"]]
    elif prop_type == "rich_text":
        return "".join([rt_item["plain_text"] for rt_item in prop["rich_text"]])
    else:
        # print(f"Warning: Unsupported property type '{prop_type}' for '{prop_name}'.")
        return None


def fetch_all_database_items(notion_client, database_id):
    """Fetches all items from a Notion database, handling pagination."""
    all_items = []
    has_more = True
    start_cursor = None

    print(f"Fetching items from database ID: {database_id}...")
    while has_more:
        try:
            response = notion_client.databases.query(
                database_id=database_id,
                start_cursor=start_cursor
                # You can add filters or sorts here if needed
                # filter={"property": "Status", "select": {"equals": "Done"}}
            )
        except Exception as e:
            print(f"Error querying database: {e}")
            return [] # Return empty list on error

        results = response.get("results", [])
        for page in results:
            properties = page.get("properties", {})
            item_data = {
                "id": page.get("id"),
                "title": get_property_value(properties, TITLE_FIELD, "title"),
                "date": get_property_value(properties, DATE_FIELD, "date"),
                "tags": get_property_value(properties, TAGS_FIELD, "multi_select"),
                "tweet": get_property_value(properties, TWEET_FIELD, "rich_text"),
                "author": get_property_value(properties, AUTHOR_FIELD, "rich_text"),
            }
            all_items.append(item_data)

        has_more = response.get("has_more", False)
        start_cursor = response.get("next_cursor")
        if has_more:
            print(f"Fetched {len(results)} items, more available...")

    print(f"Total items fetched: {len(all_items)}")
    return all_items


def get_great_content_from_notion(category):

    if category == 'Astronomy':
        NOTION_DATABASE_ID = "1f7e46d2882f801392ddc8b9d9653546"

    if category == 'Manifest':
        NOTION_DATABASE_ID = "1ebe46d2882f807d966cfbc286fe31d1"

    if not NOTION_API_KEY or not NOTION_DATABASE_ID:
        print("Error: NOTION_API_KEY or NOTION_DATABASE_ID not set.")
        print("Please set them as environment variables or in the script.")
        return

    # Initialize Notion client
    try:
        notion = Client(auth=NOTION_API_KEY)
        # Test connection by trying to retrieve the database (optional, but good check)
        notion.databases.retrieve(database_id=NOTION_DATABASE_ID)
        print("Successfully connected to Notion and found the database.")
    except Exception as e:
        print(f"Error initializing Notion client or accessing database: {e}")
        print("Check your API key, database ID, and if the integration has access to the database.")
        return

    # Fetch all items from the database
    database_items = fetch_all_database_items(notion, NOTION_DATABASE_ID)

    if not database_items:
        print("No items found in the database or an error occurred.")
        return

    # Select one item at random
    random_item = random.choice(database_items)

    # Print the random item
    print("\n--- Randomly Selected Item ---")
    print(f"ID:    {random_item.get('id', 'N/A')}")
    print(f"Author: {random_item.get('author', 'N/A')}")
    print(f"Title: {random_item.get('title', 'N/A')}")
    print(f"Date:  {random_item.get('date', 'N/A')}")
    print(f"Tags:  {', '.join(random_item.get('tags', [])) if random_item.get('tags') else 'N/A'}")
    print(f"Tweet: {random_item.get('tweet', 'N/A')}")
    print("----------------------------")

    return random_item.get('tweet', 'nothing')


if __name__ == "__main__":
    get_great_content_from_notion("Astronomy")
