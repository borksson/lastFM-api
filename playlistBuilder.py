#Application name	getMusic
#API key			ae4c5fa87182e5dafeb88f5a35ac73a8
#Shared secret		6ba9ea744c8681624af841f69b2632ac
#Registered to		borkson

import requests
import json
import requests_cache
import time
from IPython.core.display import clear_output
import pandas as pd
from tqdm import tqdm
import random
import sys
from datetime import datetime
import os

tqdm.pandas()
requests_cache.install_cache()

API_KEY = "ae4c5fa87182e5dafeb88f5a35ac73a8"
USER_AGENT = "borkson"

headers = {
	'user-agent': USER_AGENT
}

payload = {
	'api_key': API_KEY,
	'method': 'track.getSimilar',
	'format': 'json',
	'track': 'crush',
	'artist': 'souly had',
	'limit': 15
}

playlist = {"playlist": {"name": "Testbed", "track": [{"artist": "cher", "name": "believe"}]}}
numToAdd = 10

if(len(sys.argv)>1):
	playlist = json.loads(sys.argv[1])
if(len(sys.argv)>2):
	numToAdd = int(sys.argv[2])

#r = requests.get('https://ws.audioscrobbler.com/2.0/', headers=headers, params=payload)
#print(r.status_code)

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

def similartracks(playlist):
	output = {"similartracks_list": []}
	for track in playlist['playlist']['track']:
		similartracks = {"similartracks": {"base_trackNM": track['name'],"base_artistNM": track['artist'],"track": []}}
		payload['track'] = track['name']
		payload['artist'] = track['artist']
		r = lastfm_get(payload).json()
		if not getattr(r, 'from_cache', False):
			time.sleep(0.25)
		tracks = r['similartracks']['track']
		for track in tracks:
			similartracks['similartracks']['track'].append({"artist":track['artist']['name'],"name":track['name']})
		output['similartracks_list'].append(similartracks)
	return output

def songsToAdd(playlist, numToAdd):
	output = {"songsToAdd": []}
	similartracks_list = similartracks(playlist)
	#if (numToAdd>len(similartracks_list['similartracks_list'])):
	#	numToAdd = len(similartracks_list['similartracks_list'])
	similartracks_list = [t for t in similartracks_list['similartracks_list'] if len(similartracks_list['similartracks_list']) > 0]
	randSel = random.choices(similartracks_list, k=numToAdd)
	for track_sel in randSel:
		if(len(track_sel['similartracks']['track'])>0):
			rc = random.choice(track_sel['similartracks']['track'])
			inPlaylist = True
			while(inPlaylist):
				if rc['name'] in [i['name'] for i in playlist['playlist']['track']]:
					rc = random.choice(track_sel['similartracks']['track'])
				elif rc['name'] in [i['name'] for i in output['songsToAdd']]:
					rc = random.choice(track_sel['similartracks']['track'])
				else:
					inPlaylist = False
			rc['artist'] = rc['artist'].replace("'","")
			rc['name'] = rc['name'].replace("'","")
			output['songsToAdd'].append(rc)
	return output
	#while numAdded < numToAdd:

output = songsToAdd(playlist, numToAdd)
with open("/home/borkson/Code/Python/APIS/APIRequests/Last.FM/exe_record.txt","a") as file:
	file.write(' '.join(["Executed at:",datetime.now().strftime("%d/%m/%Y %H:%M:%S"),'\n',"Number to add:",
		str(numToAdd),'\n',"Input playlist:",json.dumps(playlist),'\n',"Output:",json.dumps(output),'\n',"Number added:",str(len(output['songsToAdd'])),'\n\n']))
print(output)

# Input: {"playlist": {"name": "Testbed", "track": [{"artist": "cher", "name": "believe"}]}
# Output: {"similartracks": {"base_trackNM": "believe", "base_artistNM": "cher", "track": [{"artist": "Madonna", "name": "Vogue"}]}}
