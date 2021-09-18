from pywizlight import wizlight, PilotBuilder, discovery
from bulbScript_functions import bulbVariables, bulbSet

def runCustomFunction(func):
    variables = func[func.find("(")+1:func.find(")")]
    variables = variables.replace(" ", "")
    variables = variables.split(",")
    
    for i, variable in enumerate(variables):
        variables[i] = bulbVariables.getVariable(str(variable).lower(), True, True)
        
    addedVars = False
    func = func.split("(")[0]
    func += "("
    for x in variables:
        func += str(x).lower() + ", "
        addedVars = True
        
    if addedVars:
        func = func[:-2]
    func += ")"
    
    return(eval(func)) #Returns the value which will be assigned to the default variable "returned"

######ADD YOUR FUNCTIONS BELOW######

def exampleFunction(value): #See this function in use in the "Custom Function Example.bulb" script
   return value * 5
