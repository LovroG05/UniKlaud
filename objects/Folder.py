import json


class Folder:
	def __init__(self, name):
		self.name = name
		self.folders = {}
		self.files = {}
		
	def addFolder(self, folder):
		self.folders[folder.name] = folder

	def addFile(self, file):
		self.files[file.name] = file

	def removeFile(self, file):
		self.files.pop(file.name, None)
		
	def getFolders(self):
		return self.folders

	def getFolder(self, folderName):
		return self.folders[folderName]

	def getFiles(self):
		return self.files

	def getFile(self, fileName):
		return self.files[fileName]
		
	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)