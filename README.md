# BulbScript-for-Wiz-Lights
**setrgb *'all/index of light'* (R, G, B)** <br>
ex. 'setrgb all (255, 255, 255)' //Sets the rgb value of all lights to (255, 255, 255) <br>

**setbrightness *'all/index of light'* *'int 1-255'*** <br>
ex. 'setbrightness 1 50' //Sets the brightness value of the light at the index of 1 to 50 <br>

**setscene *'all/index of light'* *'int 1-255'*** <br>
ex. 'setscene all 4' //Sets the scene, supported scenes can be found [here](https://github.com/sbidy/pywizlight/blob/master/pywizlight/scenes.py) <br>

**setwhite *'all/index of light'* *warm/cold* *'int 1-255'*** <br>
ex. 'setwhite all warm 50' //Sets all lights to a warm white with a brightness value of 50 <br>
ex. 'setwhite all cold 255' //Sets all lights to a cold white with a brightness value of 255 <br>

**setoff *'all/index of light'*** <br>
ex. 'setoff all' //Turns all the lights off <br>

**slp *float*** <br>
ex. 'slp 0.5' //Waits for half a second before continuing <br>

**var *varName*** <br>
ex. 'var exampleIntVariable = 50' <br>
ex. 'var exampleFloatVariable = 5.5' <br>
ex. 'var exampleStringVariable = Hello World!' <br>

**mov *variable* *'variable/value'*** <br>
mov exampleIntVariable 50 //Sets the value of exampleIntVariable to 50 <br>
mov exampleIntVariable exampleFloatVariable //Sets the value of exampleIntVariable to the value of exampleFloatVariable <br>

**add *variable* *'variable/value'*** <br>
add exampleIntVariable 50 //Adds 50 to the value of exampleIntVariable <br>
add exampleIntVariable anotherIntVariable //Adds the value of anotherIntVariable to the value of exampleIntVariable <br>

**sub *variable* *'variable/value'*** //Same as add but for subtraction <br>

