import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
import deepl

load_dotenv()

def translate(data): 
    deepl_auth_key = os.getenv('DEEPL_API_KEY')
    translator = deepl.Translator(deepl_auth_key)
    
    for string in data:
        # Split the string into words
        words = string.split()        
        words_string = ' '.join(words)
        result = translator.translate_text(words_string, target_lang="KO")
        print(result.text)

# Path to the credentials JSON file downloaded from Google Cloud Console
credentials_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS')

# Scopes required for accessing Google Sheets API
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
    ]

# Load credentials from the JSON file
credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
gc = gspread.authorize(credentials)

# Create a service object for interacting with Google Sheets API
service = build('sheets', 'v4', credentials=credentials)

spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1llg9I2NUYMVi5tLI_toMIfs5-UQYE8c2tPqsc-Hti6k/edit#gid=1191188390'

# take the spreadsheet document
doc = gc.open_by_url(spreadsheet_url)

sis = 'chae.alexa@gmail.com'
doc.share(sis, perm_type='user', role='writer')

# choose a sheet
worksheet = doc.worksheet('3')

# take data from a column and separate the cells one by one, remaining alphabets only
column_data = worksheet.col_values(1)
print(column_data)

translate(column_data)
    