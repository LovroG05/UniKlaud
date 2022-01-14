import json


class File:
	def __init__(self, name, manifestuuid, manifestname, subfiles):
		self.name = name
		self.manifestuuid = manifestuuid
		self.manifestname = manifestname
		self.subFiles = subfiles

	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)