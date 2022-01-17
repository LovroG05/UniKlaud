import json


class File:
	def __init__(self, name, manifestuuid, manifestfilename, actualmn, subfilesjson):
		self.name = name
		self.manifestuuid = manifestuuid
		self.manifestfilename = manifestfilename
		self.actualmanifestname = actualmn
		self.subFiles = subfilesjson

	def isFolder(self):
		return False
		
	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)