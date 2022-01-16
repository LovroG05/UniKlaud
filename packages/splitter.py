from fsplit.filesplit import Filesplit
import os
import csv
import json
import colorama
import uuid
import random
import shutil
from objects.File import File
from objects.Folder import Folder
from packages.MessageUtil import *

class Splitter:
    def __init__(self, filesize, tmppath, uniklaud):
        self.fs = Filesplit()
        self.filesize = filesize
        self.tmppath = tmppath
        self.uniklaud = uniklaud

    def split_cb(self, f, s):
        print("file: {0}, size: {1}".format(f, s))

    def merge_cb(self, f, s):
        print("file: {0}, size: {1}".format(f, s))

    def split(self, path):
        try:
            self.fs.split(file=path, split_size=4000000, output_dir=self.tmppath, callback=self.split_cb)
        except Exception as e:
            printError("Error while splitting file: " + str(e))

    def merge(self, in_path, out_path, manifest_path):
        try:
            self.fs.merge(input_dir=in_path, output_file=out_path, manifest_file=manifest_path)
        except Exception as e:
            printError("Error while merging files: " + str(e))

    def makeUFname(self, filename, _uuid):
        l = filename.split("_")
        return _uuid + "_" + l[-1]


    def split_and_upload(self, path):
        self.split(path)

        filename = path.split("/")[-1]
        _uuid = str(uuid.uuid4())
        try:
            os.rename(self.tmppath + "/fs_manifest.csv", self.tmppath + "/fs_" + _uuid + ".csv")
        except Exception as e:
            printError("Error while renaming manifest file: " + str(e))

        maindrive = self.uniklaud.getMainDrive()
        for drive in self.uniklaud.mountedStorageObjects:
            if drive.storageName == maindrive:
                print("Uploading to maindrive")
                try:
                    drive.uploadFile(self.tmppath + "/fs_" + _uuid + ".csv", "fs_" + _uuid + ".csv")
                except Exception as e:
                    printError("Error while uploading manifest file: " + str(e))

        try:
            lines = []
            with open(self.tmppath + "/fs_" + _uuid + ".csv", "r") as f:
                reader = csv.reader(f)
                fields = next(reader)
                for line in reader:
                    lines.append(line)
                f.close()
        except Exception as e:
            printError("Error while reading manifest file: " + str(e))

        fileJsons = []
        for file in lines:
            allfree = self.uniklaud.getAllFreeB()
            for storageComponent in self.uniklaud.mountedStorageObjects:
                storageComponent.updateStoragePercentage(allfree)

            storages = self.uniklaud.mountedStorageObjects
            storages.sort(key=lambda x: x.storagePercentage, reverse=False)
            
            print(colorama.Fore.GREEN + "Uploading file: " + file[0] + " to " + storages[0].storageName)
            renamed_file = self.makeUFname(file[0], _uuid)
            try:
                os.rename(self.tmppath + "/" + file[0], self.tmppath + "/" + renamed_file)
            except Exception as e:
                printError("Error while renaming file: " + str(e))

            try:
                storages[0].uploadFile(self.tmppath + "/" + renamed_file, renamed_file)
            except Exception as e:
                printError("Error while uploading file: " + str(e))

            fileJsons.append({"name": renamed_file, "actualname": file[0], "storage": storages[0].storageName, "size": file[1], "encoding": file[2], "header": file[3]})
            # delete file from /tmp/file[0]
            filetd = self.tmppath + "/" + renamed_file
            print(colorama.Fore.YELLOW + "Deleting file: " + filetd)
            try:
                os.remove(filetd)
            except Exception as e:
                printError("Error while deleting file: " + str(e))

        file = File(filename, _uuid, "fs_" + _uuid + ".csv", "fs_" + filename + ".csv", fileJsons)
        self.uniklaud.pwDir.addFile(file)
        self.uniklaud.saveFilesystem()

        maindrive = self.uniklaud.getMainDrive()
        for drive in self.uniklaud.mountedStorageObjects:
            if drive.storageName == maindrive:
                print(colorama.Fore.GREEN + "Uploading to maindrive")
                try:
                    drive.deleteFile("main.json")
                    drive.uploadFile(self.tmppath + "/main.json", "main.json")
                except Exception as e:
                    printError("Error while uploading the main.json file: " + str(e))

    def download_and_merge(self, file, out_path):
        randomConvInt = random.randint(0, 9999)
        try:
            os.mkdir(self.tmppath + "/" + str(randomConvInt))
        except Exception as e:
            printError("Error while creating tmp subfolder: " + str(e))

        manifestFilename = file.manifestfilename
        actualManifestFilename = file.actualmanifestname
        maindrive = self.uniklaud.getMainDrive()
        for drive in self.uniklaud.mountedStorageObjects:
            if drive.storageName == maindrive:
                try:
                    drive.downloadFile(manifestFilename, self.tmppath + "/" + str(randomConvInt) + "/" + actualManifestFilename)
                except Exception as e:
                    printError("Error while downloading manifest file: " + str(e))

        subfiles_list = []
        for subfile in file.subFiles:
            subfiles_list.append(subfile)

        for subfile in subfiles_list:
            for drive in self.uniklaud.mountedStorageObjects:
                if drive.storageName == subfile["storage"]:
                    print(colorama.Fore.GREEN + "Downloading file: " + subfile["name"] + " from " + drive.storageName)
                    try:
                        drive.downloadFile(subfile["name"], self.tmppath + "/" + str(randomConvInt) + "/" + subfile["actualname"])
                    except Exception as e:
                        printError("Error while downloading partfile: " + str(e))

        apathw = self.tmppath + "/" + str(randomConvInt) + "/"
        print(colorama.Fore.YELLOW + apathw)
        self.merge(apathw, out_path + file.name, self.tmppath + "/" + str(randomConvInt) + "/" + actualManifestFilename)
        try:
            shutil.rmtree(apathw)
        except Exception as e:
            printWarning("Error while deleting tmp subfolder: " + str(e))

    def remove_file(self, folder, file):
        for subfile in file.subFiles:
            for drive in self.uniklaud.mountedStorageObjects:
                if drive.storageName == subfile["storage"]:
                    try:
                        print(colorama.Fore.YELLOW + "Deleting file: " + subfile["name"] + " from " + drive.storageName)
                        drive.deleteFile(subfile["name"])
                    except Exception as e:
                        printError("Error while deleting partfile: " + str(e))

        maindrive = self.uniklaud.getMainDrive()
        for drive in self.uniklaud.mountedStorageObjects:
            if drive.storageName == maindrive:
                try:
                    drive.deleteFile(file.manifestfilename)
                except Exception as e:
                    printError("Error while deleting manifest file: " + str(e))

        folder.removeFile(file)
        self.uniklaud.saveFilesystem()

        maindrive = self.uniklaud.getMainDrive()
        for drive in self.uniklaud.mountedStorageObjects:
            if drive.storageName == maindrive:
                print(colorama.Fore.GREEN + "Uploading to maindrive")
                try:
                    drive.deleteFile("main.json")
                    drive.uploadFile(self.tmppath + "/main.json", "main.json")
                except Exception as e:
                    printError("Error while uploading the main.json file: " + str(e))
