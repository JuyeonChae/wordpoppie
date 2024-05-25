import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
import deepl

def translate(data): 
    deepl_auth_key = os.getenv('DEEPL_API_KEY')
    translator = deepl.Translator(deepl_auth_key)
    
    translated_words = []    
    for string in data:
        result = translator.translate_text(string, target_lang="KO")
        translated_words.append(result.text)
    return translated_words

# add the translated words to 'specified column + 1' for now, and let the user to choose the target column later
def update_cells(worksheet, column, translated_words):
    data = [[value] for value in translated_words]
    
    target_column = column + 1
    
    # Calculate the range to update
    cell_range = f'{chr(64 + target_column)}1:{chr(64 + target_column)}{len(translated_words)}'

    # Update the specified range with the new values
    worksheet.update(range_name = cell_range, values = data)

def main():
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

    # Create a service object for interacting with Google Sheets API
    service = build('sheets', 'v4', credentials=credentials)

    spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1llg9I2NUYMVi5tLI_toMIfs5-UQYE8c2tPqsc-Hti6k/edit#gid=1191188390'

    # take the spreadsheet document
    doc = gc.open_by_url(spreadsheet_url)

    sis = 'chae.alexa@gmail.com'
    doc.share(sis, perm_type='user', role='writer')

    # choose a sheet
    worksheet = doc.worksheet('Sheet4')

    # take data from a specific column/range - let the user choose it
    column = 1
    column_data = worksheet.col_values(column)

    # translated words are stored in translated_words
    translated_words = translate(column_data)
    print(translated_words)
    update_cells(worksheet, column, translated_words)

if __name__ == "__main__":
    main()