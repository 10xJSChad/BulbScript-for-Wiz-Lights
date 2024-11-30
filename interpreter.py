import asyncio
import sys
import config
import random
from bulbScript_functions import bulbSet, bulbVariables, bulbFunctions
from user_functions import customFunctions

funcName = ""
funcCode = []
recordCode = False
skip = 0

async def initialize(script):
    await bulbSet.initialize(config.broadcastSpace)
    await parseCode(script)
    
async def parseCommand(cmd):
    global funcName, funcCode, recordCode, skip
    
    cmd = cmd.lstrip()
    cmdUnchanged = cmd
    
    cmd = cmd.split("//")[0] # removes the comment if there is one
    cmd = cmd.lower() # lowercase for simpler parsing
    splitCmd = cmd.split(" ")
    

    # keeps track of the current "if statement" depth
    # this is necessary for nested conditionals to work properly
    # the old solution for if statements was to just skip to the next 'end if'
    # but that would often result in jumping to the end of a child condition
    # despite the parent condition being evaluated to false

    if splitCmd[0] == "if" and skip > 0:
        skip += 1 
    if splitCmd[0] == "end" and splitCmd[1] == "if" and skip > 0:
        skip -= 1 
        
    if skip > 0: return


    # if a function is declared, capture all the code until the next 'end func'
    # nested function definitions are not supported.
    if recordCode: funcCode.append(cmd)

    if splitCmd[0] == "func":
        funcName = splitCmd[1]
        recordCode = True

    if splitCmd[0] == "end" and splitCmd[1] == "func":
        funcCode.pop(-1) # remove the "end func" from the function code

        # adds a function entry with the name and captured code
        bulbFunctions.addFunction(funcName, funcCode)

        funcCode = [] 
        recordCode = False

    # function calls
    # checks for a function call and executes the function if once is present
    # if the function call does not specify how many times to execute the function, 
    # then the function is executed only once.

    if splitCmd[0] == "call":
        bulbFunction = bulbFunctions.getFunction(splitCmd[1])[1]
        if len(splitCmd) == 3 and splitCmd[2] != "":
            for _ in range(int(splitCmd[2])):
                await parseCode(bulbFunction, True)
            return        
        await parseCode(bulbFunction, True)
        
    if not recordCode:
        # this should have been a dictionary

        if splitCmd[0] == "setrgb":
            await bulbSet.setRgb(bulbVariables.getAllVariablesFromRgbInput(cmd), 
                                 bulbVariables.getVariable(splitCmd[1], True, True))
            
        if splitCmd[0] == "setbrightness":
            await bulbSet.setBrightness(bulbVariables.getVariable(splitCmd[1], True, True), 
                                        bulbVariables.getVariable(splitCmd[2], True, True))
            
        if splitCmd[0] == "setscene":
            await bulbSet.setScene(bulbVariables.getVariable(splitCmd[1], True, True), 
                                   bulbVariables.getVariable(splitCmd[2], True, True))
            
        if splitCmd[0] == "setwhite":
            await bulbSet.setWhite(splitCmd[2], 
                                   bulbVariables.getVariable(splitCmd[3], True, True), 
                                   bulbVariables.getVariable(splitCmd[1], True, True))
        
        if splitCmd[0] == "setoff":
            await bulbSet.setOff(bulbVariables.getVariable(splitCmd[1], True, True))

        if splitCmd[0] == "slp":
            await asyncio.sleep(float(splitCmd[1]))

        if splitCmd[0] == "var":
            varName = splitCmd[1]
            if len(splitCmd) > 2:
                varValue = cmd.split("=")[1]
                varValue = varValue.replace(" ", "")
            else: varValue = ""
            bulbVariables.addVariable(varName, varValue)

        if splitCmd[0] == "mov" or splitCmd[0] == "set":
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
            if not (bulbVariables.compareVariable(splitCmd[1], splitCmd[3], splitCmd[2])): skip += 1 
    
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

script_name = "DefaultScript.bulb" if len(sys.argv) == 1 else sys.argv[1]
asyncio.run(initialize(open("bulbScript_scripts/" + script_name, "r")))