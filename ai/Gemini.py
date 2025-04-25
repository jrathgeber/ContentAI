import google.generativeai as genai
import configparser

# Get Reference to Properties
config = configparser.ConfigParser()
config.read('C:\\etc\\properties.ini')

api_key = config['gemini']['api_key']


def list_models():

    genai.configure(api_key=api_key)

    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
            print(m.name)


def generate_article(model_name, prompt):

    """
    Generates an article using the Gemini API.

    Args:
        model_name: The name of the Gemini model to use (e.g., "gemini-1.0-pro").
        prompt: The prompt for the article generation.

    Returns:
        The generated article text, or None if an error occurs.
    """

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating article: {e}")
        return None


if __name__ == "__main__":

    print("Hello Gemini")

    list_models()

    model_name = "gemini-2.0-flash"
    prompt = "Tell me what is going on with this web site : https://agentverse.ai/?sort=relevancy&page=1&recommended=true"

    article = generate_article(model_name, prompt)

    if article:
        print(article)
