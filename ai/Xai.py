from openai import OpenAI
import configparser
import json

# Get Reference to Properties
config = configparser.ConfigParser()
config.read('C:\\etc\\properties.ini')


def ask_grok_something(model_name, prompt):

    client = OpenAI(
        # This is the default and can be omitted
        api_key=config['Xai']['api_key'],
        base_url="https://api.x.ai/v1"
    )

    response = client.chat.completions.create(

        model=model_name,

        messages=[
           {"role": "system", "content": "State today's date at beginning and echo the prompt question. Provide X citations only. Focus on happy and good news not wars and conflicts."},
           {"role": "user", "content": prompt}
        ],
    )

    return response.choices[0].message.content


if __name__ == "__main__":

    model_name = "grok-3-latest"
    prompt = "What is happening in the world today?  Avoid wars and conflicts. Any good happy news ?  "

    answer = ask_grok_something(model_name, prompt)

    if answer:
        print(answer)
