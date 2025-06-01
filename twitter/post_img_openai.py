import ai.OpenAIImage as ai


def new_image(key_words):

    key_words = key_words.lstrip()

    slug = key_words.replace(" ", "_")

    file_name = slug + '.jpg'

    image_bytes = ai.get_openai_image_bytes(key_words)

    file_image_path = "C:\\dep\\ContentAI\\zTemp\\images\\" + file_name
    file_image_path = "C:\\Users\\jrath\\PycharmProjects\\ContentAI\\zTemp\\images\\" + file_name

    # Save the image to a file
    with open(file_image_path, "wb") as f:
        f.write(image_bytes)

    return file_name


if __name__ == '__main__':
    try:
        file_path = new_image("New York Knicks playing basket ball and loosing")
    except KeyboardInterrupt:
        print (file_path)

