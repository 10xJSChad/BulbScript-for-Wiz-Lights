# BulbScript for Wiz Lights

BulbScript is a simple scripting language used to control Philips Wiz Lightbulbs using the [pywizlight](https://github.com/sbidy/pywizlight) library. <br>
BulbScript can be used to *very quickly* create intricate lightbulb sequences with the help of functions, variables, and conditional statements, all without having to write any Python code. However, BulbScript also supports executing and getting returned values from custom Python functions, for those who are looking to create more advanced light sequences and routines.

<img src="https://user-images.githubusercontent.com/48174610/124525483-bf406700-ddff-11eb-8f87-406c2870df9e.gif" width="400" height="250"/>
This script and several other example scripts can be found in /BulbScript_scripts


<h3>Dependencies</h3>

• [pywizlight](https://github.com/sbidy/pywizlight)

<h2>Using BulbScript</h2>
1. Configure your broadcast space in config.py. (Default: "192.168.1.255") <br>
2. Run interpreter.py, this will execute the default BulbCode.bulb script. If your lights start slowly turning off and on, your broadcast space is set correctly. <br>
3. Create your own BulbScript script! Simply navigate to the /bulbScript_scripts directory and create a new .bulb file. Then open it in your favorite text editor and start coding! Make sure to read the documentation below and check out the other example script in the /bulbScript_scripts directory if you're struggling.<br>
4. Set the "loadedScript" variable in config.py to your new bulb script, and run interpreter.py. If everything is configured correctly, your script will be successfully executed. The script will infinitely loop until it hits a "stop" command. <br>

<h2>BulbScript Commands/Functions</h2>

**setrgb *'all/index of light'* (R, G, B)** <br>
```
setrgb all (255, 255, 255) //Sets the rgb value of all lights to (255, 255, 255) <br>
```

**setbrightness *'all/index of light'* *'int 1-255'*** <br>
```
setbrightness 1 50 //Sets the brightness value of the light at the index of 1 to 50 <br>
```

**setscene *'all/index of light'* *'int 1-255'*** <br>
```
setscene all 4 //Sets the scene on all lights to 4
```
Supported scenes can be found [here](https://github.com/sbidy/pywizlight/blob/master/pywizlight/scenes.py) <br>

**setwhite *'all/index of light'* *warm/cold* *'int 1-255'*** <br>
```
setwhite all warm 50 //Sets all lights to a warm white with a brightness value of 50 <br>
setwhite all cold 255 //Sets all lights to a cold white with a brightness value of 255 <br>
```

**setoff *'all/index of light'*** <br>
```
setoff all //Turns all the lights off <br>
```

**slp *float*** <br>
```
slp 0.5 //Waits for half a second before continuing <br>
```

**var *varName*** <br>
```
var exampleIntVariable = 50
var exampleFloatVariable = 5.5
var exampleStringVariable = Hello World!
```

**mov *variable* *'variable/value'*** <br>
```
mov exampleIntVariable 50 //Sets the value of exampleIntVariable to 50 
mov exampleIntVariable exampleFloatVariable //Sets the value of exampleIntVariable to the value of exampleFloatVariable 
```

**add *variable* *'variable/value'*** <br>
```
add exampleIntVariable 50 //Adds 50 to the value of exampleIntVariable
add exampleIntVariable anotherIntVariable //Adds the value of anotherIntVariable to the value of exampleIntVariable
```

**sub *variable* *'variable/value'*** //Same as add but for subtraction <br>

**exec *functionName()*** //Executes a Python function from /user_functions/customFunctions.py <br<
//Note: The default BulbScript variable 'returned' will be set to whatever the custom function returns

**print** //Prints out whatever comes after it <br>
```
print Hello World! //Prints out "Hello World!"
print The value of X is *X* //Prints out "The value of X is " followed by the value of the variable 'X'
```

**rnd *variable* *int* *int*** <br>
```
rnd exampleIntVariable 0 500 //Sets the value of exampleIntVariable to a random number between 0 and 500
```

**if** and **end if** //Starts and ends an If Statement <br>
*Supported operators:* ==, >=, <=, >, <, !=
```
if x == 255 //Checks if x is equal to 255
mov y x //Sets the value of y to the value of x (255)
mov x 0  //Sets x to 0
end if //Ends the if statement
```
**func**, **end func**, and **call** //Starts, ends, and calls a function <br>

```
func lightsOff
setoff all
end func

call lightsOff //calls lightsOff once, 'call lightsOff 2' would call it twice.
```

**stop**  //Stops the script so it will not loop indefinitely 
