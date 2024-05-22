import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()

# Path to the credentials JSON file downloaded from Google Cloud Console
credentials_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS')

# Scopes required for accessing Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def main():
    # Load credentials from the JSON file
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=SCOPES)

    # Create a service object for interacting with Google Sheets API
    service = build('sheets', 'v4', credentials=credentials)

    # Example: List all spreadsheets
    spreadsheet_list = service.spreadsheets().list().execute()
    for spreadsheet in spreadsheet_list.get('files', []):
        print(spreadsheet['name'])

if __name__ == '__main__':
    main()
