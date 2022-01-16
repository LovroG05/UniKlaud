import colorama

def printError(message):
    print(colorama.Fore.RED + "ERROR: " + message)

def printWarning(message):
    print(colorama.Fore.YELLOW + "WARNING: " + message)

def printLog(message):
    print(colorama.Fore.RESET + message)

def printInfo(message):
    print(colorama.Fore.LIGHTBLUE_EX + "INFO: " + message)