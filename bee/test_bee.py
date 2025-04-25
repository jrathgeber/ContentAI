import requests
import json
import configparser

# Get Reference to Properties
config = configparser.ConfigParser()
config.read('C:\\etc\\properties.ini')

# Get API key from environment variables
BEEHIIV_API_KEY = config['beehiiv']['api_key']
PUBLICATION_ID = config['beehiiv']['pub_id']

# beehiiv API base URL
API_BASE_URL = "https://api.beehiiv.com/v2"


def create_post(title, content, subtitle=None, slug=None, thumbnail_url=None,
                is_paid=False, is_preview_enabled=True, preview_content=None,
                status="draft"):
    """
    Create a new post on beehiiv

    Parameters:
    - title: Post title (required)
    - content: HTML content of the post (required)
    - subtitle: Optional subtitle for the post
    - slug: Custom URL slug (optional)
    - thumbnail_url: URL of thumbnail image (optional)
    - is_paid: Whether the post is for paid subscribers only
    - is_preview_enabled: Whether to enable preview for non-subscribers
    - preview_content: HTML content for the preview (required if is_preview_enabled is True)
    - status: Post status - "draft", "scheduled", or "published"

    Returns:
    - Response from the API or error details
    """

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {BEEHIIV_API_KEY}"
    }

    # Build post data
    post_data = {
        # Remove publication_id from request body
        # "publication_id": PUBLICATION_ID,
        "title": title,
        "content": content,
        "status": status,
        "settings": {
            "is_paid": is_paid,
            "is_preview_enabled": is_preview_enabled
        }
    }

    # Add optional fields if provided
    if subtitle:
        post_data["subtitle"] = subtitle
    if slug:
        post_data["slug"] = slug
    if thumbnail_url:
        post_data["thumbnail_url"] = thumbnail_url
    if preview_content and is_preview_enabled:
        post_data["settings"]["preview_content"] = preview_content

    # Updated endpoint with publication ID in the path
    endpoint = f"{API_BASE_URL}/publications/{PUBLICATION_ID}/posts"

    # Debug info
    print(f"Sending request to: {endpoint}")
    print(f"Headers: {json.dumps({k: '***' if k == 'Authorization' else v for k, v in headers.items()}, indent=2)}")
    print(f"Request body: {json.dumps(post_data, indent=2)}")

    try:
        # Make the API request
        response = requests.post(
            endpoint,
            headers=headers,
            json=post_data
        )

        # Print response info for debugging
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {response.headers}")
        print(f"Response content: {response.text}")

        # Try to parse JSON response
        if response.text.strip():
            try:
                return response.json()
            except json.JSONDecodeError:
                return {"error": "Invalid JSON response", "response_text": response.text}
        else:
            return {"error": "Empty response received"}

    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

def upload_image(file_path):
    """
    Upload an image to beehiiv

    Parameters:
    - file_path: Path to the image file

    Returns:
    - URL of the uploaded image or error details
    """
    headers = {
        "Authorization": f"Bearer {BEEHIIV_API_KEY}"
    }

    try:
        with open(file_path, 'rb') as image_file:
            files = {'file': image_file}
            response = requests.post(
                f"{API_BASE_URL}/publications/{PUBLICATION_ID}/images",
                headers=headers,
                files=files
            )

        # Print response info for debugging
        print(f"Image upload status code: {response.status_code}")
        print(f"Image upload response: {response.text}")

        if response.status_code == 200:
            return response.json().get('url')
        else:
            return {"error": f"Image upload failed with status {response.status_code}", "details": response.text}
    except Exception as e:
        return {"error": f"Image upload exception: {str(e)}"}


def verify_credentials():
    """
    Verify API credentials by checking the publication details
    """
    if not BEEHIIV_API_KEY:
        return {"error": "API key not found. Please set BEEHIIV_API_KEY in your .env file."}

    if not PUBLICATION_ID:
        return {"error": "Publication ID not found. Please set BEEHIIV_PUBLICATION_ID in your .env file."}

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {BEEHIIV_API_KEY}"
    }

    try:
        response = requests.get(
            f"{API_BASE_URL}/publications/{PUBLICATION_ID}",
            headers=headers
        )

        print(f"Credentials check status code: {response.status_code}")

        if response.status_code == 200:
            publication_data = response.json()
            print(f"Connected to publication: {publication_data.get('name', 'Unknown')}")
            return {"success": True}
        else:
            print(f"Credentials check failed. Response: {response.text}")
            return {"error": f"Failed to verify credentials. Status code: {response.status_code}"}
    except Exception as e:
        return {"error": f"Credentials check failed with exception: {str(e)}"}


def main():
    # First verify credentials
    verification = verify_credentials()
    if verification.get("error"):
        print(verification["error"])
        return

    # Sample usage
    title = "My First beehiiv Post via API"
    content = """
    <h1>Hello beehiiv World!</h1>
    <p>This is a post created using the beehiiv API and Python.</p>
    <p>You can format your content with HTML tags for rich formatting.</p>
    <ul>
        <li>Point 1</li>
        <li>Point 2</li>
        <li>Point 3</li>
    </ul>
    """

    # Uncomment to upload an image
    # image_result = upload_image("path/to/your/image.jpg")
    # if isinstance(image_result, str):  # If it's a string, it's the URL
    #     content += f'<img src="{image_result}" alt="My uploaded image" />'
    # else:
    #     print(f"Image upload failed: {image_result.get('error')}")

    # Create the post
    result = create_post(
        title=title,
        content=content,
        subtitle="Created with Python",
        status="draft"  # Set to "published" to publish immediately
    )

    if isinstance(result, dict) and "id" in result:
        print(f"Post created successfully with ID: {result['id']}")
        print(f"Status: {result.get('status', 'unknown')}")
    else:
        print(f"Error creating post: {result}")


if __name__ == "__main__":
    main()