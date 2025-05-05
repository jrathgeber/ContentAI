import ai.OpenAi013 as ai


def generate_them(data_file):

    twitter_content = ai.get_tweets("10 Dark Ways to Get Rich Fast", data_file)

    # File path where you want to save the HTML file
    # file_path = path + "article_" + number + "_" + slug + ".html"

    # Open the file in write mode and save the HTML content
    # with open(file_path, "w") as file:
    #    file.write(html_content_2)

    # print(f"HTML file saved as {file_path}")

    return twitter_content
