import objects.storageProvider as StorageProvider
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os, sys
from packages.MessageUtil import *

class GoogleDriveProvider(StorageProvider.StorageProvider):
    def __init__(self, provider, storageName, size_bytes):
        try:
            self.auth = self.getAuth(storageName)
        except Exception as e:
            printError("Error while authenticating: " + str(e))
            sys.exit()
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
                try:
                    os.remove(storagename + ".txt")
                except Exception as e:
                    printWarning("Error while removing google credentials file: " + str(e))
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
        try:
            file_list = self.drive.ListFile({'q': "'root' in parents"}).GetList()
            return file_list
        except Exception as e:
            printError("Error while listing files: " + str(e))
            raise e

    def uploadFile(self, file_path, filename):
        try:
            file1 = self.drive.CreateFile({'title': filename})
            file1.SetContentFile(file_path)
            file1.Upload()
        except Exception as e:
            raise e

    def getUsedB(self):
        try:
            return self.drive.GetAbout().get('quotaBytesUsed')
        except Exception as e:
            printError("Error while getting used bytes: " + str(e))
            raise e

    def getFileId(self, filename):
        try:
            file_list = self.drive.ListFile({'q': "'root' in parents"}).GetList()
        except Exception as e:
            printError("Error while listing files: " + str(e))
            raise e
        if file_list is not None:
            for file1 in file_list:
                if filename == file1['title']:
                    return file1['id']
        return "That file does not exist"
        
    def downloadFile(self, file, store_filename):
        fileid = self.getFileId(file)
        if fileid == "That file does not exist":
            print("That file does not exist")
        else:
            try:
                file1 = self.drive.CreateFile({'id': fileid})
                file1.GetContentFile(store_filename)
            except Exception as e:
                raise e

    def deleteFile(self, file):
        fileid = self.getFileId(file)
        if fileid == "That file does not exist":
            print("That file does not exist")
        else:
            try:
                file1 = self.drive.CreateFile({'id': fileid})
                file1.Delete()
            except Exception as e:
                raise e