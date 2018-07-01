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

"""
GOOGLE SPREADSHEETS API
CONNECT TO ANTLEXA DATABASE

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
 
# Connect to Antlexa Database spreadsheet
sheet = client.open("Antlexa Database").sheet1
 
# Extract and print all of the values
list_of_hashes = sheet.get_all_values()
#print(list_of_hashes)
"""

stopDicts = {
  '8197566':'UTC North',
  '8197552':'UTC South',
  '8197554':'Campus Cornell',
  '8197568':'California Cornell',
  '8197570':'AV Stop #1',
  '8197572':'CDS Stop #1',
  '8197574':'CDS Stop #2',
  '8197576':'CDS Stop #3',
  '8197560':'VDC Stop #1',
  '8197558':'VDC Stop #2',
  '8197580':'VDC Norte Stop #1',
  '8197582':'VDC Norte Stop #2',
  '8197584':'VDC Norte Stop #3',
  '8197564':'East Campus Transfer',
  '8197578':'Puerta del sol North'  		
}


response = unirest.get("https://transloc-api-1-2.p.mashape.com/arrival-estimates.json?agencies=1039&callback=call",
  headers={
    "X-Mashape-Key": "l9Kp0js8cGmshilLQYcPz6gyx8o7p1SN9FTjsnWgrCsUaZex9O",
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
  string = timeLeft[1] + " minutes and " + timeLeft[2] + " seconds"
  print string

def getTimes(stop_id):  
    for route in response.body['data']:
    if route[stop_id] == '8197580':
      for stops in route['arrivals']:
         parseTime(stops['arrival_at'])    

"""
response = unirest.get("https://transloc-api-1-2.p.mashape.com/routes.json?agencies=1039&callback=call",
  headers={
    "X-Mashape-Key": "l9Kp0js8cGmshilLQYcPz6gyx8o7p1SN9FTjsnWgrCsUaZex9O",
    "Accept": "application/json"
  }
)
"""
# V LINE STOPS: [u'8197552', u'8197554', u'8197558', u'8197560', u'8197564']
# C LINE STOPS: [u'8197566', u'8197568', u'8197570', u'8197572', u'8197574', u'8197576', u'8197578']
# N LINE STOPS: [u'8197566', u'8197580', u'8197582', u'8197584', u'8197564', u'8197578']
# H LINE STOPS: [u'8197566', u'8197554', u'8197568', u'8197570', u'8197572', u'8197574', u'8197576', u'8197560', u'8197558', u'8197580', u'8197582', u'8197584', u'8197564', u'8197578']


# 8197566 Puerta del sol north?

if "__name__" = main:
	#ask user for input for stop id

















 




