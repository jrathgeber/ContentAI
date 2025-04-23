from ebaysdk.finding import Connection as Finding

api = Finding(domain='svcs.sandbox.ebay.com', appid="JasonRat-Mechaniz-SBX-3f73964fa-89a456a0", config_file=None)
response = api.execute('findItemsAdvanced', {'keywords': 'Python'})
print(response.dict())