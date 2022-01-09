class StorageProvider:
    def __init__(self, provider, storageName):
        self.auth = self.getAuth()
        self.initialize(self.auth)
        self.provider = provider
        self.storageName = storageName

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

    def downloadFile(self, file):
        pass

    def deleteFile(self, file):
        pass

    def getJsonData(self):
        return {
            "provider": self.provider,
            "storagename": self.storageName
        }