# BulbScript-for-Wiz-Lights
**setrgb *'all/index of light'* (R, G, B)** <br>
ex. 'setrgb all (255, 255, 255)' //Sets the rgb value of all lights to (255, 255, 255) <br>

**setbrightness *'all/index of light'* 1-255** <br>
ex. 'setbrightness 1 50' //Sets the brightness value of the light at the index of 1 to 50 <br>

**setscene *'all/index of light'* *scene*** <br>
ex. 'setscene all 4' //Sets the scene, supported scenes can be found [here](https://github.com/sbidy/pywizlight/blob/master/pywizlight/scenes.py) <br>

**setwhite *'all/index of light'* *warm/cold* *brightness*** <br>
ex. 'setwhite all warm 50' //Sets all lights to a warm white with a brightness value of 50 <br>
ex. 'setwhite all cold 255' //Sets all lights to a cold white with a brightness value of 255 <br>
