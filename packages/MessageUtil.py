import colorama
import datetime

def printError(message):
    print(colorama.Fore.RED + "ERROR: " + message)
    logToFile("ERROR: " + message)

def printWarning(message):
    print(colorama.Fore.YELLOW + "WARNING: " + message)
    logToFile("WARNING: " + message)

def printLog(message):
    print(colorama.Fore.RESET + message)

def printInfo(message):
    print(colorama.Fore.LIGHTBLUE_EX + "INFO: " + message)

def logToFile(message):
    with open("../log.txt", "a") as f:
        f.write(message + " Time: " + str(datetime.datetime.now()) + "\n")
        f.close()