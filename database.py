import inspect
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from creds import *

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
