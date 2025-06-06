import configparser
import emailxx.yahoo_send_mail as yahoo

config = configparser.ConfigParser()
config.read('C:\\etc\\properties.ini')

url = config['yahoo']['yahoo.url']
user = config['yahoo']['yahoo.user']
password = config['yahoo']['yahoo.pass']
server = config['yahoo']['yahoo.server']
port = config['yahoo']['yahoo.port']
username = config['yahoo']['yahoo.username']


def send_quick_message(subject, message):
    if message != '':
        yahoo.send_mail('jrathgeber@yahoo.com', 'jrathgeber@yahoo.com', subject, message, [], server, port, username, password)


#send_quick_message("Hello!")