import json


class File:
	def __init__(self, name, uuid):
		self.name = name
		self.uuid = uuid

	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)