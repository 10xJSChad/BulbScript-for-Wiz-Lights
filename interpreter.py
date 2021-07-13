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

def stripSpaces(cmd):
    return(cmd.lstrip())

async def initialize(script):
    await bulbSet.initialize(config.broadcastSpace)
    await parseCode(script)
    
async def parseCommand(cmd):
    cmd = stripSpaces(cmd)
    print(cmd)
    global funcName, funcCode, recordCode, skip
    cmdUnchanged = cmd
    cmd = cmd.split("//")[0]   
    cmd = cmd.lower()
    splitCmd = cmd.split(" ")
    if splitCmd[0] == "end" and splitCmd[1] == "if" and skip == True:
        skip = False 
    if skip: return
    if recordCode: funcCode.append(cmd)    
    if splitCmd[0] == "func":
        funcName = splitCmd[1]
        recordCode = True                           
    if splitCmd[0] == "end" and splitCmd[1] == "func":
        funcCode.pop(-1)
        bulbFunctions.addFunction(funcName, funcCode)
        funcCode = []
        recordCode = False
    if splitCmd[0] == "call":
        bulbFunction = bulbFunctions.getFunction(splitCmd[1])[1]    
        if len(splitCmd) == 3 and splitCmd[2] != "":
            for i in range(0, int(splitCmd[2])):
                await parseCode(bulbFunction, True)  
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