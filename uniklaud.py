import sys, os
import storagePlugins.googledrive as googleDrive
from packages.configurator import Configurator
from packages.splitter import Splitter
import json
import pyfiglet
import colorama
import storagePlugins.dropboxprovider as dropboxprovider
import random
from flatten_json import flatten, unflatten
import jsonpickle
from objects.File import File
from objects.Folder import Folder


class Uniklaud:
    def __init__(self, mnt, config):
        self.split_size = 4000000
        self.tempPath = "tmp"
        self.mountedStorageObjects = []
        self.providers = ["googleDrive", "dropbox"]
        self.maindrive = config["mainDriveName"]
        self.config = config
        self.splitter = Splitter(self.split_size, self.tempPath, self)
        
        self.loadMount(mnt)
        if self.maindrive != "":
            if self.mountedStorageObjects != []:
                self.getMainJson()

        self.filesystem = None
        self.pwd = "/"
        self.pwDir = None
        self.filesystem = self.loadFilesystem()
        self.cd("/")
        

    def loadFilesystem(self):
        root:Folder = None
        with open(self.tempPath + "/" + "main.json") as f:
            root = jsonpickle.decode(f.read())
            f.close()

        return root

    def saveFilesystem(self):
        rootString = jsonpickle.encode(self.filesystem)

        with open(self.tempPath + "/" + "main.json", 'w') as fp:
            fp.write(rootString)
            fp.close()

    def cd(self, path):  # TODO ../..
        if path == "..":
            pathArr = self.pwd.split("/")
            pathArr = pathArr[:-1]
            finalPath = "/" + "".join(pathArr)

            self.cd(finalPath)
        elif path == "/":
            self.pwd = "/"
            self.pwDir = self.filesystem
        else:
            if path[0] == '/':
                pathParts = path.split("/")
                pathParts = pathParts[1:]
                self.pwDir = self.filesystem
                self.pwd = ""
                
                for i in pathParts:
                    self.pwDir = self.pwDir.getFolders()[i]
                    self.pwd = self.pwd + "/" + self.pwDir.name
            else:
                pathParts = path.split("/")

                for i in pathParts:
                    if self.pwd == "/":
                        self.pwDir = self.pwDir.getFolders()[i]
                        self.pwd = self.pwd + self.pwDir.name
                    else:
                        self.pwDir = self.pwDir.getFolders()[i]
                        self.pwd = self.pwd + "/" + self.pwDir.name

    def ls(self):
        list = []
        list.append(self.pwDir.folders)
        list.append(self.pwDir.files)
        return list


    def getMainJson(self):
        if not os.path.isdir(self.tempPath):
            os.mkdir(self.tempPath)
        for i in self.mountedStorageObjects:
            if i.storageName == self.maindrive:
                i.downloadFile("main.json", "tmp/main.json")

    def loadMount(self, mnt):
        print(mnt)
        for i in mnt:
            drive = json.loads(i)
            provider = drive["provider"]
            storagename = drive["storagename"]
            size = drive["size_bytes"]
            if provider == "googleDrive":
                self.mountedStorageObjects.append(googleDrive.GoogleDriveProvider(provider, storagename, size))
                print("Storage object mounted")
            elif provider == "dropbox":
                self.mountedStorageObjects.append(dropboxprovider.DropboxProvider(provider, storagename, size))
                print("Storage object mounted")
            else:
                print("Unknown storage provider")

    def setMainDrive(self, drive):
        self.maindrive = drive
        configMaster = Configurator("config.json")
        config = configMaster.get_config()
        config["mainDriveName"] = drive
        configMaster.write_config(config)
        print("Main drive set to " + drive)
        print(colorama.Fore.RED + "DO NOT ATTEMPT TO CHANGE IT!")

    def getMainDrive(self):
        return self.maindrive

    def updateConfigMounted(self, value):
        configMaster = Configurator("config.json")
        config = configMaster.get_config()
        list = []
        for i in value:
            list.append(json.dumps(i.getJsonData()))
        config["mountedStorageObjects"] = list
        configMaster.write_config(config)

    def mountStorageObject(self, storageObject):
        self.mountedStorageObjects.append(storageObject)
        self.updateConfigMounted(self.mountedStorageObjects)

    def unmountStorageObject(self, storageName):
        self.mountedStorageObjects.pop(storageName)
        self.updateConfigMounted(self.mountedStorageObjects)

    def mountStorage(self, storagename, provider, size):
        if provider == "googleDrive":
            self.mountStorageObject(googleDrive.GoogleDriveProvider(provider, storagename, size))
            print("Storage object mounted")
        elif provider == "dropbox":
            self.mountStorageObject(dropboxprovider.DropboxProvider(provider, storagename, size, config["dropbox_key"], config["dropbox_secret"]))
            print("Storage object mounted")
        else:
            print("Unknown storage provider")

    def getUsedStorageNames(self):
        names = []
        for i in self.mountedStorageObjects:
            names.append(i.storageName)
        return names

    def getAllFreeB(self):
        allfree = 0 # bytes
        for storageComponent in self.mountedStorageObjects:
            allfree = allfree + (int(storageComponent.size_bytes) - int(storageComponent.getUsedB()))

        return allfree

    def upload(self, filepath):
        self.splitter.split_and_upload(filepath)
        print(colorama.Fore.GREEN + "File uploaded!")
        if random.randint(0, 999999) == 0:
            print(colorama.Fore.BLUE + "POGGERS!")

