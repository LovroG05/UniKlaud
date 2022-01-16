import jsonpickle
from objects.File import File
from objects.Folder import Folder

root = Folder("root")
root.addFolder(Folder("td"))
root.getFolders()["td"].addFolder(Folder("sub2"))

print(jsonpickle.encode(root))