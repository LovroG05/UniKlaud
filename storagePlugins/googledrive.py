import objects.storageProvider as StorageProvider
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class GoogleDriveProvider(StorageProvider.StorageProvider):
    def __init__(self, provider, storageName):
        self.auth = self.getAuth()
        self.initialize(self.auth)
        self.provider = provider
        self.storageName = storageName

    def getAuth(self):
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
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
        
    def downloadFile(self, file):
        pass

    def deleteFile(self, file):
        pass