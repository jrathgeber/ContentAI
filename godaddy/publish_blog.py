import ftplib
import configparser

config = configparser.ConfigParser()
config.read('C:\\etc\\properties.ini')

gdurl = config['godaddy']['godaddy.url']
gduser = config['godaddy']['godaddy.user']
gdpass = config['godaddy']['godaddy.pass']


def publish_blog(file_path, article, blog_type):

    session = ftplib.FTP(gdurl, gduser, gdpass)

    from_file = file_path + article

    if blog_type == "post":
        post_file = open(from_file, 'rb')
        session.storbinary('STOR /vcard/blogpost/' + article, post_file)  # send the file
        post_file.close()

    if blog_type == "article":
        article_file = open(from_file, 'rb')
        session.storbinary('STOR /vcard/blogpost/Articles/' + article, article_file)  # send the file
        article_file.close()

    if blog_type == "image":
        image_file = open(from_file, 'rb')
        session.storbinary('STOR /vcard/assets/custom/images/blog/' + article, image_file)  # send the file
        image_file.close()

    if blog_type == "thumb":
        thumb_file = open(from_file, 'rb')
        session.storbinary('STOR /vcard/assets/custom/images/blog/thumbs/' + article, thumb_file)  # send the file
        thumb_file.close()

    if blog_type == "blog":
        blog_file = open(from_file, 'rb')
        session.storbinary('STOR /vcard/' + article, blog_file)  # send the file
        blog_file.close()

    session.quit()


def publish_old():

    publish_blog('C:\\dev\\godaddy\\vcard\\blogpost\\', 'blogpost_050_use_the__xAI_API_to_call_grok.html',  'post')
    publish_blog('C:\\dev\\godaddy\\vcard\\blogpost\\Articles\\', 'article_050_use_the__xAI_API_to_call_grok.html', 'article')

    publish_blog('C:\\dev\\godaddy\\vcard\\assets\\custom\\images\\blog\\', '050_call_grok.jpg', 'image')
    publish_blog('C:\\dev\\godaddy\\vcard\\assets\\custom\\images\\blog\\thumbs\\', '050_call_grok.jpg', 'thumb')

    #publish_blog('C:\\dev\\godaddy\\vcard\\', 'blog.jpg', 'blog')


def publish(slug):
    publish_blog('C:\\dev\\godaddy\\vcard\\blogpost\\', 'blogpost_' + slug + '.html',  'post')
    publish_blog('C:\\dev\\godaddy\\vcard\\blogpost\\Articles\\', 'article_' + slug + '.html', 'article')

    publish_blog('C:\\dev\\godaddy\\vcard\\assets\\custom\\images\\blog\\',  slug + '.jpg', 'image')
    publish_blog('C:\\dev\\godaddy\\vcard\\assets\\custom\\images\\blog\\thumbs\\', slug + '.jpg', 'thumb')


if __name__ == "__main__":
    #publish("046_how_can_retail_short_volatility")
    #publish("047_how_to_add_a_cheap_SSL_certificate_to_a_go_daddy_site")
    #publish("048_dividend_investing")

    publish_blog('C:\\dev\\godaddy\\vcard\\', 'blog.html', 'blog')
