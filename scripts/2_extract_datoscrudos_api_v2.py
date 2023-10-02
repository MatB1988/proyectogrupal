from __future__ import print_function

import io

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload


# Authenticate with Google Drive API
creds, _ = google.auth.default()

drive_service = build('drive', 'v3', credentials=creds)

# ID of the Google Drive folder you want to download
folder_id = '19QNXr_BcqekFNFNYlKd0kcTXJ0Zg7lI6'

# Destination directory where you want to save the folder
destination_dir = '/home/henry_grupo10_v1/1_data_extract'

def download_folder(service, folder_id, destination_dir):
    results = service.files().list(q=f"'{folder_id}' in parents",
                                   fields="files(id, name, mimeType)").execute()
    items = results.get('files', [])

    for item in items:
        if item['mimeType'] == 'application/vnd.google-apps.folder':
            # Recursively download subfolders
            subfolder_dest = os.path.join(destination_dir, item['name'])
            os.makedirs(subfolder_dest, exist_ok=True)
            download_folder(service, item['id'], subfolder_dest)
        else:
            file_dest = os.path.join(destination_dir, item['name'])
            request = service.files().get_media(fileId=item['id'])
            fh = open(file_dest, 'wb')
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"Downloading {item['name']} ({int(status.progress() * 100)}%)")

download_folder(drive_service, folder_id, destination_dir)
