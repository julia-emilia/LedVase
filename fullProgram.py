from machine import Pin, Timer
from neopixel import NeoPixel
from array import array
from time import sleep_ms

led = Pin(25, Pin.OUT)
timer = Timer()
timer2 = Timer()
## Hardware
# GPIO-Pin für WS2812
pin_np = 28
# Anzahl der LEDs
NumOfLeds = 93
#Abstand der LEDs
distLeds = 60/100 #Led pro cm
# Helligkeit: 0 bis 255
brightness = 10
# Aktualisierung
frameRate = 30 #Hz



#Colors
ColorBlack = (0,0,0)
ColorRed = [brightness,0,0]
ColorYellow = [brightness//2,brightness//2,0]
ColorGreen = [0,brightness,0]
ColorCyan = [0,brightness//2,brightness//2]
ColorBlue = [0,0,brightness]
ColorMagenta = [brightness//2,0,brightness//2]
ColorWarmWhite = [brightness,brightness-1,brightness-9]
ColorWhite = [brightness,brightness-1,brightness-9]
#Global frames
InitFrame = [ColorWarmWhite]*NumOfLeds
#Global variables
programCounter = 0
frontLedIdx = 0
frontPosition = 0.0
finished = 0
timeCounter = 0.0


def dimLed(rgb,factor):
     # Multiply all elements by 2
    result = [int(x * factor) for x in rgb]
    return result
def dimLedAbs(rgb,Add):
     # Multiply all elements by 2
    for x in range(len(rgb)):
        if rgb[x]+Add >=0:
            rgb[x] = rgb[x]+Add
    
    return rgb

def PercToRgb(red,green,blue):
    result = [int(brightness*red),int(brightness*green),int(brightness*blue)]
    return result
def dimAll(frame,factor):
    for k in range(len(frame)):
        frame[k] = dimLed(frame[k],factor)
    return frame

    
whitePattern =[ColorWarmWhite]*NumOfLeds
#currentFrame = [ColorRed,dim(ColorRed,0.5),ColorRed,ColorRed,ColorRed,ColorRed,ColorRed,ColorRed]
redPattern = [ColorRed]*NumOfLeds
for k in range(NumOfLeds):
    redPattern[k] = dimLed(ColorRed,1/(k+1))

rainbowPattern = [ColorWhite]*NumOfLeds
for m in range(NumOfLeds//2):
    rainbowPattern[m] = PercToRgb(1-m/NumOfLeds,m/NumOfLeds,0)
    rainbowPattern[NumOfLeds//2+m] = PercToRgb(0,1-m/NumOfLeds,m/NumOfLeds)
currentPattern = rainbowPattern

ringStarts = [0,11,22,34,46,58,70,82]
ringLength = 11
def dimRing(frame,ringIdx,factor):
    for k in range(ringLength):
        m = ringStarts[ringIdx]+k
        frame[m] = dimLed(frame[m],factor)
def dimRingAbs(frame,ringIdx,Add):
    for k in range(ringLength):
        m = ringStarts[ringIdx]+k
        frame[m] = dimLedAbs(frame[m],Add)        

ringRainbowPattern = [ColorBlack]*ringLength
ringRainbowPattern[0] = ColorRed
ringRainbowPattern[1] = ColorRed
ringRainbowPattern[2]=  ColorYellow
ringRainbowPattern[3] = ColorYellow
ringRainbowPattern[4] = ColorGreen
ringRainbowPattern[5] = ColorGreen
ringRainbowPattern[6] = ColorBlue
ringRainbowPattern[7] = ColorBlue
ringRainbowPattern[8] = ColorCyan
ringRainbowPattern[9] = ColorMagenta
ringRainbowPattern[10] = ColorMagenta

# Initialisierung WS2812/NeoPixel
np = NeoPixel(Pin(pin_np, Pin.OUT), NumOfLeds)
currentFrame = InitFrame
for k in range(NumOfLeds):
    np[k] = InitFrame[k]
    np.write()
    
sleep_ms(1000)
#np = dimAll(InitFrame,0.5)


def blinkOnboard(timer2):
    led.toggle()

def allOff(frame):
    for led in range(NumOfLeds):
        frame[led] = ColorBlack
    return frame
def posToIdx(position):
    Idx = position/distLeds
    return int(Idx)

def runFrameIn(frame,velocity,pattern):
    global frontLedIdx
    global frontPosition
    finished = 0
    if posToIdx(frontPosition) >= NumOfLeds:
        frontLedIdx = 0
        frontPosition = 0.0
        frame = allOff(frame)
        finished = 1
    else:
        frontLedIdx = posToIdx(frontPosition)
        for k in range(frontLedIdx+1):
            if frontLedIdx-k>=0:
                frame[frontLedIdx-k] = pattern[k]
        #np[frontLedIdx] = currentFrame[0]
        frontLedIdx+=1
        frontPosition+=velocity/frameRate
    return finished
    
def showPattern(frame,holdTime,pattern):
    global timeCounter
    finished = 0
    for k in range(NumOfLeds):
        frame[k] = pattern[NumOfLeds-k-1]
    timeCounter = timeCounter + 1/frameRate
    if timeCounter >= holdTime:
        finished = 1
        timeCounter = 0.0
    return finished
def runFrameOut(frame,velocity,pattern):
    global frontLedIdx
    global frontPosition
    finished = 0
    if posToIdx(frontPosition) >= NumOfLeds:
        frontLedIdx = 0
        frontPosition = 0.0
        frame = allOff(frame)
        finished = 1
    else:
        frontLedIdx = posToIdx(frontPosition) #Maximum of frontLedIdx: NumOfLeds-1
        for k in range(frontLedIdx+1):
            if frontLedIdx-k>=0:
                frame[frontLedIdx-k] = ColorBlack
        for k in range(NumOfLeds-frontLedIdx):
                frame[frontLedIdx+k] = pattern[NumOfLeds-1-k]
        #np[frontLedIdx] = currentFrame[0]
        frontLedIdx+=1
        frontPosition+=velocity/frameRate
    return finished

  
def fadeout(frame):
    finished = 0
    frame = dimAll(frame,0.99)
    if frame[0] == [0,0,0]:
        finished = 1
    return finished
def ringStacking(frame,stepTime,ringPattern):
    global ringStarts
    global ringLength
    global frontLedIdx
    global timeCounter
    for m in range(ringLength):
        k = ringStarts[len(ringStarts)-1-frontLedIdx]+m
        frame[NumOfLeds-k-1] = ringRainbowPattern[m]
    finished = 0
    timeCounter = timeCounter + 1/frameRate
    if timeCounter >= stepTime:
        timeCounter = 0.0
        frontLedIdx += 1
    if frontLedIdx >= len(ringStarts):
        finished = 1
        frontLedIdx = 0
    return finished
def ringSpinning(frame,stepTime,ringPattern):
    global ringStarts
    global ringLength
    global frontLedIdx
    global timeCounter
    for r in range(len(ringStarts)):
        for m in range(ringLength):
            k = ringStarts[len(ringStarts)-1-r]+m
            if NumOfLeds-1-k >=0:
                if m+frontLedIdx < len(ringPattern):
                    frame[NumOfLeds-1-k] = ringPattern[m+frontLedIdx]
                else:
                    frame[NumOfLeds-1-k] = ringPattern[m+frontLedIdx-len(ringPattern)]
        #for n in range(frontLedIdx):
            #h = ringStarts[len(ringStarts)-1-r]+n
            #if NumOfLeds-h-1 >=0:
                #frame[NumOfLeds-h-1] = ringRainbowPattern[n]
    finished = 0
    timeCounter = timeCounter + 1/frameRate
    if timeCounter >= stepTime:
        timeCounter = 0.0
        frontLedIdx += 1
    if frontLedIdx >= ringLength:
        finished = 1
        timeCounter = 0.0
        frontLedIdx = 0
    return finished
def glistening(frame,stepTime):
    global timeCounter
    finished = 0
    timeCounter = timeCounter + 1/frameRate
    if timeCounter >= stepTime/2:
        if timeCounter < stepTime/2 +1/frameRate:
            dimRingAbs(currentFrame,1,-1)
            dimRingAbs(currentFrame,2,1)
            dimRingAbs(currentFrame,3,1)
            dimRingAbs(currentFrame,4,1)
            dimRingAbs(currentFrame,5,1)
            dimRingAbs(currentFrame,6,-1)
            dimRingAbs(currentFrame,7,1)
    if timeCounter >= stepTime:
        timeCounter = 0.0
        dimRingAbs(currentFrame,1,1)
        dimRingAbs(currentFrame,2,-1)
        dimRingAbs(currentFrame,3,-1)
        dimRingAbs(currentFrame,4,-1)
        dimRingAbs(currentFrame,5,-1)
        dimRingAbs(currentFrame,6,1)
        dimRingAbs(currentFrame,7,-1)
    return finished
    
def periodicFunction(timer):
        global currentFrame
        #Program of lightshow
        global programCounter
        global finished
        global timeCounter

        if programCounter == 0:
            if fadeout(currentFrame):
                programCounter +=1
        if programCounter == 1:
            if runFrameIn(currentFrame,50,redPattern):
                programCounter +=1
        if programCounter == 2:
            if runFrameOut(currentFrame,50,redPattern):
                programCounter += 1
        if programCounter == 3:
            if runFrameIn(currentFrame,20,rainbowPattern):
                programCounter +=1
                #timeCounter = 0.0
        if programCounter == 4:   
            if showPattern(currentFrame,5.0,rainbowPattern):
                programCounter+=1
        if programCounter == 5:
            if runFrameOut(currentFrame,20,rainbowPattern):
                programCounter += 1
        if programCounter == 6:
            if ringStacking(currentFrame,1.0,ringRainbowPattern):
                programCounter +=1
                timeCounter = 0.0
        if programCounter == 7:   
            if ringSpinning(currentFrame,1.0,ringRainbowPattern):
                programCounter+=1
        if programCounter == 8:
            if fadeout(currentFrame):
                programCounter +=1
        if programCounter == 9:
            if showPattern(currentFrame,1.0,whitePattern):
                programCounter +=1
        if programCounter == 10:
            if finished == 0:
                dimRing(currentFrame,1,0.9)
                dimRing(currentFrame,2,0.6)
                dimRing(currentFrame,3,0.3)
                dimRing(currentFrame,4,0.2)
                dimRing(currentFrame,5,0.2)
                dimRing(currentFrame,6,0.15)
                dimRing(currentFrame,7,0.15)
                finished = 1
            programCounter +=0
        #Send to hardware
        for k in range(NumOfLeds):
            np[k] = currentFrame[k]
        np.write()
    
    


timer.init(freq=frameRate, mode=Timer.PERIODIC, callback=periodicFunction)
timer2.init(freq=1, mode=Timer.PERIODIC, callback=blinkOnboard)