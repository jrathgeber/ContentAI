from openai import OpenAI
import configparser

# Get Reference to Properties
config = configparser.ConfigParser()
config.read('C:\\etc\\properties.ini')


def write_article(key_words, further_info):

    client = OpenAI(
        # This is the default and can be omitted
        api_key=config['openai']['api_key'],
    )

    GPT_MODEL = 'gpt-4o-mini'
    #GPT_MODEL = 'o1-mini'

    prepend = "Answer should be embedded in html tags and that's it. Nothing else. No quotes"
    instructions = "Write a short blog post titled :  "
    keywords = key_words
    further_info = further_info

    prompt = prepend + " " + instructions + " " + keywords + " " + further_info
    response = client.chat.completions.create(model=GPT_MODEL,messages=[{"role":"user","content": prompt}])

    print(response.choices[0].message.content)

    return response.choices[0].message.content
