import objects.storageProvider as StorageProvider
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class GoogleDriveProvider(StorageProvider.StorageProvider):
    def __init__(self, provider, storageName, size_bytes):
        self.auth = self.getAuth()
        self.initialize(self.auth)
        self.provider = provider
        self.storageName = storageName
        self.size_bytes = size_bytes

    def getAuth(self):
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile("mycreds.txt")
        if gauth.credentials is None:
            # Authenticate if they're not there
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
        # Refresh them if expired
            gauth.Refresh()
        else:
            # Initialize the saved creds
            gauth.Authorize()
        # Save the current credentials to a file
        gauth.SaveCredentialsFile("mycreds.txt")
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