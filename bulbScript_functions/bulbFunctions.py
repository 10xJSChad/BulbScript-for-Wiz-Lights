functions = []
errorFunction = ["funcNotFound", "print Function not found"]

def getFunction(name):
    for function in functions:
        if function[0] == name:
            return function
    return errorFunction

def addFunction(name, code):
    functions.append([name, code])