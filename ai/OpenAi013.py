from openai import OpenAI
import configparser

# Get Reference to Properties
config = configparser.ConfigParser()
config.read('C:\\etc\\properties.ini')


def write_article(key_words, further_info):

    # Get Reference to Properties
    config = configparser.ConfigParser()
    config.read('C:\\etc\\properties.ini')

    client = OpenAI(
        # This is the default and can be omitted
        api_key=config['openai']['api_key'],
    )

    GPT_MODEL = 'gpt-4o-mini'
    O1_MODEL = 'o3-mini'

    prepend = ""
    instructions = "Write a short medium article titled :  "
    keywords = key_words
    further_info = further_info

    prompt = prepend + " " + instructions + " " + keywords + " make sure to include these points" + further_info
    response = client.chat.completions.create(model=O1_MODEL,messages=[{"role":"user","content": prompt}])

    print(response.choices[0].message.content)

    return response.choices[0].message.content


def get_tweets( trancript):

    # Get Reference to Properties
    config = configparser.ConfigParser()
    config.read('C:\\etc\\properties.ini')

    client = OpenAI(
        # This is the default and can be omitted
        api_key=config['openai']['api_key'],
    )

    GPT_MODEL = 'gpt-4o-mini'
    # O1_MODEL = 'o3-mini'

    prepend = ""
    instructions = "Find 5 great tweets about self improvement and manifesting from the following text. Don't use emogis. Dont use exclamation marks. Just one hashtag max.   "

    prompt = instructions + " : " + trancript

    response = client.chat.completions.create(model=GPT_MODEL,messages=[{"role":"user","content": prompt}])

    print(response.choices[0].message.content)

    return response.choices[0].message.content
