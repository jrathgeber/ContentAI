import re
import ai.ClaudeCode
import ai.XaiLive
import blog.write_blog
import mediun.create_article
import mediun.write_article
import notion.search as notnsearch
import notion.get_post as notn
import notion.Upload_data_new_2 as notdb
import twitter.gen_tweets as tw
import twitter.tweet
import twitter.post_img
import twitter.post_img_openai
import twitter.tweet_image_v2
import web.get_amazon_product
import web.get_rockbros_product_gemini
import web.get_web_article
import wordpress.Trifindr
import youtubevids.upload_video
import youtubevids.download_transcript
import emailxx.yahoo_quick_email as yahoo

from datetime import date

# Get today's Date
today = date.today()
formatted_date = today.strftime("%Y%m%d")
print("Processing " + formatted_date)

# Get the Notion page ID
url = notnsearch.search_notion_page(formatted_date)
print(url)

if url is None:
    print(f"Date {formatted_date} not in Notion pages. Check connections.")
    exit()

page_id = url.partition("-")[2]

# Connect to Notion and get today's Journal
daily_dict = notn.main(page_id)

# Medium String builder and vars
med_list = []
med_title = ""

# Yt variables
yt_title = ""
yt_path = ""
yt_desc = ""
yt_cat = ""
yt_privy = ""
yt_key = ""

# Twitter vars
tw_tweet = "nothing"


# Flags for running it. Makes easier to test.
ai_flag = True
amzn_flag = True
blog_flag = True
code_flag = True
medium_flag = True
triathlon_flag = True
twitter_flag = True
youtube_flag = True
youtube_download_flag = True
web_flag = True
send_email = True

medium_set = False
youtube_set = False
video_text = None

# Iterate the list
for key, value in daily_dict.items():

    print(f"{key}: {value}")

    if str(key).startswith("AI") and str(value) != "    " and ai_flag:
        code_task = value.lstrip()
        print(value.lstrip())

    if str(key).startswith("Code") and str(value) != "    " and code_flag:
        code_task = value.lstrip()
        ai.ClaudeCode.write_code_task(code_task)

    if str(key).startswith("Web") and str(value) != "    " and web_flag:
        web_article = value.lstrip()
        text = web.get_web_article.download_article_text(web_article)

        print(text)

        lines = text.splitlines()
        for line in lines:
            if re.match(r"^\d", line): # ^\d means "starts with a digit"
                notdb.upload_to_notion("AI Mumbo", line, "AI")

    if str(key).startswith("Amazon") and str(value) != "    " and amzn_flag:
        print("[" + str(value) + "]")
        o = web.get_amazon_product.get_product(value)
        name = o["title"].split(",", 1)[0].split("|", 1)[0].split("-", 1)[0]
        url = str(value)
        wordpress.Trifindr.create_product(url, name, str(o["title"]), o["price"], o["description"],  o["images"])

    if str(key).startswith("Rock") and str(value) != "    " and amzn_flag:
        print("[" + str(value) + "]")
        o = web.get_rockbros_product_gemini.get_rock_product(value)
        name = o["title"].split(",", 1)[0].split("|", 1)[0].split("-", 1)[0]
        url = str(value)
        wordpress.Trifindr.create_product_rock(url, name, str(o["title"]), o["price"], o["description"], o["images"])

    if str(key).startswith("Blog") and str(value) != "    " and blog_flag:
        blog.write_blog.write(value.lstrip())

    if str(key).startswith("Medium") and str(value) != "    " and medium_flag:
        if "Article : " in str(value):
            title = value.partition("Article : ")[2]
        med_list.append(value)
        medium_set = True

    if str(key).startswith("Triathlon") and str(value) != "    " and triathlon_flag:
        #wordpress.Trifindr.create_blog_post(value)
        wordpress.Trifindr.create_news_post(value)

    if str(key).startswith("Twitter") and str(value) != "    " and twitter_flag:
        twitter.tweet.tweetSomething(value)
        tw_tweet = value
        print("Tweeting ::: " + value)

    if str(key).startswith("Image") and str(value) != "    " and twitter_flag:
        img = twitter.post_img_openai.new_image(value)

        twitter.tweet_image_v2.post_image_tweet(img, value.lstrip())
        tw_tweet = value
        print("Tweeting ::: " + value)

    if str(key).startswith("Xai") and str(value) != "    " and twitter_flag:

        text = ai.XaiLive.ask_live_grok_something(value)
        twitter.tweet.tweetSomething(text)
        tw_tweet = value

        print("Tweeting ::: " + value)



    if str(key).startswith("YouTube Upload") and str(value) != "    " and youtube_flag:

        youtube_set = True

        if "Title:" in str(value):
            yt_title = value.partition("Title: ")[2]

        if "Path:" in str(value):
            yt_path = value.partition("Path: ")[2]

        if "Desc:" in str(value):
            yt_desc = value.partition("Desc: ")[2]

        if "Cat:" in str(value):
            yt_cat = value.partition("Cat: ")[2]

        if "Privy:" in str(value):
            yt_privy = value.partition("Privy: ")[2]

        if "Key:" in str(value):
            yt_key = value.partition("Key: ")[2]

    if str(key).startswith("YouTube Transcript") and str(value) != "    " and youtube_download_flag:

        yt_author = 'Nero New'
        yt_category = 'Manifest'

        print("Author ::: " + value.partition(":")[0])

        if ":" in str(value):
            yt_catagory = value.partition(":")[0]

        print("Downloading ::: " + value.partition("=")[2])
        video_text = youtubevids.download_transcript.fetch_it(value.partition("=")[2])

        print("Collecting tweets ::: " + video_text)
        tweets = tw.generate_them(video_text)
        i=0
        lines = tweets.splitlines()
        pattern = re.compile(r"^\s*(-?\d+(?:\.\d+)?|-?\.\d+)\s*(.*)")
        for line in lines:
            match = pattern.match(line)
            if match:
                number_part = match.group(1)
                text_part = match.group(2).strip('.').lstrip()
                notdb.upload_to_notion(number_part, yt_author, text_part, ['YouTube', yt_category])

if medium_flag and medium_set:

    my_ideas = "".join(med_list)

    if youtube_download_flag and video_text is not None:
        my_ideas += video_text

    print("The text : ")
    print(med_list)

    content = mediun.write_article.new_article(med_title, my_ideas)

    print("Title : " + med_title)
    print("Content : " + content)

    mediun.create_article.do_it(med_title, content)

if youtube_flag and youtube_set:

    print(f"\nYouTube upload for {yt_title} and {yt_path} and {yt_desc} and {yt_cat} and {yt_privy} and {yt_key}")
    youtubevids.upload_video.upload_video_from_batch(yt_title, yt_path, yt_desc, yt_cat, yt_privy, yt_key)

print(f"finished batch for {formatted_date}")

if send_email:
    yahoo.send_quick_message('Notion Batch has run :' + tw_tweet,
                                "ai_flag [" + str(ai_flag) + "] \n\n" +
                                "amzn_flag [" + str(amzn_flag) + "] \n\n" +
                                "blog_flag [" + str(blog_flag) + "] \n\n" +
                                "medium_flag [" + str(medium_flag) + "] \n\n" +
                                "triathlon_flag [" + str(triathlon_flag) + "] \n\n" +
                                "twitter_flag" + str(twitter_flag) + "] \n\n" +
                                "youtube_flag [" + str(youtube_flag) + "] \n\n" +
                                "youtube_download_flag [" + str(youtube_download_flag) + "] \n\n" +
                                "send_email [" + str(send_email)
                             )
