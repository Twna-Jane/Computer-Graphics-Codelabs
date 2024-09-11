import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Scopes - toke.json should be deleted if they're modified
SCOPES = ['https://www.googleapis.com/auth/drive']


def create_drive_service():
    """
    Authenticate and return the Google Drive service object.
    - A section of the code is from the Google Drive API Python quickstart documentation
    :return: Google Drive API service object.
    """
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If no valid credentials available, prompt user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for future runs
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # Build and return the Drive v3 API service
        return build("drive", "v3", credentials=creds)
    except HttpError as error:
        print(f"An error occurred while creating the Drive service: {error}")
        return None
