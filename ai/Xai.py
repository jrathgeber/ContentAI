from openai import OpenAI
import configparser

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
           {"role": "system", "content": "Be precise and concise."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


if __name__ == "__main__":

    model_name = "grok-2-latest"
    prompt = "What type of AI are you and what is your model ? "

    answer = ask_grok_something(model_name, prompt)

    if answer:
        print(answer)
