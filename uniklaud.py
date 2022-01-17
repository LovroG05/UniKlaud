import sys, os
import storagePlugins.googledrive as googleDrive
from packages.configurator import Configurator
from packages.splitter import Splitter
import json
import pyfiglet
import colorama
import storagePlugins.dropboxprovider as dropboxprovider
import random
import jsonpickle
from objects.File import File
from objects.Folder import Folder
import pandas as pd
from packages.MessageUtil import *
from dotenv import load_dotenv

class Uniklaud:
    def __init__(self, mnt, config):
        self.split_size = 4000000
        self.tempPath = "tmp"
        self.mountedStorageObjects = []
        self.maindrive = config["mainDriveName"]
        self.providers = ["googleDrive", "dropbox"]
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

    def uploadMainJson(self):
        for drive in self.mountedStorageObjects:
            if drive.storageName == self.maindrive:
                print(colorama.Fore.GREEN + "Uploading to maindrive")
                try:
                    drive.deleteFile("main.json")
                    drive.uploadFile(self.tempPath + "/main.json", "main.json")
                except Exception as e:
                    printError("Error while uploading the main.json file: " + str(e))
        

    def loadFilesystem(self):
        root:Folder = None
        try:
            with open(self.tempPath + "/" + "main.json") as f:
                root = jsonpickle.decode(f.read())
                f.close()
        except FileNotFoundError as e:
            printError("No main.json found")
            printError("Trying to fetch main.json from " + self.maindrive)
            self.getMainJson()

        return root

    def saveFilesystem(self):
        try:
            rootString = jsonpickle.encode(self.filesystem)
            with open(self.tempPath + "/" + "main.json", 'w') as fp:
                fp.write(rootString)
                fp.close()
        except Exception as e:
            printError("Error while saving filesystem: " + str(e))

        self.uploadMainJson()

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
                    try:
                        folderToCd = self.pwDir.getFolder(i)

                        self.pwDir = self.pwDir.getFolder(i)
                        self.pwd = self.pwd + "/" + self.pwDir.name
                    except KeyError:
                        printError("Folder does not exist")
                        break
            else:
                pathParts = path.split("/")

                for i in pathParts:
                    try:
                        folderToCd = self.pwDir.getFolder(i)
                        
                        if self.pwd == "/":
                            self.pwDir = folderToCd
                            self.pwd = self.pwd + self.pwDir.name
                        else:
                            self.pwDir = folderToCd
                            self.pwd = self.pwd + "/" + self.pwDir.name    
                    except KeyError:
                        printError("Folder does not exist")
                        break

    def ls(self):
        list = []
        list.append(self.pwDir.folders)
        list.append(self.pwDir.files)
        return list
        
    def createFolder(self, folderName):
        folders = self.pwDir.getFolders().keys()
        
        if folderName not in folders:
            self.pwDir.addFolder(Folder(folderName))
            self.saveFilesystem()
        else:
            printError("Folder with that name already exists")

    def removeFile(self, folder, file):
        self.splitter.remove_file(folder, file)

    def removeFolder(self, folder):
        try:
            fileDict = folder.getFiles()
            folderDict = folder.getFolders()
            
            fileList = []
            for i in fileDict:
                fileList.append(fileDict[i])

            for i in fileList:
                self.removeFile(folder, i)
            
            folderList = []
            for i in folderDict:
                folderList.append(folderDict[i])
            
            for i in folderList:
                self.removeFolder(i)

            self.pwDir.removeFolder(folder)
            self.saveFilesystem()

        except KeyError:
            printError("Folder does not exist")

    def getMainJson(self):
        try:
            if not os.path.isdir(self.tempPath):
                os.mkdir(self.tempPath)
            for i in self.mountedStorageObjects:
                if i.storageName == self.maindrive:
                    if "main.json" in [j["title"] for j in i.listFiles()]:
                        i.downloadFile("main.json", self.tempPath + "/main.json")
                        break
                    else:
                        printWarning("No main.json found on maindrive")
                        with open(self.tempPath + "/main.json", 'w') as fp:
                            rootString = jsonpickle.encode(Folder("root"))
                            fp.write(rootString)
                            fp.close()
                        self.saveFilesystem()
        except Exception as e:
            printError("Error while downloading main.json: " + str(e))

    def loadMount(self, mnt):
        for i in mnt:
            drive = json.loads(i)
            provider = drive["provider"]
            storagename = drive["storagename"]
            size = drive["size_bytes"]
            if provider == "googleDrive":
                try:
                    self.mountedStorageObjects.append(googleDrive.GoogleDriveProvider(provider, storagename, size))
                    print(colorama.Fore.GREEN + "Storage object mounted")
                except Exception as e:
                    printError("Error while mounting drive: " + str(e))
                
            elif provider == "dropbox":
                try:
                    self.mountedStorageObjects.append(dropboxprovider.DropboxProvider(provider, storagename, size, os.getenv("DROPBOX_KEY"), os.getenv("DROPBOX_SECRET")))
                    print(colorama.Fore.GREEN + "Storage object mounted")
                except Exception as e:
                    printError("Error while mounting drive: " + str(e))
            else:
                printError("Unknown storage provider")

    def setMainDrive(self, drive):
        printWarning("Attempting to change it may cause files to be unrecoverable")
        answer = input("Are you sure you want to change the main drive? (y/n)")
        if answer == "y":
            self.maindrive = drive
            configMaster = Configurator("config.json")
            config = configMaster.get_config()
            config["mainDriveName"] = drive
            configMaster.write_config(config)
            print("Main drive set to " + drive)
        

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
        for i in self.mountedStorageObjects:
            if i.storageName == storageName:
                try:
                    self.mountedStorageObjects.remove(i)
                    self.updateConfigMounted(self.mountedStorageObjects)
                except Exception as e:
                    printError("Error while unmounting drive: " + str(e))

    def mountStorage(self, storagename, provider, size):
        if provider == "googleDrive":
            try:
                self.mountStorageObject(googleDrive.GoogleDriveProvider(provider, storagename, size))
                print("Storage object mounted")
            except Exception as e:
                printError("Error while mounting drive: " + str(e))
        elif provider == "dropbox":
            try:
                self.mountStorageObject(dropboxprovider.DropboxProvider(provider, storagename, size, os.getenv("DROPBOX_KEY"), os.getenv("DROPBOX_SECRET")))
                print("Storage object mounted")
            except Exception as e:
                printError("Error while mounting drive: " + str(e))
        else:
            printError("Unknown storage provider")

    def getUsedStorageNames(self):
        names = []
        if len(self.mountedStorageObjects) > 0:
            for i in self.mountedStorageObjects:
                names.append(i.storageName)
        return names

    def getAllFreeB(self):
        allfree = 0 # bytes
        for storageComponent in self.mountedStorageObjects:
            allfree = allfree + (int(storageComponent.size_bytes) - int(storageComponent.getUsedB()))

        return allfree

    def upload(self, filepath):
        try:
            self.splitter.split_and_upload(filepath)
            print(colorama.Fore.GREEN + "File uploaded!")
            if random.randint(0, 999999) == 0:
                print(colorama.Fore.BLUE + "POGGERS!")
        except Exception as e:
            printError("Error while uploading file: " + str(e))

    def download(self, filename, out_path):
        fileToDownload = None
        try:
            fileToDownload = self.pwDir.getFiles()[filename]
        except KeyError:
            printError("File does not exist")

        if fileToDownload != None: 
            try:
                self.splitter.download_and_merge(fileToDownload, out_path)
                print(colorama.Fore.GREEN + "File downloaded!")
            except Exception as e:
                printError("Error while downloading file: " + str(e))
        else:
            printError("File not found!")

