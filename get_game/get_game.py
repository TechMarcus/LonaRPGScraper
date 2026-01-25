import gdown
from get_game.google_drive_service_instance import service
import pandas as pd


def get_game(filepath, download_path):
  mainFolder = '1-AbAeaaIuW9jrCFy6UQ9w7t2l-R_cOGD'
  files = get_files(mainFolder)
  df = pd.DataFrame(files)

  latest_version = find_latest_version(files, df)
  while True:
    try:
      files = get_files(latest_version[1])
      df = pd.DataFrame(files)
      latest_version = find_latest_version(files, df)
    except Exception as e:
      print("An error occurred: ", e)
      break
    
  new_version = is_new_version(latest_version[0], filepath)
  if new_version is not None:
    download(latest_version[1], latest_version[0], download_path)
    with open(filepath, 'w') as f:
      f.write(str(new_version))
    print("new version is avalible")


def get_files(folder):
    query = f"parents = '{folder}'"
    response = service.files().list(q=query).execute()
    files = response.get('files')
    nextPageToken = response.get('nextPageToken')

    while nextPageToken:
      response = service.files().list(q=query).execute()
      files.extend(response.get('files'))
      nextPageToken = response.get('nextPageToken')
    return files


def is_new_version(version, file):
   with open(file, "r") as f:
      firstLine = f.readline()
      if int(firstLine) != int(version):
          return version


def version_to_number(version):
   version_number = 0
   for symbol in version:
      if symbol.isdigit():
          version_number = version_number * 10 + int(symbol)
   return version_number


def find_latest_version(files, df):
  versions = []
  for file in files:
      versions.append(version_to_number(file['name']))
  latest_version = [
    max(versions),
    df['id'].values[versions.index(max(versions))]
  ]
  return latest_version


def download(id, name, download_path):
  gdown.download(
       id=id,
       quiet=False,
       output=f"{download_path}{name}.zip"
   )