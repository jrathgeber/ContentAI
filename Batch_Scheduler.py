import time
import datetime
import schedule
import notion.download_data as nt

import Batch_1200pm

def midday_motivation():

    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"Current time: {current_time}")

    Batch_1200pm.do_it()


def print_current_time():

    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"Current time: {current_time}")

    Batch_1200pm.do_it()

# Schedule the tasks
schedule.every().day.at("09:30").do(print_current_time)
schedule.every().day.at("12:00").do(midday_motivation)
schedule.every().day.at("15:00").do(print_current_time)

print("Scheduler started. Waiting for scheduled times...")
print("Scheduled times: 9:10 AM, 12:00 PM, and 5:00 PM")

tweet = nt.main()

print("Tweeting :: " + tweet)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
