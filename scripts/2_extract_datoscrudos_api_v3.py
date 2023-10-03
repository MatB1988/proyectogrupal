import os
import os.path
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account

# Specify the path to your JSON key file
credentials_path = '/home/henry_grupo10_v1/0_scripts/extreme-unison-399121-cadd77c555ca.json'

# Load the credentials from the JSON file
credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=['https://www.googleapis.com/auth/drive'])

# Use the 'credentials' object in your code to authenticate with Google Drive API

# Authenticate with Google Drive API
drive_service = build('drive', 'v3', credentials=credentials)

folderId = '1olnuKLjT8W2QnCUUwh8uDuTTKVZyxQ0Z'
outputFolder = 'output'

# Create folder if not existing
if not os.path.isdir(outputFolder):
    os.mkdir(outputFolder)

items = []
pageToken = ""
while pageToken is not None:
    response = drive_service.files().list(q="'" + folderId + "' in parents", pageSize=1000, pageToken=pageToken,
                                          fields="nextPageToken, files(id, name)").execute()
    items.extend(response.get('files', []))
    pageToken = response.get('nextPageToken')

for file in items:
    file_id = file['id']
    file_name = file['name']
    request = drive_service.files().get_media(fileId=file_id)
    ### Saves all files under outputFolder
    fh = io.FileIO(outputFolder + '/' + file_name, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(f'{file_name} downloaded completely.')