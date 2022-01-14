import json


class Folder:
	def __init__(self, name):
		self.name = name
		self.directories = {}
		self.files = {}
		
	def addFile(self, file):
		self.files[file.name] = file
		
	def addDirectory(self, directory):
		self.directories[directory.name] = directory
		
	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)