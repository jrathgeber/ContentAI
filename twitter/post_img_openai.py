import ai.OpenAIImage as ai

import configparser
config = configparser.ConfigParser()
config.read('C:\\etc\\properties.ini')


def new_image(key_words):

    # set some vars
    key_words = key_words.lstrip()
    slug = key_words.replace(" ", "_")
    file_name = slug + '.jpg'

    # new API returns the bytes
    image_bytes = ai.get_openai_image_bytes(key_words)

    temp_path = str(config['blog']['blog_temp'])
    file_image_path = temp_path + "images\\" + file_name

    # Save the image to a file
    with open(file_image_path, "wb") as f:
        f.write(image_bytes)

    return file_name


if __name__ == '__main__':
    try:
        file_path = new_image("New York Knicks playing basket ball and loosing")
    except KeyboardInterrupt:
        print (file_path)

