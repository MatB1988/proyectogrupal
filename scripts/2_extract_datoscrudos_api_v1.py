from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.cloud import storage

# Set up the credentials for the Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive.appfolder']
SERVICE_ACCOUNT_FILE = '/home/henry_grupo10_v1/0_scripts/extreme-unison-399121-cadd77c555ca.json'

credentials = None
try:
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
except ImportError:
    print('Unable to load credentials')
    exit(1)

# Set up the credentials for Google Cloud Storage
client = storage.Client.from_service_account_json(SERVICE_ACCOUNT_FILE)

# Set up the Google Drive API service
drive_service = build('drive', 'v3', credentials=credentials)

# Set up the Google Cloud Storage bucket
bucket_name = 'datos_crudos'
bucket = client.get_bucket(bucket_name)

# Get the file ID of the file you want to copy
file_id = '1mwNNdOMSNty6WumYdH9FJNJZJYQ6oD1c'

# Get the file metadata
file = drive_service.files().get(fileId=file_id).execute()

# Download the file to a temporary file
temp_file = '/tmp/{}'.format(file['name'])
request = drive_service.files().get_media(fileId=file_id)
fh = open(temp_file, 'wb')
downloader = MediaIoBaseDownload(fh, request)
done = False
while done is False:
    status, done = downloader.next_chunk()
    print('Download %d%%.' % int(status.progress() * 100))

# Upload the file to Google Cloud Storage
blob = bucket.blob(file['name'])
blob.upload_from_filename(temp_file)

print('File {} uploaded to {}.'.format(
    file['name'],
    bucket_name))