class UniklaudCLI:
    def __init__(self, uniklaud):
        self.result = pyfiglet.figlet_format("Uniklaud", font="bulbhead")
        self.uniklaud = uniklaud
        self.print_header()
        self.print_commands()
        self.mainLoop()
        

    def print_header(self):
        print(colorama.Fore.GREEN + self.result)
        print("A RAID-like file system for free online storage providers")
        print("\n\n\n")

    def print_commands(self):
        print("Available commands:")
        print("(0)  help")
        print("(1)  mount <storageName> <provider> <size[Bytes]>")
        print("(2)  unmount <storageName>")
        print("(3)  listmounted --provider <provider>")
        print("(4)  maindrive <storageName>")
        print("(5)  ls")
        print("(6)  upload <file path>")
        print("(7)  download <csv filename> <output file>")
        print("(98)  quit")
        print("(99)  clear")
        print("\n\n\n")

    def mainLoop(self):
        while True:
            command = input(colorama.Fore.GREEN + self.uniklaud.pwd + "> ")
            if command == "help" or command == "0":
                self.print_header()
                self.print_commands()

            elif command.startswith("mount"):
                args = command.split(" ")
                self.mount(args[1], args[2], args[3])

            elif command == "unmount":
                print(colorama.Fore.RED + "This command is not implemented yet")

            elif command.startswith("listmounted"):
                self.listmounted()

            elif command.startswith("maindrive"):
                self.maindrive(command.split(" ")[1])

            elif command.startswith("ls"):
                self.ls()

            elif command.startswith("pwd"):
                print(self.uniklaud.pwd)

            elif command.startswith("cd"):
                self.uniklaud.cd(command.split(" ")[1])

            elif command.startswith("upload"):
                self.upload(command.split(" ")[1])

            elif command.startswith("download"):
                filename = command.split(" ")[1]
                out_path = command.split(" ")[2]
                self.download(filename, out_path)

            elif command == "quit":
                print(colorama.Fore.RED + "Goodbye!")
                sys.exit()
            
            elif command == "clear":
                os.system('clear')
    
    # COMMAND FUNCTIONS
    def mount(self, storagename, provider, size):
        usednames = self.uniklaud.getUsedStorageNames()
        if provider in usednames:
            print(colorama.Fore.RED + "Storage name already used!")
        else:
            self.uniklaud.mountStorage(storagename, provider, size)

        self.listmounted()

    def unmount(self, storageName):
        if storageName in self.uniklaud.mountedStorageObjects:
            self.uniklaud.unmountStorageObject(storageName)
            print("Storage object unmounted")
        else:
            print("Storage object was never mounted")

    def listmounted(self):
        print(colorama.Fore.MAGENTA + "Main storage drive: " + self.uniklaud.maindrive)
        print(colorama.Fore.YELLOW + "name -------- provider -------- size[Bytes]")
        for i in self.uniklaud.mountedStorageObjects:
            print(colorama.Fore.CYAN + i.storageName + " -------- " + i.provider + " -------- " + i.size_bytes)

    def maindrive(self, storageName):
        if self.uniklaud.maindrive == "":
            self.uniklaud.setMainDrive(storageName)
        else:
            print(colorama.Fore.YELLOW + "Main drive already set")

    def ls(self):  # TODO
        for i in self.uniklaud.ls()[0]:
            print(colorama.Fore.CYAN + i)
        for i in self.uniklaud.ls()[1]:
            print(colorama.Fore.BLUE + i)

    def upload(self, filepath):
        self.uniklaud.upload(filepath)

    def download(self, filename, out_path):
        with open("tmp/main.json", "r") as mj:
            mainjson = json.load(mj)
            mj.close()
        
        filejson = ""
        for i in mainjson["files"]:
            if i["manifestname"] == filename:
                filejson = i

        if filejson != "": 
            self.splitter.download_and_merge(filejson, out_path)
            print(colorama.Fore.GREEN + "File downloaded!")
        else:
            print(colorama.Fore.RED + "File not found!")


if __name__ == '__main__':
    configMaster = Configurator("config.json")
    config = configMaster.get_config()
    uniklaud = Uniklaud(config["mountedStorageObjects"], config)
    uniklaudCLI = UniklaudCLI(uniklaud)
