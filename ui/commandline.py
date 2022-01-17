import colorama
import pyfiglet
import pandas as pd
from packages.MessageUtil import *
import sys, os

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
            if command == "help" or command == "0":
                self.print_header()
                self.print_commands()

            elif command.startswith("mount"):
                args = command.split(" ")
                storagename = args[1]
                provider = args[2]
                size = args[3]
                usednames = self.uniklaud.getUsedStorageNames()
                if provider in usednames:
                    print(colorama.Fore.RED + "Storage name already used!")
                else:
                    self.uniklaud.mountStorage(storagename, provider, size)
                    print(colorama.Fore.GREEN + "Storage object mounted")

            elif command.startswith("unmount"):
                printWarning("Note that this will make any files on the storage unrecoverable!")
                if input("Are you sure? (y/n)") == "y":
                    storagename = command.split(" ")[1]
                    self.uniklaud.unmountStorageObject(storagename)
                    print(colorama.Fore.GREEN + "Storage object unmounted")

            elif command.startswith("listmounted"):
                print(colorama.Fore.CYAN + "Main storage drive: " + self.uniklaud.maindrive)
                print(pd.DataFrame([[i.storageName, i.provider, i.size_bytes] for i in self.uniklaud.mountedStorageObjects]))

            elif command.startswith("maindrive"):
                storageName = command.split(" ")[1]
                self.uniklaud.setMainDrive(storageName)

            elif command.startswith("ls"):
                for i in self.uniklaud.ls()[0]:
                    print(colorama.Fore.CYAN + i)
                for i in self.uniklaud.ls()[1]:
                    print(colorama.Fore.BLUE + i)

            elif command.startswith("cd"):
                self.uniklaud.cd(command.split(" ")[1])

            elif command.startswith("pwd"):
                print(self.uniklaud.pwd)

            elif command.startswith("upload"):
                self.uniklaud.upload(command.split(" ")[1])

            elif command.startswith("download"):
                filename = command.split(" ")[1]
                out_path = command.split(" ")[2]
                self.uniklaud.download(filename, out_path)
            
            elif command.startswith("mkdir"):
                foldername = command.split(" ")[1]
                self.uniklaud.createFolder(foldername)

            elif command.startswith("rmdir"):
                foldername = command.split(" ")[1]
                self.uniklaud.removeFolder(self.uniklaud.pwDir.getFolder(foldername))

            elif command.startswith("rm"):
                filename = command.split(" ")[1]
                rmFolder = self.uniklaud.pwDir

                self.uniklaud.removeFile(rmFolder, rmFolder.getFile(filename))

            elif command == "quit" or command == "exit":
                print(colorama.Fore.RED + "Goodbye!")
                sys.exit()
            
            elif command == "clear":
                os.system('clear')