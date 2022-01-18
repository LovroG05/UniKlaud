from storagePlugins.googledrive import GoogleDriveProvider

gdrive = GoogleDriveProvider("gdrive", "GoogleDrive", 150000000000)

file_list = gdrive.listFiles()
for file1 in file_list:
    print('title: {}, id: {}'.format(file1['title'], file1['id']))

if "main.json" in [i["title"] for i in file_list]:
    print("true")