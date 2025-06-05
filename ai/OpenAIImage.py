from openai import OpenAI
import base64

import configparser

# Get Reference to Properties
config = configparser.ConfigParser()
config.read('C:\\etc\\properties.ini')

def get_openai_image_bytes(prompt):

    client = OpenAI(
        # This is the default and can be omitted
        api_key=config['openai']['api_key']
    )

    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1536x1024"
    )

    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    return image_bytes


if __name__ == "__main__":

    test = """
        The andromeda galaxy
        """

    image_bytes = get_openai_image_bytes(test)

    # Save the image to a file
    with open("image.png", "wb") as f:
        f.write(image_bytes)
