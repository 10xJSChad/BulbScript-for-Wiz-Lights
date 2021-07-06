import asyncio
import time
import threading
import config
import os
from pywizlight import wizlight, PilotBuilder, discovery
bulbs = []

async def initialize(broadcastSpace): 
    unsortedIPs = []
    
    #Add all bulbs to an unsorted list
    bulbsUnsorted = await discovery.discover_lights(broadcast_space=broadcastSpace)
    
    #Sorts all the bulbs alphabetically and appends them to a new list
    for x in bulbsUnsorted:
        unsortedIPs.append(x.ip)
        
    unsortedIPs = sorted(unsortedIPs)
    
    for x in unsortedIPs:
        for y in bulbsUnsorted:
            if x == y.ip: bulbs.append(y)
        
async def changeColor(bulbIndex, color):
    if bulbIndex == "all":
        for bulb in bulbs:
            await bulb.turn_on(PilotBuilder(rgb = (color)))
    else:
        await bulbs[int(bulbIndex)-1].turn_on(PilotBuilder(rgb = (color)))
        
async def setBrightness(bulbIndex, newBrightness): 
    newBrightness = int(newBrightness)
    if bulbIndex == "all":
        for bulb in bulbs:
            await bulb.turn_on(PilotBuilder(brightness = newBrightness))
    else:
        await bulbs[int(bulbIndex)-1].turn_on(PilotBuilder(brightness = newBrightness))      
     
async def setScene(bulbIndex, scene): 
    scene = int(scene)
    if bulbIndex == "all":
        for bulb in bulbs:
            await bulb.turn_on(PilotBuilder(scene = scene))
    else:
        await bulbs[int(bulbIndex)-1].turn_on(PilotBuilder(scene = scene))
                  
async def setOff(bulbIndex):
    if bulbIndex == "all":
        for bulb in bulbs:
            await bulb.turn_off()
    else:
        await bulbs[int(bulbIndex)-1].turn_off()
        
async def setWhite(value, brightness, bulbIndex):
    brightness = int(brightness)
    newColor = PilotBuilder(cold_white = 255) #Defaults to cold white
    if value == "cold": newColor = PilotBuilder(cold_white = brightness)
    if value == "warm": newColor = PilotBuilder(warm_white = brightness)
    if bulbIndex == "all":
        for bulb in bulbs:
            await bulb.turn_on(newColor)
    else:
        await bulbs[int(bulbIndex)-1].turn_on(newColor)
                             
async def setRgb(value, bulbIndex):
    await changeColor(bulbIndex, (int(value[0]),int(value[1]),int(value[2])))