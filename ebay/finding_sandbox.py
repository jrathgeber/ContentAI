from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError

try:
    api = Finding(domain='svcs.sandbox.ebay.com', config_file='c:\\etc\\ebay.yaml')
    response = api.execute('findItemsAdvanced', {'keywords': 'Python'})
    print(response.dict())
except ConnectionError as e:
    print(e)
    print(e.response.dict())