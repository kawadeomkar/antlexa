"""
ANTLEXA
Get arrival estimates for the Anteater Express using Transloc API
"""
import inspect
from datetime import datetime
import unirest
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from creds import *


stopDicts = {
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

# only contains 2 bus times
retStr = []

response = unirest.get("https://transloc-api-1-2.p.mashape.com/arrival-estimates.json?agencies=1039&callback=call",
  headers={
    "X-Mashape-Key": xmashupkey,  
    "Accept": "application/json"
  }
)


def parseTime(time): 
  #print time
  times = time.split("T")
  retTime = times[1][0:8]
  currentTime = datetime.now().strftime("%H:%M:%S")
  FMT = '%H:%M:%S'
  tdelta = datetime.strptime(retTime, FMT) - datetime.strptime(currentTime, FMT)
  timeLeft = str(tdelta).split(":")

  if timeLeft[1] == "00":
    string = " " + timeLeft[2] + " seconds "
  elif timeLeft[2] == "00":
    string = timeLeft[1] + " minutes"
  else:
    string = timeLeft[1] + " minutes and " + timeLeft[2] + " seconds"
  
  return string

def getTimes(stop_name):  
  for route in response.body['data']:
    if route['stop_id'] == stopDicts[stop_name]:
      for stops in route['arrivals']:
        timeStr = parseTime(stops['arrival_at'])
        retStr.append(timeStr)
  return ", ".join(retStr)    

"""
response = unirest.get("https://transloc-api-1-2.p.mashape.com/routes.json?agencies=1039&callback=call",
  headers={
    "X-Mashape-Key": xmashupkey,
    "Accept": "application/json"
  }
)
"""
# V LINE STOPS: [u'8197552', u'8197554', u'8197558', u'8197560', u'8197564']
# C LINE STOPS: [u'8197566', u'8197568', u'8197570', u'8197572', u'8197574', u'8197576', u'8197578']
# N LINE STOPS: [u'8197566', u'8197580', u'8197582', u'8197584', u'8197564', u'8197578']
# H LINE STOPS: [u'8197566', u'8197554', u'8197568', u'8197570', u'8197572', u'8197574', u'8197576', u'8197560', u'8197558', u'8197580', u'8197582', u'8197584', u'8197564', u'8197578']

# 8197566 Puerta del sol north?
#getTimes(8197566)

#if "__name__" = main:
	#ask user for input for stop id

















 




