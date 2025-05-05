import io
import os
import ast
from dotenv import load_dotenv

from google.oauth2 import service_account
from googleapiclient.discovery import build

# Load env variables
load_dotenv()
google_creds_dict = ast.literal_eval(os.environ["GOOGLE_API_CREDENTIALS"])

# Create service account credentials
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
credentials = service_account.Credentials.from_service_account_info(google_creds_dict, scopes=SCOPES)

# Build the Drive service
service = build('drive', 'v3', credentials=credentials)

# List folders in your Drive
def list_folders():
    try:
        results = service.files().list(
            q="mimeType='application/vnd.google-apps.folder' and trashed=false",
            spaces='drive',
            fields="files(id, name)"
        ).execute()
        folders = results.get('files', [])
        for folder in folders:
            print(f"Name: {folder['name']}, ID: {folder['id']}")
    except Exception as e:
        print(f"An error occurred: {e}")

list_folders()