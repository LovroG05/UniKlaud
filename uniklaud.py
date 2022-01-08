from fsplit.filesplit import Filesplit
import sys, os
import click
import storagePlugins.googledrive as googleDrive
import packages.configurator as configurator


class Uniklaud:
    def __init__(self, mnt):
        self.fs = Filesplit()
        self.split_size = 6291456
        self.tempPath = "/tmp/uniklaud"
        self.mountedStorageObjects = mnt
        self.providers = ["googleDrive"]

    def updateConfigMounted(self, value):
        configMaster = configurator.Configurator("config.json")
        config = configMaster.get_config()
        for i in value:
            config["mountedStorageObjects"] = value[i].getJsonData()
        configMaster.write_config(config)

    def split(self, path):
        self.fs.split(file=path, split_size=self.split_size, output_dir=self.tempPath)  # TODO

    def merge(self):
        self.fs.merge(input_dir=self.tempPath) # TODO

    def mountStorageObject(self, storageObject, storageName):
        self.mountedStorageObjects[storageName] = storageObject
        self.updateConfigMounted(self.mountedStorageObjects)

    def unmountStorageObject(self, storageName):
        self.mountedStorageObjects.pop(storageName)
        self.updateConfigMounted(self.mountedStorageObjects)


@click.group()
def main():
    pass

@main.command()
@click.argument('storagename')
@click.argument("provider")
def mount(storagename, provider):
    if provider == "googleDrive":
        if storagename in uniklaud.mountedStorageObjects:
            print("Storage object already mounted")
        else:
            uniklaud.mountStorageObject(googleDrive.GoogleDriveProvider(provider, storagename), storagename)
            print("Storage object mounted")
    else:
        print("Unknown storage provider")

@main.command()
@click.argument('storageName')
def unmount(storageName):
    if storageName in uniklaud.mountedStorageObjects:
        uniklaud.unmountStorageObject(storageName)
        print("Storage object unmounted")
    else:
        print("Storage object was never mounted")

@main.command()
@click.option("--provider")
def listmounted(provider=""):
    if provider == "":
        print("Mounted storage objects:")
        for storageName in uniklaud.mountedStorageObjects:
            print(storageName) # make it nicer
    else:
        if provider in uniklaud.providers: # prolly doesnt work
            for p in uniklaud.mountedStorageObjects:
                print("Storage objects for provider: " + provider)
                if p.provider == provider:
                    print(p.storageName) # again, make it nicer


if __name__ == '__main__':
    configMaster = configurator.Configurator("config.json")
    config = configMaster.get_config()
    uniklaud = Uniklaud(config["mountedStorageObjects"])
    main()