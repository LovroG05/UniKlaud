from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

# For using listdir()
import os

# Below code does the authentication
# part of the code
gauth = GoogleAuth()

# Creates local webserver and auto
# handles authentication.
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

# replace the value of this variable
# with the absolute path of the directory
path = r"/media/jurij/Data/Downloads/temp"

# iterating thought all the files/folder
# of the desired directory
for x in os.listdir(path):
	f = drive.CreateFile({'title': x})
	f.SetContentFile(os.path.join(path, x))
	f.Upload()

	drive.

	# Due to a known bug in pydrive if we
	# don't empty the variable used to
	# upload the files to Google Drive the
	# file stays open in memory and causes a
	# memory leak, therefore preventing its
	# deletion
	f = None
