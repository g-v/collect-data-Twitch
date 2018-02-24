import requests # requirement!
import socket
import sys
import time
import json
from datetime import datetime

words = []
t1 = datetime.now()
t3 = datetime.now()
t2 = None
deltaT = None
deltaTGeral = None
fileNumber = 1
nameOfEvent = 'testEvent'

# client info
headers={'Client-ID': '...'} # client-ID for the Twitch API

def request():
	global t1
	global t2
	global t3
	global deltaT
	global deltaTGeral
	global words
	global headers
	global fileNumber
	global nameOfEvent

	t2 = datetime.now()

	deltaT = t2 - t1
	deltaTGeral = t2 - t3

	if deltaT.total_seconds() > 60: # minimum time to make a request, you can change that if you want
		# request
		with requests.Session() as c:
			url = 'https://api.twitch.tv/kraken/streams/channel' # don't forget to change channel!
		try:
			response = c.get(url, headers=headers)
		except:
			print('Error connecting to Twitch API. Check your Internet connection.')
			return

		timeNow = '{:%Y-%b-%d %H:%M}'.format(datetime.now())
		if timeNow is not None:
			words.append(timeNow)
		if response is not None:
			words.append(response.json())
		
		t1 = datetime.now()

	if deltaTGeral.total_seconds() > 3600: # minimum time to write to text file 
	
		# it was better for our team to have separate files for each hour.
		# you might want to change that, or not
		with open(nameOfEvent+'-'+str(fileNumber), 'w') as myFile:
			json.dump(words, myFile)
			words = []
			t3 = datetime.now()
			fileNumber = fileNumber + 1
			



while True:
	try:
		request() # try and get data
	except:
		pass # ignore errors that came from the request
	time.sleep(60) # sleep for a minute, you might want to increase or decrease the interval between requests