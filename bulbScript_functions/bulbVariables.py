variables = [["returned", 0]] #List of variables, variables are stored in this list as ["VARIABLE NAME", VALUE]
#"returned" is a default variable used by custom Python functions

#Checks if variable exists
def doesVariableExist(varName):
    for variable in variables:
        if variable[0] == varName: return True
    return False

#Gets a variable by name, returns the variable name by default
def getVariable(varName, returnInput=False, returnValue=False):
    for index, variable in enumerate(variables):
        if variable[0] == varName:
            if returnValue: return variable[1]
            return variable, index
    if not returnInput: return None #I don't remember the purpose of this
    return varName

#Tries to get all variables from a BulbScript command
def getAllVariablesFromRgbInput(cmd):
    newValues = []
    values = cmd[cmd.find("(")+1:cmd.find(")")]
    values = values.replace(" ", "")
    values = values.replace("*", "")
    values = values.split(",")
    for value in values:
        if getVariable(value) != None:
            newValues.append(getVariable(value)[0][1])
        else: newValues.append(value)
    return newValues

#Adds a new variable to the variables list
def addVariable(varName, varValue):
    if doesVariableExist(varName): return
    try:
        varValue = int(varValue)
    except:
        1+1       
    variables.append([varName, varValue])
       
#Math functions
def setVariable(varName, newValue):
    varIndex = getVariable(varName)[1]  
    try:
        newValue = int(newValue)
    except:
        1+1  
    if getVariable(newValue) == None:
        variables[varIndex][1] = newValue
    else: variables[varIndex][1] = getVariable(newValue)[0][1]
  
#Math functions
#Addition
def addToVariable(varName, newValue):
    varType = "num"
    varIndex = getVariable(varName)[1]
    varValue = variables[varIndex][1]
    try:
        varValue = int(varValue)
    except:
        return; 
    if doesVariableExist(newValue):
        toAddIndex = getVariable(newValue)[1]
        variables[varIndex][1] = varValue + int(variables[toAddIndex][1])
        return       
    variables[varIndex][1] = varValue + int(newValue)
    
#Subtraction
def subFromVariable(varName, newValue):
    varType = "num"
    varIndex = getVariable(varName)[1]
    varValue = variables[varIndex][1]
    try:
        varValue = int(varValue)
    except:
        return; 
    if doesVariableExist(newValue):
        toAddIndex = getVariable(newValue)[1]
        variables[varIndex][1] = varValue - int(variables[toAddIndex][1])
        return       
    variables[varIndex][1] = varValue - int(newValue)
    
#Comparison operations
def compareVariable(varName, compareTo, operator):
    if getVariable(varName) == None: return   
    try:
        compareTo = int(compareTo)
    except:
        1+1 
    varValue = getVariable(varName)[0][1]
    if getVariable(compareTo) != None: compareTo = getVariable(compareTo)[0][1]
    if operator == "==": return varValue == compareTo
    if operator == ">=": return varValue >= compareTo
    if operator == "<=": return varValue <= compareTo
    if operator == ">": return varValue > compareTo
    if operator == "<": return varValue < compareTo
    if operator == "!=": return varValue != compareTo
    
    
#Printing
def formatAndPrint(toPrint):
    finalString = ""
    variableToAdd = ""
    recordVariable = False
    
    for x in toPrint: 
        if not recordVariable:
            if x == "*":
                recordVariable = True
            else: finalString += x
        else: 
            if x == "*": 
                recordVariable = False
                finalString += str(getVariable(variableToAdd)[0][1])
            else: variableToAdd += x;
                     
    print(finalString)
