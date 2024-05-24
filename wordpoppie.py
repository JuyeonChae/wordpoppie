import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re

load_dotenv()

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
# gc.share('chae.alexa@gmail.com', perm_type='user', role='owner')

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
pattern = re.compile(r'^[a-zA-Z\s]+$')
filtered_strings = [cell for cell in column_data if isinstance(cell, str) and pattern.match(cell)]

print(filtered_strings)