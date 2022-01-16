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
        self.fs.split(file=path, split_size=4000000, output_dir=self.tmppath, callback=self.split_cb)  # TODO
        # TODO delete temp after upload

    def merge(self, in_path, out_path, manifest_path):
        # TODO download to temp
        self.fs.merge(input_dir=in_path, output_file=out_path, manifest_file=manifest_path) # TODO
        # TODO delete temp after merge

    def makeUFname(self, filename, _uuid):
        l = filename.split("_")
        return _uuid + "_" + l[-1]


    def split_and_upload(self, path):
        self.split(path)
        # rename /tmp/fs_manifest.csv to /tmp/fs_ + filename + .csv
        filename = path.split("/")[-1]
        _uuid = str(uuid.uuid4())
        os.rename(self.tmppath + "/fs_manifest.csv", self.tmppath + "/fs_" + _uuid + ".csv")
        # upload /tmp/fs_ + filename + .csv to maindrive
        maindrive = self.uniklaud.getMainDrive()
        for drive in self.uniklaud.mountedStorageObjects:
            if drive.storageName == maindrive:
                print("Uploading to maindrive")
                drive.uploadFile(self.tmppath + "/fs_" + _uuid + ".csv", "fs_" + _uuid + ".csv")

        # TODO split split files between providers and write it to /tmp/main.json, then upload it to maindrive

        lines = []
        with open(self.tmppath + "/fs_" + _uuid + ".csv", "r") as f:
            reader = csv.reader(f)
            fields = next(reader)
            for line in reader:
                lines.append(line)
            f.close()

        fileJsons = []
        for file in lines:
            allfree = self.uniklaud.getAllFreeB()
            for storageComponent in self.uniklaud.mountedStorageObjects:
                storageComponent.updateStoragePercentage(allfree)

            storages = self.uniklaud.mountedStorageObjects
            storages.sort(key=lambda x: x.storagePercentage, reverse=False)
            
            print(colorama.Fore.GREEN + "Uploading file: " + file[0] + " to " + storages[0].storageName)
            renamed_file = self.makeUFname(file[0], _uuid)
            os.rename(self.tmppath + "/" + file[0], self.tmppath + "/" + renamed_file)
            storages[0].uploadFile(self.tmppath + "/" + renamed_file, renamed_file)
            fileJsons.append({"name": renamed_file, "actualname": file[0], "storage": storages[0].storageName, "size": file[1], "encoding": file[2], "header": file[3]})
            # delete file from /tmp/file[0]
            filetd = self.tmppath + "/" + renamed_file
            print(colorama.Fore.YELLOW + "Deleting file: " + filetd)
            os.remove(filetd)

        file = File(filename, _uuid, "fs_" + _uuid + ".csv", "fs_" + filename + ".csv", fileJsons)
        self.uniklaud.pwDir.addFile(file)
        self.uniklaud.saveFilesystem()

        maindrive = self.uniklaud.getMainDrive()
        for drive in self.uniklaud.mountedStorageObjects:
            if drive.storageName == maindrive:
                print(colorama.Fore.GREEN + "Uploading to maindrive")
                drive.deleteFile("main.json")
                drive.uploadFile(self.tmppath + "/main.json", "main.json")

    def download_and_merge(self, file, out_path):
        randomConvInt = random.randint(0, 9999)
        os.mkdir(self.tmppath + "/" + str(randomConvInt))

        manifestFilename = file.manifestfilename
        actualManifestFilename = file.actualmanifestname
        maindrive = self.uniklaud.getMainDrive()
        for drive in self.uniklaud.mountedStorageObjects:
            if drive.storageName == maindrive:
                drive.downloadFile(manifestFilename, self.tmppath + "/" + str(randomConvInt) + "/" + actualManifestFilename)

        subfiles_list = []
        for subfile in file.subFiles:
            subfiles_list.append(subfile)

        for subfile in subfiles_list:
            for drive in self.uniklaud.mountedStorageObjects:
                if drive.storageName == subfile["storage"]:
                    print(colorama.Fore.GREEN + "Downloading file: " + subfile["name"] + " from " + drive.storageName)
                    drive.downloadFile(subfile["name"], self.tmppath + "/" + str(randomConvInt) + "/" + subfile["actualname"])

        apathw = self.tmppath + "/" + str(randomConvInt) + "/"
        print(colorama.Fore.YELLOW + apathw)
        self.merge(apathw, out_path + file.name, self.tmppath + "/" + str(randomConvInt) + "/" + actualManifestFilename)
        shutil.rmtree(apathw)

    def remove_file(self, folder, file):
        for subfile in file.subFiles:
            for drive in self.uniklaud.mountedStorageObjects:
                if drive.storageName == subfile["storage"]:
                    print(colorama.Fore.YELLOW + "Deleting file: " + subfile["name"] + " from " + drive.storageName)
                    drive.deleteFile(subfile["name"])

        maindrive = self.uniklaud.getMainDrive()
        for drive in self.uniklaud.mountedStorageObjects:
            if drive.storageName == maindrive:
                drive.deleteFile(file.manifestfilename)

        folder.removeFile(file)
        self.uniklaud.saveFilesystem()
