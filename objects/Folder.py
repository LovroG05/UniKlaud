import json


class Folder:
	def __init__(self, name):
		self.name = name
		self.nodes = {}
		
	def addNode(self, node):
		self.nodes[node.name] = node
		
	def getNodes(self):
		return self.nodes
		
	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)