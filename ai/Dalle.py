import openai
from openai import OpenAI
import configparser


def create_image(key_words):

    # Get Reference to Properties
    config = configparser.ConfigParser()
    config.read('C:\\etc\\properties.ini')

    client = OpenAI(
        # This is the default and can be omitted
        api_key=config['openai']['api_key'],
    )

    response = client.images.generate(
        model="dall-e-3",
        prompt=key_words,
        size="1792x1024",
        quality="standard",
        n=1,
    )

    print(response.data[0].url)

    return response.data[0].url


def create_image_v2(key_words):

    # Get Reference to Properties
    config = configparser.ConfigParser()
    config.read('C:\\etc\\properties.ini')

    client = OpenAI(
        # This is the default and can be omitted
        api_key=config['openai']['api_key'],
    )

    response = client.images.generate(
        model="gpt-image-1",
        prompt=key_words,
        size="1024x1536",
        quality="auto",
        n=1,
    )

    print(response.data[0].url)

    return response.data[0].url