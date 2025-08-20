import os
import io
import json
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

class drive_folder:
    def __init__(self, folder_id, project):
        self.master_folder = folder_id
        self.project = project
        pass

    def drive_client(self):
        # Load environment variables
        load_dotenv()

        # Load the path from .env
        creds_path = os.getenv("GOOGLE_API_CREDENTIALS_PATH")
        if not os.path.isabs(creds_path):
            creds_path = os.path.join(os.path.dirname(__file__), creds_path)
        # Load credentials from file
        with open(creds_path, "r") as f:
            creds_dict = json.load(f)

        # Create credentials object
        SCOPES = ['https://www.googleapis.com/auth/drive'] #this scope is needed to get the permissions to download files
        credentials = service_account.Credentials.from_service_account_info(creds_dict, scopes=SCOPES)

        # Build the Drive API client
        self.service = build('drive', 'v3', credentials=credentials)

    def get_drive_files(self):
        if self.project == "STEM":
            self.stem_prd_files()

        elif self.project == "NOVUS":
            self.novus_prd_files()

        else:
            print("ERROR - SPECIFY VALID PROJECT")

    def stem_prd_files(self):
        prd_dirs = [] #list to loop the download function for each item
        file_dirs = {}
        query = f"'{self.master_folder}' in parents and trashed = false"

        results = self.service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name, mimeType)'
        ).execute()
        
        sub_dirs = results.get('files', [])

        if not sub_dirs:
            print('No files found.')
        else:
            for folder_id in sub_dirs:
                if (folder_id['mimeType']=="application/vnd.google-apps.folder") & (folder_id['name'].split('_')[1]=='prod'):
                    prd_dirs.append(folder_id)

        for prd_folder in prd_dirs:
            query = f"'{prd_folder['id']}' in parents and trashed = false"
            results = self.service.files().list(
                            q=query,
                            spaces='drive',
                            fields='files(id, name, mimeType)'
                            ).execute()
            file_ids = [x for x in results.get('files', []) if x["mimeType"] == "text/csv"]
            file_dirs[prd_folder['name']] = file_ids
        self.csv_list = file_dirs

    def download_drive_files(self, keys=[] ,all=0):
        # keys: list[str] disctionary keys from self.csv_list to indicate which test_subject to download
        # all: bool (0/1) to download all the files in the csv list
        
        if all == 1:
            for subject in self.csv_list.keys():
                pass
        
            return
        
        for key in keys:
            for file in self.csv_list[key]:
                print(f'getting {key} : {file['name']}')
                io_csv = self.download_file(file['id'])

                # Build full directory path and ensure it exists
                output_dir = os.path.join(f"./{self.project}/CSV", file['name'].replace('.csv', ''))
                os.makedirs(output_dir, exist_ok=True)
                # Write CSV to file
                output_path = os.path.join(output_dir, f"{key}.csv")
                with open(output_path, "wb") as binary_file:
                    binary_file.write(io_csv)
                binary_file.close()
                    
    def download_file(self, real_file_id):
        """Downloads a file
        Args:
            real_file_id: ID of the file to download
        Returns : IO object with location.

        Load pre-authorized user credentials from the environment.
        TODO(developer) - See https://developers.google.com/identity
        for guides on implementing OAuth2 for the application.
        """
        try:
            # pylint: disable=maybe-no-member
            request = self.service.files().get_media(fileId=real_file_id)
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}.")

        except HttpError as error:
            print(f"An error occurred: {error}")
            file = None

        return file.getvalue()
    
if __name__ == "__main__":
    dirs = drive_folder("1XL74fi7YxV5-U0nXM1CqQU5051UR3I3m","STEM")
    dirs.drive_client()
    dirs.get_drive_files()
    dirs.download_drive_files(keys=["A01285907_prod"])

