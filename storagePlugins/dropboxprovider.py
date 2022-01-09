import dropbox
import objects.storageProvider as StorageProvider

class DropboxProvider(StorageProvider.StorageProvider):
    def __init__(self, provider, storageName, size_bytes):
        self.dropbox = self.initialize(self.getAuth())
        self.dropbox.users_get_current_account()
        self.provider = provider
        self.storageName = storageName
        self.size_bytes = size_bytes
        self.storagePercentage = 0

    def getAuth(self):
        with open("dropbox.txt", "r") as f:
            return f.read()

    def initialize(self, auth):
        return dropbox.Dropbox(auth)

    def listFiles(self):
        file_list = self.dropbox.files_list_folder(path="").entries
        return file_list

    def uploadFile(self, file_path, filename):
        with open(file_path, "rb") as f:
            self.dropbox.files_upload(f.read(), "/" + filename)

    def downloadFile(self, filename, save_filename):
        with open(save_filename, "wb") as f:
            meth, res = self.dropbox.files_download( "/" + filename)
            f.write(res.content)
            f.close()

    def getUsedB(self):
        return self.dropbox.users_get_space_usage().used

    def deleteFile(self, filename):
        self.dropbox.files_delete(filename)
