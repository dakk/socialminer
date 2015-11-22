import requests

def submitTwitterAccount (account):
	url = 'http://optools.anonops.com/edi/twAT.php?o=opparis&t='+account
	r = requests.get (url)
	r.text