class UniklaudCLI:
    def __init__(self, uniklaud):
        self.result = pyfiglet.figlet_format("Uniklaud", font="bulbhead")
        self.uniklaud = uniklaud
        self.commands = [
            {"command": "help", "arguments":""},
            {"command": "mount", "arguments":"<provider> <storagename> <size_bytes>"},
            {"command": "unmount", "arguments":"<storagename>"},
            {"command": "maindrive", "arguments":"<storageName>"},
            {"command": "ls", "arguments":""},
            {"command": "pwd", "arguments":""},
            {"command": "cd", "arguments":"<path>"},
            {"command": "upload", "arguments":"<file path>"},
            {"command": "mkdir", "arguments":"<folderName>"},
            {"command": "download", "arguments":"<fileName> <output/file/path>"},
            {"command": "rm", "arguments":"<fileName>"},
            {"command": "rmdir", "arguments":"<folderName>"},
            {"command": "exit", "arguments":""},
            {"command": "clear", "arguments":""}
        ]
        self.print_header()
        self.print_commands()
        self.mainLoop()
        

    def print_header(self):
        print(colorama.Fore.GREEN + self.result)
        print("A RAID-like file system for free online storage providers")
        print("\n\n\n")

    def print_commands(self):
        print("Available commands:")
        print(pd.DataFrame(self.commands))
        print("\n\n\n")

    def mainLoop(self):
        while True:
            command = input(colorama.Fore.GREEN + self.uniklaud.pwd + "> ")
            if command.startswith("help"):
                self.print_header()
                self.print_commands()

            elif command.startswith("mount"):
                args = command.split(" ")
                if len(args) == 4:
                    storagename = args[1]
                    provider = args[2]
                    size = args[3]
                    usednames = self.uniklaud.getUsedStorageNames()
                    if provider in usednames:
                        print(colorama.Fore.RED + "Storage name already used!")
                    else:
                        self.uniklaud.mountStorage(storagename, provider, size)
                        print(colorama.Fore.GREEN + "Storage object mounted")
                else:
                    printWarning("Invalid number of arguments")

            elif command.startswith("unmount"):
                args = command.split(" ")
                if len(args) == 2:
                    printWarning("Note that this will make any files on the storage unrecoverable!")
                    if input("Are you sure? (y/n)") == "y":
                        storagename = args[1]
                        self.uniklaud.unmountStorageObject(storagename)
                        print(colorama.Fore.GREEN + "Storage object unmounted")
                else:
                    printWarning("Invalid number of arguments")

            elif command.startswith("listmounted"):
                print(colorama.Fore.CYAN + "Main storage drive: " + self.uniklaud.maindrive)
                print(pd.DataFrame([[i.storageName, i.provider, i.size_bytes] for i in self.uniklaud.mountedStorageObjects]))

            elif command.startswith("maindrive"):
                args = command.split(" ")
                if len(args) == 2:
                    storageName = args[1]
                    self.uniklaud.setMainDrive(storageName)
                else:
                    printWarning("Invalid number of arguments")

            elif command.startswith("ls"):
                for i in self.uniklaud.ls()[0]:
                    print(colorama.Fore.CYAN + i)
                for i in self.uniklaud.ls()[1]:
                    print(colorama.Fore.BLUE + i)

            elif command.startswith("cd"):
                args = command.split(" ")
                if len(args) == 2:
                    self.uniklaud.cd(args[1])
                else:
                    printWarning("Invalid number of arguments")

            elif command.startswith("pwd"):
                print(self.uniklaud.pwd)

            elif command.startswith("upload"):
                args = command.split(" ")
                if len(args) == 2:
                    if os.path.isfile(args[1]):
                        self.uniklaud.upload(args[1])
                    else:
                        printInfo("File does not exist")
                else:
                    printWarning("Invalid number of arguments")

            elif command.startswith("download"):
                args = command.split(" ")
                if len(args) == 3:
                    filename = args[1]
                    out_path = args[2]
                    self.uniklaud.download(filename, out_path)
                else:
                    printWarning("Invalid number of arguments")
            
            elif command.startswith("mkdir"):
                args = command.split(" ")
                if len(args) == 2:
                    foldername = args[1]
                    self.uniklaud.createFolder(foldername)
                else:
                    printWarning("Invalid number of arguments")

            elif command.startswith("rmdir"):
                args = command.split(" ")
                if len(args) == 2:
                    foldername = args[1]
                    self.uniklaud.removeFolder(self.uniklaud.pwDir.getFolder(foldername))
                else:
                    printWarning("Invalid number of arguments")

            elif command.startswith("rm"):
                args = command.split(" ")
                if len(args) == 2:
                    filename = args[1]
                    rmFolder = self.uniklaud.pwDir

                    if filename in rmFolder.getFiles():
                        self.uniklaud.removeFile(rmFolder, rmFolder.getFile(filename))
                    else:
                        printWarning("File does not exist")
                else:
                    printWarning("Invalid number of arguments")

            elif command == "quit" or command == "exit":
                print(colorama.Fore.RED + "Goodbye!")
                sys.exit()
            
            elif command == "clear":
                os.system('clear')


if __name__ == '__main__':
    load_dotenv()
    if os.getenv("UNIKLAUD_API_KEY") == "":
        printError("Dropbox API key and secret not set!")
    if not os.path.isfile("client_secrets.json"):
        printError("client_secrets.json not found!")
    if not os.path.isfile("config.json"):
        printError("config.json not found!")
        exit(1)
    configMaster = Configurator("config.json")
    config = configMaster.get_config()
    uniklaud = Uniklaud(config["mountedStorageObjects"], config)
    uniklaudCLI = UniklaudCLI(uniklaud)
