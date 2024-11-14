from getGame.googleDriveServiceInstance import service
import gdown, pandas as pd, shutil


def GetFiles(folder):
    query = f"'{folder}' in parents"
    response = service.files().list(
      pageSize=1000,q=query,fields="nextPageToken, files(id, name)",includeItemsFromAllDrives=True, supportsAllDrives=True
        ).execute()
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
      first_line = f.readline()
      if first_line != version:
         with open(file, 'w') as f:
            f.write(version)
            return True

def GetGame(file_path, download_folder):
  mainFolder = '1-AbAeaaIuW9jrCFy6UQ9w7t2l-R_cOGD'
  files = GetFiles(mainFolder)
  df = pd.DataFrame(files)
  id = df['id'].values[0]
  files = GetFiles(id)
  df = pd.DataFrame(files)
  id = df['id'].values[0]
  name = df['name'].values[1]
  if IsNewVersion(name, file_path):
    Download(name, id)
    print("new version is avalible")
    shutil.move(name, download_folder)



