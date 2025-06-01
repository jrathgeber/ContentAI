import requests
import json
import base64
from requests_oauthlib import OAuth1

import configparser
config = configparser.ConfigParser()
config.read('C:\\etc\\properties.ini')

# personal details
API_KEY = config['twitter']['consumer_key']
API_SECRET = config['twitter']['consumer_secret']
ACCESS_TOKEN = config['twitter']['access_token']
ACCESS_TOKEN_SECRET = config['twitter']['access_token_secret']
bearer_token = config['twitter']['bearer_token']


# OAuth1 authentication
auth = OAuth1(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)



def upload_media(image_path):
    """
    Upload media to Twitter and return media_id
    Note: Media upload still uses v1.1 endpoint
    """
    url = "https://upload.twitter.com/1.1/media/upload.json"

    temp_path = str(config['blog']['blog_temp'])

    with open(temp_path + "images\\" + image_path, 'rb') as image_file:
        files = {'media': image_file}
        response = requests.post(url, auth=auth, files=files)

    if response.status_code == 200:
        media_data = response.json()
        return media_data['media_id_string']
    else:
        print(f"Media upload failed: {response.status_code}")
        print(response.text)
        return None


def create_tweet_with_media(text, media_id):
    """
    Create a tweet with attached media using v2 API
    """
    url = "https://api.twitter.com/2/tweets"

    payload = {
        "text": text,
        "media": {
            "media_ids": [media_id]
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, auth=auth, json=payload, headers=headers)

    if response.status_code == 201:
        tweet_data = response.json()
        print("Tweet posted successfully!")
        print(f"Tweet ID: {tweet_data['data']['id']}")
        return tweet_data
    else:
        print(f"Tweet creation failed: {response.status_code}")
        print(response.text)
        return None


def post_image_tweet(image_path, tweet_text):
    """
    Complete function to post a tweet with an image
    """
    # Step 1: Upload the media
    media_id = upload_media(image_path)

    if media_id:
        # Step 2: Create tweet with media
        result = create_tweet_with_media(tweet_text, media_id)
        return result
    else:
        print("Failed to upload media")
        return None


# Example usage
if __name__ == "__main__":
    # Path to your image file
    image_file_path = "Memorial_Day_Summer_2025.jpg"

    # Your tweet text
    tweet_content = "Enjoy Memorial day X! 📸"

    # Post the tweet with image
    post_image_tweet(image_file_path, tweet_content)