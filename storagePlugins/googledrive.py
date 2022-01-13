import objects.storageProvider as StorageProvider
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

class GoogleDriveProvider(StorageProvider.StorageProvider):
    def __init__(self, provider, storageName, size_bytes):
        self.auth = self.getAuth(storageName)
        self.drive = self.initialize(self.auth)
        self.provider = provider
        self.storageName = storageName
        self.size_bytes = size_bytes
        self.storagePercentage = 0

    def getAuth(self, storagename):
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile(storagename + ".txt")
        if gauth.credentials is None:
            # Authenticate if they're not there
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
        # Refresh them if expired
            try:
                gauth.Refresh()
            except Exception as e:
                gauth.Authorize()
        else:
            # Initialize the saved creds
            gauth.Authorize()
        # Save the current credentials to a file
        gauth.SaveCredentialsFile(storagename + ".txt")
        return gauth

    def initialize(self, auth):
        return GoogleDrive(auth)

    def listFiles(self):
        file_list = self.drive.ListFile({'q': "'root' in parents"}).GetList()
        return file_list

    def uploadFile(self, file_path, filename):
        file1 = self.drive.CreateFile({'title': filename})
        file1.SetContentFile(file_path)
        file1.Upload()

    def getUsedB(self):
        return self.drive.GetAbout().get('quotaBytesUsed')

    def getFileId(self, filename):
        file_list = self.drive.ListFile({'q': "'root' in parents"}).GetList()
        for file1 in file_list:
            # print('title: {}, id: {}'.format(file1['title'], file1['id']))
            if filename == file1['title']:
                return file1['id']
        return "That file does not exist"
        
    def downloadFile(self, file, store_filename):
        fileid = self.getFileId(file)
        if fileid == "That file does not exist":
            print("That file does not exist")
        else:
            file1 = self.drive.CreateFile({'id': fileid})
            file1.GetContentFile(store_filename)

    def deleteFile(self, file):
        fileid = self.getFileId(file)
        if fileid == "That file does not exist":
            print("That file does not exist")
        else:
            file1 = self.drive.CreateFile({'id': fileid})
            file1.Delete()