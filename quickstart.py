import gspread
from oauth2client.service_account import ServiceAccountCredentials
import string

scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name('facebook-messenger-bot-46e94bcec445.json', scope)

gc = gspread.authorize(credentials)

#Opening the fb_messenger_bot Sheet1
worksheet = gc.open("fb_messenger_bot").sheet1

#returns the value within that cell
#val = worksheet.acell('B1').value # With label
#if the cell is empty, it would return ""

#Helpful Source
#http://gspread.readthedocs.io/en/latest/oauth2.html


