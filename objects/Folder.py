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
		try:
			del self.files[file.name]
		except KeyError:
			pass

	def removeFolder(self, folder):
		try:
			del self.folders[folder.name]
		except KeyError:
			raise KeyError("Folder not found")
		
	def getFolders(self):
		return self.folders

	def getFolder(self, folderName):
		try:
			return self.folders[folderName]
		except KeyError:
			raise KeyError("Folder not found")

	def getFiles(self):
		return self.files

	def getFile(self, fileName):
		try:
			return self.files[fileName]
		except KeyError:
			raise KeyError("File not found")
		
	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)