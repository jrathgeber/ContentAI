import time
import datetime
import schedule

import notion.download_data as nt
import emailxx.yahoo_quick_email as yahoo


def good_morning():

    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"Current time: {current_time}")

    tweet = nt.get_great_content_from_notion("Manifest")
    print("Tweeting :: " + tweet)
    yahoo.send_quick_message('ContentAI is Live!', tweet)


def midday_motivation():

    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"Current time: {current_time}")

    tweet = nt.get_great_content_from_notion("Manifest")
    print("Tweeting :: " + tweet)
    yahoo.send_quick_message('ContentAI is Live!', tweet)

def good_night():

    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"Current time: {current_time}")

    tweet = nt.get_great_content_from_notion("Manifest")
    print("Tweeting :: " + tweet)
    yahoo.send_quick_message('ContentAI is Live!', tweet)


# Schedule the stuff
schedule.every().day.at("08:00").do(good_morning)
schedule.every().day.at("12:00").do(midday_motivation)
schedule.every().day.at("20:00").do(good_night)

print("Scheduler started. Waiting for scheduled times...")
print("Scheduled times: 8:00 AM, 12:00 PM, and 8:00 PM")


# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
