import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
import objects.storageProvider as StorageProvider
import webbrowser
import os, sys
from packages.MessageUtil import *

class DropboxProvider(StorageProvider.StorageProvider):
    def __init__(self, provider, storageName, size_bytes, appkey, appsecret):
        self.APP_KEY = appkey
        self.APP_SECRET = appsecret
        refresh = ""

        try:
            with open(storageName + ".txt", "r") as f:
                refresh = f.read()
                f.close()
        except:
            printWarning("File " + storageName + ".txt not found")

        if refresh == "":
            try:
                self.auth_flow = DropboxOAuth2FlowNoRedirect(self.APP_KEY, use_pkce=True, token_access_type='offline')
                authorize_url = self.auth_flow.start()
                print("1. Go to: " + authorize_url)
                print("2. Click \"Allow\" (you might have to log in first).")
                print("3. Copy the authorization code.")
                webbrowser.open(authorize_url)
                auth_code = input("Enter the authorization code here: ").strip()

                try:
                    oauth_result = self.auth_flow.finish(auth_code)
                except Exception as e:
                    printError("Error: %s" % (e,))
                    exit(1)
                
                refresh = oauth_result.refresh_token

                with open(storageName + ".txt", "w") as f:
                    f.write(refresh)
                    f.close()
            
            except Exception as e:
                printError("Error while authenticating: " + str(e))
                sys.exit()
        
        self.provider = provider
        self.storageName = storageName
        self.size_bytes = size_bytes
        self.storagePercentage = 0

        # print("Access token: %s" % (oauth_result.refresh_token))
        self.dropbox = self.initialize(refresh)
        self.dropbox.users_get_current_account()

    def initialize(self, auth):
        return dropbox.Dropbox(oauth2_refresh_token=auth, app_key=self.APP_KEY)

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
