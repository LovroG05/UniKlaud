import json


class File:
	def __init__(self, name, manifestuuid, manifestfilename, subfilesjson):
		self.name = name
		self.manifestuuid = manifestuuid
		self.manifestfilename = manifestfilename
		self.subFiles = subfilesjson

	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)