from fsplit.filesplit import Filesplit
import sys, os
import storagePlugins.googledrive as googleDrive
import packages.configurator as configurator
import json
import pyfiglet
import colorama


class Uniklaud:
    def __init__(self, mnt):
        self.fs = Filesplit()
        self.split_size = 4000000
        self.tempPath = "/tmp/uniklaud"
        self.mountedStorageObjects = []
        self.providers = ["googleDrive"]
        self.loadMount(mnt)

    def loadMount(self, mnt):
        print(mnt)
        for i in mnt:
            print(i)
            drive = json.loads(i)
            provider = drive["provider"]
            print(provider)
            storagename = drive["storagename"]
            print(storagename)
            if provider == "googleDrive":
                print("true")
                self.mountedStorageObjects.append(googleDrive.GoogleDriveProvider(provider, storagename))
                print("Storage object mounted")
            else:
                print("Unknown storage provider")

    def updateConfigMounted(self, value):
        configMaster = configurator.Configurator("config.json")
        config = configMaster.get_config()
        list = []
        for i in value:
            list.append(json.dumps(i.getJsonData()))
        config["mountedStorageObjects"] = list
        configMaster.write_config(config)

    def split(self, path):
        self.fs.split(file=path, split_size=self.split_size, output_dir=self.tempPath)  # TODO

    def merge(self):
        self.fs.merge(input_dir=self.tempPath) # TODO

    def mountStorageObject(self, storageObject):
        self.mountedStorageObjects.append(storageObject)
        self.updateConfigMounted(self.mountedStorageObjects)

    def unmountStorageObject(self, storageName):
        self.mountedStorageObjects.pop(storageName)
        self.updateConfigMounted(self.mountedStorageObjects)

    def mountStorage(self, storagename, provider):
        if provider == "googleDrive":
            self.mountStorageObject(googleDrive.GoogleDriveProvider(provider, storagename))
            print("Storage object mounted")
        else:
            print("Unknown storage provider")

    def getUsedStorageProviders(self):
        providers = []
        for i in self.mountedStorageObjects:
            providers.append(i.provider)
        return providers

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
        print("(1)  mount <storageName> <provider>")
        print("(2)  unmount <storageName>")
        print("(3)  listmounted --provider <provider>")
        print("(4)  quit")
        print("\n\n\n")

    def mainLoop(self):
        while True:
            command = input(colorama.Fore.GREEN + "Uniklaud> ")
            if command == "help" or command == "0":
                self.print_header()
                self.print_commands()

            elif command.startswith("mount"):
                args = command.split(" ")
                self.mount(args[1], args[2])

            elif command == "unmount":
                print("This command is not implemented yet")

            elif command == "listmounted":
                self.listmounted()

            elif command == "quit":
                print(colorama.Fore.RED + "Goodbye!")
                sys.exit()
            
            elif command == "clear":
                os.system('clear')
    
    # COMMAND FUNCTIONS
    def mount(self, storagename, provider):
        usedproviders = self.uniklaud.getUsedStorageProviders()
        if provider in usedproviders:
            print("Storage provider already mounted")
        else:
            self.uniklaud.mountStorage(storagename, provider)

        self.listmounted()
        


    def unmount(self, storageName):
        if storageName in self.uniklaud.mountedStorageObjects:
            self.uniklaud.unmountStorageObject(storageName)
            print("Storage object unmounted")
        else:
            print("Storage object was never mounted")


    def listmounted(self):
        print(colorama.Fore.YELLOW + "name -------- provider")
        for i in self.uniklaud.mountedStorageObjects:
            print(colorama.Fore.CYAN + i.storageName + " -------- " + i.provider)


if __name__ == '__main__':
    configMaster = configurator.Configurator("config.json")
    config = configMaster.get_config()
    uniklaud = Uniklaud(config["mountedStorageObjects"])
    uniklaudCLI = UniklaudCLI(uniklaud)