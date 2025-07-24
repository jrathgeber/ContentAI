import tweepy
import time

# Twitter API credentials
consumer_key = "YOUR_CONSUMER_KEY"
consumer_secret = "YOUR_CONSUMER_SECRET"
access_token = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def like_new_tweets():
    followers = api.get_followers()
    for follower in followers:
        tweets = api.user_timeline(user_id=follower.id, count=10)
        for tweet in tweets:
            if not tweet.favorited:
                try:
                    api.create_favorite(tweet.id)
                    print(f"Liked tweet: {tweet.text}")
                    time.sleep(2)  # Add delay to avoid rate limiting
                except tweepy.TweepError as e:
                    print(f"Error liking tweet: {e}")

if __name__ == "__main__":
    while True:
        like_new_tweets()
        print("Waiting for 15 minutes before checking for new tweets...")
        time.sleep(900)  # Wait for 15 minutes before checking again