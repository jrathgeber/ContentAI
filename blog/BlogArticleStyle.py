import time
from shutil import copyfile


def copywrite(copy, article_number, slug, key_words, todaydate):

    copy.write('\n\n')
    copy.write('    <link rel="stylesheet" href="./medium.css" type="text/css" />\n')
    copy.write('    <link rel="canonical" href="https://www.jasonrathgeber.com/vcard/blogpost/blogpost_' + article_number + '_' + slug + '.html" /> \n')
    copy.write('\n\n')


def replace_stype_backup(blog_path, article_number, slug, key_words, today_date):

    f = open(blog_path + "\\articles\\article_" + article_number + '_' + slug + ".html", "r")
    copy = open("\\zTemp\\blog\\article.html", "w")

    for line in f:

        if '<style type="text/css">' in line:
            for _ in range(127):
                next(f)
            copywrite(copy, article_number, slug, key_words, today_date)
        else:
            copy.write(line)

    f.close()
    copy.close()

    copyfile('\\zTemp\\blog\\article.html', blog_path + '\\articles\\article_' + article_number + '_' + slug + '.html')

    # Give it some time
    time.sleep(3)


def insert_after_text(filename, search_text, new_line):
    # Read the entire file
    with open(filename, 'r') as file:
        content = file.read()

    # Check if the search text exists in the file
    if search_text in content:

        # Replace the search text with itself plus the new line
        modified_content = content.replace(search_text, new_line + search_text)

        # Write the modified content back to the file
        with open(filename, 'w') as file:
            file.write(modified_content)
        return True
    else:
        return False


def replace_stype(blog_path, article_number, slug, key_words, today_date):

    filename = blog_path + "\\articles\\article_" + article_number + '_' + slug + ".html"
    insert_after_text(filename, '    </head>', '        <link rel="stylesheet" href="./medium.css" type="text/css" />\n')
    insert_after_text(filename, '    </head>', '        <link rel="canonical" href="https://www.jasonrathgeber.com/vcard/blogpost/blogpost_' + article_number + '_' + slug + '.html" />\n')


def replace_one_line(path, article):

    filename = path + article
    insert_after_text(filename, '</head>', '<link rel="canonical" href="https://www.jasonrathgeber.com/vcard/blogpost/blogpost_' + article + '" />\n')


if __name__ == "__main__":
    replace_one_line('C:\\dev\\godaddy\\vcard\\blogpost\\Articles\\', 'article_050_use_the__xAI_API_to_call_grok.html')
