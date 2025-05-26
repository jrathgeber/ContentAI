import ai.Dalle as ai
import requests


def download_image(url, file_name):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"Image successfully downloaded: {file_name}")
    else:
        print("Failed to retrieve the image")


def new_image(key_words):

    key_words = key_words.lstrip()

    slug = key_words.replace(" ", "_")

    file_name = slug + '.jpg'

    image_url = ai.create_image(key_words)

    file_image_path = "C:\\dep\\ContentAI\\zTemp\\images\\" + file_name

    download_image(image_url, file_image_path)

    return file_name


if __name__ == '__main__':
    try:
        file_path = new_image("Memorial Day USA people having a BBQ")
    except KeyboardInterrupt:
        print (file_path)
