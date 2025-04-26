import requests
import json
import os
from datetime import datetime

import configparser

# Get Reference to Properties
config = configparser.ConfigParser()
config.read('C:\\etc\\properties.ini')

# Get API key from environment variables
BEEHIIV_API_KEY = config['beehiiv']['api_key']
PUBLICATION_ID = config['beehiiv']['pub_id']

# beehiiv API base URL
API_BASE_URL = "https://api.beehiiv.com/v2"


def format_date(date_str):
    """Format ISO date string to readable format"""
    if not date_str:
        return "N/A"
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime("%B %d, %Y at %I:%M %p")
    except (ValueError, TypeError):
        return date_str


def get_posts(status=None, limit=100, page=1):
    """
    Retrieve posts from beehiiv

    Parameters:
    - status: Filter by status (draft, scheduled, published, archived) - optional
    - limit: Number of posts to return per page (max 100)
    - page: Page number for pagination

    Returns:
    - List of posts or error details
    """
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {BEEHIIV_API_KEY}"
    }

    # Build query parameters
    params = {
        "limit": limit,
        "page": page
    }

    if status:
        params["status"] = status

    endpoint = f"{API_BASE_URL}/publications/{PUBLICATION_ID}/posts"

    # Debug info
    print(f"Sending request to: {endpoint}")
    print(f"Query parameters: {params}")

    try:
        # Make the API request
        response = requests.get(
            endpoint,
            headers=headers,
            params=params
        )

        # Print response info for debugging
        print(f"Response status code: {response.status_code}")

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error response: {response.text}")
            return {"error": f"Failed to retrieve posts. Status code: {response.status_code}"}

    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}


def display_posts(posts_data):
    """Format and display posts in a readable way"""
    if "data" not in posts_data or not posts_data["data"]:
        print("No posts found.")
        return

    posts = posts_data["data"]
    total = posts_data.get("total", len(posts))

    print(f"\n=== Found {total} posts ===\n")

    for i, post in enumerate(posts, 1):
        print(f"--- Post {i} ---")
        print(f"ID: {post.get('id', 'N/A')}")
        print(f"Title: {post.get('title', 'Untitled')}")
        print(f"Subtitle: {post.get('subtitle', 'N/A')}")
        print(f"Status: {post.get('status', 'N/A').upper()}")
        print(f"Created: {format_date(post.get('created_at'))}")
        print(f"Updated: {format_date(post.get('updated_at'))}")
        print(f"Published: {format_date(post.get('published_at'))}")

        # Show URL if published
        if post.get('status') == 'published' and post.get('url'):
            print(f"URL: {post.get('url')}")

        print(f"Word count: {post.get('stats', {}).get('word_count', 'N/A')}")
        print(f"Read time: {post.get('stats', {}).get('reading_time', 'N/A')} min")

        # Show performance metrics if available
        if post.get('performance_metrics'):
            metrics = post['performance_metrics']
            print("\nPerformance:")
            print(f"  Opens: {metrics.get('opens', 'N/A')}")
            print(f"  Clicks: {metrics.get('clicks', 'N/A')}")
            print(f"  Open rate: {metrics.get('open_rate', 'N/A')}")
            print(f"  Click rate: {metrics.get('click_rate', 'N/A')}")

        print("")  # Add blank line between posts


def main():
    print("=== Beehiiv Post Lister ===")

    # Ask for optional status filter
    print("\nFilter by status (leave blank for all):")
    print("1. draft")
    print("2. scheduled")
    print("3. published")
    print("4. archived")
    status_choice = input("Enter choice (1-4) or press Enter for all: ")

    # Map input to status values
    status_map = {
        "1": "draft",
        "2": "scheduled",
        "3": "published",
        "4": "archived"
    }

    status = status_map.get(status_choice, None)

    # Get posts with optional status filter
    result = get_posts(status=status)

    if isinstance(result, dict) and "error" in result:
        print(f"Error: {result['error']}")
    else:
        display_posts(result)

        # Check if there are more pages
        if result.get("has_more", False):
            print(
                f"There are more posts available. Current page shows {len(result.get('data', []))} of {result.get('total', 'unknown')} posts.")
            print("Modify the script to change 'page' parameter for pagination if needed.")


if __name__ == "__main__":
    main()