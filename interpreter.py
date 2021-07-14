import asyncio
import sys
import time
import config
import random
from bulbScript_functions import bulbSet, bulbVariables, bulbFunctions
from user_functions import customFunctions

funcName = ""
funcCode = []
recordCode = False
skip = False

#Strips leading spaces
def stripSpaces(cmd):
    return(cmd.lstrip())

async def initialize(script):
    await bulbSet.initialize(config.broadcastSpace)
    await parseCode(script)
    
async def parseCommand(cmd):
    global funcName, funcCode, recordCode, skip
    cmd = stripSpaces(cmd) #Strips leading spaces
    cmdUnchanged = cmd
    cmd = cmd.split("//")[0] #Strips everything following "//" in a line, so "//" may be used to write comments in BulbScript scripts.
    cmd = cmd.lower() #Converts the line to lowercase to prepare it for further parsing
    splitCmd = cmd.split(" ") #Splits the string by space to prepare for further parsing
    
    if splitCmd[0] == "end" and splitCmd[1] == "if" and skip == True: #Checks if the first word in the splitCmd list is "end", then checks if
        #the second word is "if", marking the end of an if statement.
        skip = False #Sets the skip variable to false, making the interpreter stop ignoring future lines of BulbScript code.
        
    if skip: return
    
    if recordCode: funcCode.append(cmd) #Appends lines of BulbScript code to the funcCode list if a function has been declared    
    if splitCmd[0] == "func":
        funcName = splitCmd[1] #Sets the function name to the first word after a space
        recordCode = True #A function has been declared, so recordCode is now true
        #all lines of code until an 'end func' statement will be appended into the funcCode list.
    if splitCmd[0] == "end" and splitCmd[1] == "func":
        funcCode.pop(-1) #Removes the last entry in the funcCode list. The last entry will always be 'end func', and we don't want that
        bulbFunctions.addFunction(funcName, funcCode) #Adds the function to the function list in bulbFunctions
        funcCode = [] 
        recordCode = False
    if splitCmd[0] == "call": #Checks for a 'call' command, which is used to call a function
        bulbFunction = bulbFunctions.getFunction(splitCmd[1])[1] #Gets the code of the function called. 
        #bulbFunctions.getFunction takes a function name and returns ["Function Name", ["Function code]]
        #The code above will store only the code in bulbFunction
        if len(splitCmd) == 3 and splitCmd[2] != "": #Checks if there's a third argument, which would be used to call a function X amount of times
            for i in range(0, int(splitCmd[2])): #Calls the function however many time specified. ex. "call testFunc 10" <- calls testFunc 10 times
                await parseCode(bulbFunction, True) #Sends the function code to be parsed and ran, with runOnce set to True to prevent it from looping infinitely
            return        
        await parseCode(bulbFunction, True)
        
    if not recordCode:
        if splitCmd[0] == "setrgb":
            await bulbSet.setRgb(bulbVariables.getAllVariablesFromRgbInput(cmd), bulbVariables.getVariable(splitCmd[1], True, True));
        if splitCmd[0] == "setbrightness":
            await bulbSet.setBrightness(bulbVariables.getVariable(splitCmd[1], True, True), bulbVariables.getVariable(splitCmd[2], True, True));
        if splitCmd[0] == "setscene":
            await bulbSet.setScene(bulbVariables.getVariable(splitCmd[1], True, True), bulbVariables.getVariable(splitCmd[2], True, True));
        if splitCmd[0] == "setwhite":
            await bulbSet.setWhite(splitCmd[2], bulbVariables.getVariable(splitCmd[3], True, True), bulbVariables.getVariable(splitCmd[1], True, True));
        if splitCmd[0] == "setoff":
            await bulbSet.setOff(bulbVariables.getVariable(splitCmd[1], True, True));
        if splitCmd[0] == "slp":
            await asyncio.sleep(float(splitCmd[1]));
        if splitCmd[0] == "var":
            varName = splitCmd[1]
            if len(splitCmd) > 2:
                varValue = cmd.split("=")[1]
                varValue = varValue.replace(" ", "")
            else: varValue = ""
            bulbVariables.addVariable(varName, varValue)
        if splitCmd[0] == "mov":
            bulbVariables.setVariable(splitCmd[1], splitCmd[2])
        if splitCmd[0] == "add":
            bulbVariables.addToVariable(splitCmd[1], splitCmd[2])
        if splitCmd[0] == "sub":
            bulbVariables.subFromVariable(splitCmd[1], splitCmd[2])
        if splitCmd[0] == "exec":
            bulbVariables.setVariable("returned", customFunctions.runCustomFunction(cmdUnchanged[5:]))
        if splitCmd[0] == "print":
            bulbVariables.formatAndPrint(cmd[6:])
        if splitCmd[0] == "rnd":
            rnd = random.randint(int(splitCmd[2]), int(splitCmd[3]))
            bulbVariables.setVariable(splitCmd[1], rnd)
        if splitCmd[0] == "stop":
            return "stop"
        if splitCmd[0] == "if":
            skip = not (bulbVariables.compareVariable(splitCmd[1], splitCmd[3], splitCmd[2]))     
    
async def parseCode(codeToParse, runOnce=False):
    loop = True
    lines = []
    for line in codeToParse:
        line = line.format(line.strip())
        line = line.rstrip()
        lines.append(line)
        
    if runOnce:
        for cmd in lines: 
            if (await parseCommand(cmd)) == "stop": return
        return
        
    while loop:
        for cmd in lines: 
            if (await parseCommand(cmd)) == "stop": loop = False; return
     
sys.path.append('/bulbScript_functions')
sys.path.append('/user_functions')
asyncio.run(initialize(open("bulbScript_scripts/" + config.loadedScript, "r")))
