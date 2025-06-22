import time
import datetime
import schedule
import notion.download_data as nt
import emailxx.yahoo_quick_email as yahoo
import twitter.tweet
import twitter.tweet_image_v2
import twitter.post_img_openai
import notion.create_page_and_conent


def get_up():

    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"Current time: {current_time}")

    notion.create_page_and_conent.setup_notion_page("205e46d2882f80fc83c8f96ddd628db3")


def good_morning():

    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"Current time: {current_time}")

    tweet = nt.get_great_content_from_notion("Manifest")
    print("Tweeting :: " + tweet)
    yahoo.send_quick_message('ContentAI is Live!', tweet)

    twitter.tweet.tweetSomething(tweet)


def midday_motivation():

    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"Current time: {current_time}")

    empty_tweet = nt.get_great_content_from_notion("Snack Link")
    tweet = "https://www.trifindr.com/product/honey-stinger-organic-fruit-smoothie-energy-chew/"

    print("Tweeting :: " + tweet)
    yahoo.send_quick_message('Lunchtime snack pump', tweet)
    twitter.tweet.tweetSomething("Lunch time. I am snacking on :  " + tweet)


def good_night():

    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"Current time: {current_time}")

    fact = nt.get_great_content_from_notion("Astronomy")
    img = twitter.post_img_openai.new_image(fact)

    tweet = "Good night X : Something to think about to help you drift off : " + fact

    twitter.tweet_image_v2.post_image_tweet(img, tweet.lstrip())

    print("Tweeting :: " + tweet)
    yahoo.send_quick_message('ContentAI is going to bed!', tweet)

    # exit
    exit_script()


def exit_script():
    print("Exiting the script")
    exit()

#get_up()

# Schedule the stuff
schedule.every().day.at("07:00").do(get_up)
schedule.every().day.at("08:00").do(good_morning)
#schedule.every().day.at("12:00").do(midday_motivation)
schedule.every().day.at("22:15").do(good_night)


print("Scheduler started. Waiting for scheduled times...")
print("Scheduled times: 8:00 AM, 12:00 PM, and 8:00 PM")


# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
