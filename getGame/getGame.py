import gdown
from getGame.googleDriveServiceInstance import service
import pandas as pd


def GetFiles(folder):
    query = f"parents = '{folder}'"

    response = service.files().list(q=query).execute()
    files = response.get('files')
    nextPageToken = response.get('nextPageToken')

    while nextPageToken:
      response = service.files().list(q=query).execute()
      files.extend(response.get('files'))
      nextPageToken = response.get('nextPageToken')
    return files

def Download(id, download_path):
  gdown.download(
       id=id,
       quiet=False,
       output=download_path
   )


def IsNewVersion(version, file):
   with open(file, "r") as f:
      firstLine = f.readline()
      if firstLine != version:
          return version

def GetGame(filepath, download_path):
  mainFolder = '1-AbAeaaIuW9jrCFy6UQ9w7t2l-R_cOGD'
  files = GetFiles(mainFolder)
  df = pd.DataFrame(files)
  id = df['id'].values[0]
  files = GetFiles(id)

  df = pd.DataFrame(files)
  id = df['id'].values[0]
  files = GetFiles(id)

  df = pd.DataFrame(files)
  id = df['id'].values[0]
  name = df['name'].values[0]
  
  new_version = IsNewVersion(name, filepath)
  if new_version is not None:
    Download(id, download_path)
    with open(filepath, 'w') as f:
      f.write(new_version)
    print("new version is avalible")



