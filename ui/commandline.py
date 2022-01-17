import pyfiglet
import sys
import os
import colorama
import pandas as pd
from packages.MessageUtil import *

class UniklaudCLI:
    def __init__(self, uniklaud):
        self.result = pyfiglet.figlet_format("Uniklaud", font="bulbhead")
        self.uniklaud = uniklaud
        self.commands = [
            {"command": "help", "arguments":""},
            {"command": "mount", "arguments":"<storagename> <provider> <size_bytes>"},
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
