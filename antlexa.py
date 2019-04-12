"""
ANTLEXA
Get arrival estimates for the Anteater Express using Transloc API
"""
from datetime import datetime
import unirest
from creds import *
import json
import requests
# botocore library inside aws lambda
#from botocore.vendored import requests

class TranslocAPI:
	def __init__(self, url, xmashupkey, accept):		
		self.url = url
		self.xmashupkey = xmashupkey
		self.accept = accept
		# dictionary of names of stops
		self.stopDicts = {
			'UTC North':'8197566',
			'UTC South':'8197552',
			'Campus Cornell':'819755Z4',
			'California Cornell':'8197568',
			'AV Stop #1':'8197570',
			'CDS Stop #1':'8197572',
			'CDS Stop #2':'8197574',
			'CDS Stop #3':'8197576',
			'VDC Stop #1':'8197560',
			'VDC Stop #2':'8197558',
			'VDC Norte Stop #1':'8197580',
			'VDC Norte Stop #2':'8197582',
			'VDC Norte Stop #3':'8197584',
			'East Campus Transfer':'8197564',
			'Puerta del sol North':'8197578'		
		}

		self.busIDs = {
			'8004734':'V',
			'8004736':'C',
			'8004740':'H',
			'8004742':'D',
			'8005766':'M',
			'8004748':'N',
			'8004750':'S',
			'8004752':'W',
			'8004746':'M Weekend'
		}
		# only contains 2 bus times
		self.retStr = []
		self.response = self.getResponse()


	def getResponse(self):
		response = requests.get(self.url,
		  headers={
		    "X-Mashape-Key": self.xmashupkey,  
		    "Accept": self.accept
		  }
		)
		return json.loads(response.text)

	# parse time format into string
	def parseTime(self, time): 
		#print time
		times = time.split("T")
		retTime = times[1][0:8]
		FMT = '%H:%M:%S'
		currentTime = datetime.now().strftime(FMT)
		tdelta = datetime.strptime(retTime, FMT) - datetime.strptime(currentTime, FMT)
		timeLeft = str(tdelta).split(":")

		if timeLeft[1] == "00":
			string =  timeLeft[2] + " seconds"
		elif timeLeft[2] == "00":
			string = timeLeft[1] + " minutes"
		else:
			string = timeLeft[1] + " minutes and " + timeLeft[2] + " seconds"
		return string

	#
	def format(self, retStr):
		busString = ""
		for busTime in retStr:
			busString += retStr[0] + " Line coming in " + retStr[1] + ", ";
		return busString

	# get arrival estimates  given stop name
	def getTimes(self, stop_name):  
		for route in self.response['data']:
			if route['stop_id'] == self.stopDicts[stop_name]:
				for stops in route['arrivals']:
					timeStr = self.parseTime(stops['arrival_at'])
					self.retStr.append((timeStr, self.busIDs[stops['route_id']]))
		return format(self.retStr)

# V LINE STOPS: [u'8197552', u'8197554', u'8197558', u'8197560', u'8197564']
# C LINE STOPS: [u'8197566', u'8197568', u'8197570', u'8197572', u'8197574', u'8197576', u'8197578']
# N LINE STOPS: [u'8197566', u'8197580', u'8197582', u'8197584', u'8197564', u'8197578']
# H LINE STOPS: [u'8197566', u'8197554', u'8197568', u'8197570', u'8197572', u'8197574', u'8197576', u'8197560', u'8197558', u'8197580', u'8197582', u'8197584', u'8197564', u'8197578']

# 8197566 Puerta del sol north?
#getTimes(8197566)

if __name__ == '__main__':
	# ask user for input for stop id
	req = TranslocAPI(url, xmashupkey, accept)
	print(req.getTimes('UTC North'))















 




