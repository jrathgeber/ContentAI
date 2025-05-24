import configparser
from datetime import date

import ai.Dalle as ai
import requests
import os
from PIL import Image


def write(key_words):

    # Get today's Date
    today = date.today()
    formatted_date = today.strftime("%b %d, %Y")
    print("Processing " + formatted_date)

    # Get Reference to Properties
    config = configparser.ConfigParser()
    config.read('C:\\etc\\properties.ini')

    slug = key_words.replace(" ", "_")

    file_path_image = "c:\\\\dep\\ContentAI\\images\\"

    new_image(file_path_image, slug, key_words, formatted_date)


def download_image(url, file_name):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"Image successfully downloaded: {file_name}")
    else:
        print("Failed to retrieve the image")


def new_image(file_path_laptop_image, slug, key_words, ddate):

    file_name = file_path_laptop_image + slug + '.jpg'

    image_url = ai.create_image(file_path_laptop_image, 23,  slug, key_words, ddate)

    download_image(image_url, slug + '.jpg')


if __name__ == '__main__':
    try:
        write("Stary Night")
    except KeyboardInterrupt:
        print ('\nGoodbye!')