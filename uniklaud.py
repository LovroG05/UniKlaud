import sys, os
import storagePlugins.googledrive as googleDrive
import packages.configurator as configurator
import json
import pyfiglet
import colorama
import storagePlugins.dropboxprovider as dropboxprovider


class Uniklaud:
    def __init__(self, mnt, maindrive):
        self.split_size = 4000000
        self.tempPath = "tmp"
        self.mountedStorageObjects = []
        self.providers = ["googleDrive", "dropbox"]
        self.maindrive = maindrive
        self.loadMount(mnt)

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
        configMaster = configurator.Configurator("config.json")
        config = configMaster.get_config()
        config["mainDriveName"] = drive
        configMaster.write_config(config)
        print("Main drive set to " + drive)
        print(colorama.Fore.RED + "DO NOT ATTEMPT TO CHANGE IT!")

    def getMainDrive(self):
        return self.maindrive

    def updateConfigMounted(self, value):
        configMaster = configurator.Configurator("config.json")
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
            with open("dropbox.txt", "w") as f:
                secret = input("Enter your dropbox secret: ")
                f.write(secret)
                f.close()
                
            self.mountStorageObject(dropboxprovider.DropboxProvider(provider, storagename, size))
            print("Storage object mounted")
        else:
            print("Unknown storage provider")

    def getUsedStorageProviders(self):
        providers = []
        for i in self.mountedStorageObjects:
            providers.append(i.provider)
        return providers

    def getAllFreeB(self):
        allfree = 0 # bytes
        for storageComponent in self.mountedStorageObjects:
            allfree = allfree + (storageComponent.size_bytes - storageComponent.getUsedB())

        return allfree

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
        print("(98)  quit")
        print("(99)  clear")
        print("\n\n\n")

    def mainLoop(self):
        while True:
            command = input(colorama.Fore.GREEN + "Uniklaud> ")
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

            elif command == "quit":
                print(colorama.Fore.RED + "Goodbye!")
                sys.exit()
            
            elif command == "clear":
                os.system('clear')
    
    # COMMAND FUNCTIONS
    def mount(self, storagename, provider, size):
        usedproviders = self.uniklaud.getUsedStorageProviders()
        if provider in usedproviders:
            print("Storage provider already mounted")
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


if __name__ == '__main__':
    configMaster = configurator.Configurator("config.json")
    config = configMaster.get_config()
    uniklaud = Uniklaud(config["mountedStorageObjects"], config["mainDriveName"])
    uniklaudCLI = UniklaudCLI(uniklaud)