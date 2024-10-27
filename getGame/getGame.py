from getGame.googleDriveServiceInstance import service
import gdown, pandas as pd


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

def Download(Name, Id):
  url = 'https://drive.google.com/uc?id=' +  Id
  name =  Name
  gdown.download(url, name, quiet=False)

def IsNewVersion(version, file):
   with open(file, "r") as f:
      firstLine = f.readline()
      if firstLine != version:
         with open(file, 'w') as f:
            f.write(version)
            return True

def GetGame(filepath):
  mainFolder = '1-AbAeaaIuW9jrCFy6UQ9w7t2l-R_cOGD'
  files = GetFiles(mainFolder)
  df = pd.DataFrame(files)
  id = df['id'].values[0]
  files = GetFiles(id)
  df = pd.DataFrame(files)
  id = df['id'].values[0]
  name = df['name'].values[0]
  if IsNewVersion(name, filepath):
    Download(name, id)
    print("new version is avalible")



