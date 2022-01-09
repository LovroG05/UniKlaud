class StorageProvider:
    def __init__(self, provider, storageName, size_bytes):
        self.auth = self.getAuth()
        self.initialize(self.auth)
        self.provider = provider
        self.storageName = storageName
        self.size_bytes = size_bytes
        self.storagePercentage = 0

    def getAuth(self):
        return {
            'username': '',
            'password': ''
        }

    def initialize(self, auth):
        pass

    def listFiles(self):
        pass

    def uploadFile(self, file_path, filename):
        pass

    def downloadFile(self, file, store_filename):
        pass

    def deleteFile(self, file):
        pass

    def getUsedB(self):
        return 0

    def getJsonData(self):
        return {
            "provider": self.provider,
            "storagename": self.storageName,
            "size_bytes": self.size_bytes
        }

    def updateStoragePercentage(self, allfree):
        self.storagePercentage = allfree /((int(self.size_bytes) - int(self.getUsedB())))