from fsplit.filesplit import Filesplit
import os
import csv
import json
import colorama

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

    def merge(self, in_path, out_path):
        # TODO download to temp
        self.fs.merge(input_dir=in_path, output_file=out_path) # TODO
        # TODO delete temp after merge

    def split_and_upload(self, path):
        self.split(path)
        # rename /tmp/fs_manifest.csv to /tmp/fs_ + filename + .csv
        filename = path.split("/")[-1]
        os.rename(self.tmppath + "/fs_manifest.csv", self.tmppath + "/fs_" + filename + ".csv")
        # upload /tmp/fs_ + filename + .csv to maindrive
        maindrive = self.uniklaud.getMainDrive()
        for drive in self.uniklaud.mountedStorageObjects:
            if drive.storageName == maindrive:
                print("Uploading to maindrive")
                drive.uploadFile(self.tmppath + "/fs_" + filename + ".csv", "/fs_" + filename + ".csv")

        # TODO split split files between providers and write it to /tmp/main.json, then upload it to maindrive

        lines = []
        with open(self.tmppath + "/fs_" + filename + ".csv", "r") as f:
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
            storages[0].uploadFile(self.tmppath + "/" + file[0], file[0])
            fileJsons.append({"name": file[0], "storage": storages[0].storageName, "size": file[1], "encoding": file[2], "header": file[3]})
            # delete file from /tmp/file[0]
            filetd = self.tmppath + "/" + file[0]
            print(colorama.Fore.YELLOW + "Deleting file: " + filetd)
            os.remove(filetd)

        if not os.path.exists(self.tmppath + "/main.json"):
            with open(self.tmppath + "/main.json", "w") as f:
                f.write("{}")
                f.close()

        config = ""
        files = []
        with open(self.tmppath + "/main.json", "r") as f:
            config = json.load(f)
            if "files" in config:
                files = config["files"]
            f.close()

        with open(self.tmppath + "/main.json", "w") as f:
            _json = {}
            _json["manifestname"] = "fs_" + filename + ".csv"
            _json["subFiles"] = fileJsons
            files.append(_json)
            config["files"] = files
            json.dump(config, f)
            f.close()

        maindrive = self.uniklaud.getMainDrive()
        for drive in self.uniklaud.mountedStorageObjects:
            if drive.storageName == maindrive:
                print(colorama.Fore.GREEN + "Uploading to maindrive")
                drive.deleteFile("main.json")
                drive.uploadFile(self.tmppath + "/main.json", "main.json")


        

# {
#   "files": [
#     {
#       "manifestname": "",
#       "subFiles": [
#         {
#           "name": "",
#           "storage": "",
#           "size": "",
#           "encoding": "",
#           "header": ""
#         },
#         {
#           "name": "",
#           "storage": "",
#           "size": "",
#           "encoding": "",
#           "header": ""
#         }
#       ]
#     }
#   ]
# }