import configparser

from medium_api import Medium

# Get Reference to Properties
config = configparser.ConfigParser()
config.read('C:\\etc\\properties.ini')

# Get the medium token
api_key = config['medium']['token']

# Create a `Medium` Object
medium = Medium(api_key)

# Get the "Article" object and print markdown
article = medium.article(article_id="c4b041243c47")
# print(article.markdown)

print(article.html)

html_content = article.html
file_path = "C:\\dev\\godaddy\\vcard\\blogpost\\Articles\\article_021_will_ai_replace_all_programmers.html"

with open(file_path, 'w', encoding='utf-8') as file:
    file.write(html_content)
print(f"HTML content saved to: {file_path}")
