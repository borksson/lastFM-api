#Application name	getMusic
#API key			ae4c5fa87182e5dafeb88f5a35ac73a8
#Shared secret		6ba9ea744c8681624af841f69b2632ac
#Registered to		borkson

import requests
import json

API_KEY = "ae4c5fa87182e5dafeb88f5a35ac73a8"
USER_AGENT = "borkson"

headers = {
	'user-agent': USER_AGENT
}

payload = {
	'api_key': API_KEY,
	'method': 'chart.gettopartists',
	'format': 'json'
}

r = requests.get('https://ws.audioscrobbler.com/2.0/', headers=headers, params=payload)
print(r.status_code)

def lastfm_get(payload):
	headers = {'user-agent': USER_AGENT}
	url = 'https://ws.audioscrobbler.com/2.0/'

	payload['api_key'] = API_KEY
	payload['format'] = 'json'

	response = requests.get(url, headers=headers, params=payload)

	return response

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

r = lastfm_get({
	'method': 'chart.gettopartists'
	})

print(r.status_code)
jprint(r.json())
jprint(r.json()['artists']['@attr'])