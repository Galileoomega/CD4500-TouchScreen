##============================================================ 
##===        Visualise the touch of the CD4500 screen
##===                       
##===                         v1.1.9
##============================================================ 

import pygame, os, re, time
from importlib import reload

# INITIALISATION
pygame.init()
ecran = pygame.display.set_mode((1180, 700))
pygame.display.set_caption("Screen touch Visualiser v1.1.9")
pygame.scrap.init()

# -----------VAR-----------
# SETTING FPS
clock = pygame.time.Clock()
dt = clock.tick(60.0)

# LOOP VAR
run = clickOnMe = part1 = fingerPress = True
theresSomething = focus = iUsedCtrlV = iUsedCtrlA = iHaveMyFile = False
doesMyFileExist = True
iChangedMyPath = pathHasChanged = False
validState = moovingIsOk = False
iAmOnMultipleTouch = False
IfinishedToDraw = True
  # Button State
iPressedMyButton = iPressedMyStopButton = False
iPressedTotalButton = iPressedMySingleButton = False
iPressedPartialButton = iPressedMyMultiButton = True
iPressedMyScreenShotButton = False
  # Error State
singleButtonError = False
multiButtonError = False
justToCatchError = True


#COLOR VAR
red = (208, 14, 14)
black = (53, 50, 55)
blue = (34,138,164)
white = (255,255,255)
green = (14, 208, 14)
purple = (152, 3, 252)
orange = (252, 115, 3)
cyan = (3, 252, 240)

otherWhite = whiteVisualiser = myChangingColor = stopButtonColor = partialButtonColor = totalButtonColor = (220, 220, 220)
screenShotButtonColor = whiteVisualiser
singleColor = whiteVisualiser
multiColor = whiteVisualiser
customWhite = (180, 180, 180)
customBlack = (33,29,50)
  # Color of the background
whiteBackground = (250, 250, 250)

color0 = red
color1 = blue
color2 = green
color3 = purple
color4 = orange
color5 = cyan

lineColor = red

#POSITION VAR
pos = pos1 = 0, 0
xPathField = 800
yPathField = 20
xText = 150
xSpeedBar = 850
ySpeedBar = 440
  # Button Position
    # PARTIAL
xPartialButton = xSingleButton = 700
yPartialButton = 290
    # TOTAL
xTotalButton = xMultiButton = 900
yTotalButton = 290
    # Single
ySingleButton = 150
    # MULTI
yMultiButton = 150
    # CALCULATE
yButton = 620
xButton = 1000
    # STOP
xStopButton = 50
yStopButton = yButton
    # SCREENSHOT
xScreenShotButton = 20
yScreenShotButton = 530
    # OUTPUT CONSOLE
xOutput = 320
yOutput = 550

  # SIZE VAR
heightInput = 50
widthInput = 1000
posXInput = 90
posYInput = 290
yText = 300

#OTHER VAR
user_input_value = ""
path = ""
count3 = 5
myFileName = ""
makeAFor = 1

# MEDIA IMAGE
MANUAL_CURSOR = pygame.image.load('Resources\\cursor.png').convert_alpha()
RESIZE_CURSOR = pygame.image.load('Resources\\resizeCursor.png').convert_alpha()
blackBackground = pygame.image.load('Resources\\00.png').convert_alpha()
blackBackground = pygame.transform.scale(ecran, (1300,800))
greyCross = pygame.image.load('Resources\\cross.png').convert_alpha()
greyCross = pygame.transform.scale(greyCross, (80,80))
  # BACKGROUND INPUT BAR management
location = (0,0)
x = location[0]
y = location[1]
temp = pygame.Surface((blackBackground.get_width(), blackBackground.get_height())).convert()
temp.blit(ecran, (-x, -y))
temp.blit(blackBackground, (0, 0))
temp.set_alpha(100)

# PROGRAM VAR
loopData = countOf = myTempSpeed = 0
count = -1
releaseSeparator = 111111
oldPath = ""
myConsoleMessage = 'Console Output :'
howManyPress = "None"
max47Code = 0
perkCount = 0
firstTime = 0
numberOfFPS = 60
oldLoopData = 1
oldPerkCount = 0
errorMessage = "None"
  # LISTS
finalListOfData = pressList = ['']
stringOfCoordinatesOfLayer = []
myDunnoList = []
tempLists = []
myFinalList = []
coordinatesOfLayer = [int]
lenOfMyList = [0, 0, 0, 0, 0, 0]
coordinatesOfLayer.pop(0)
#-------------------------

#TEXT MANAGE
  #---Define font---
font = pygame.font.Font('Resources\\OpenSans-Light.ttf', 14)
waitFont = pygame.font.Font('Resources\\OpenSans-Light.ttf', 24)
secondFont = pygame.font.Font('Resources\\OpenSans-Light.ttf', 16)
font2 = pygame.font.Font('freesansbold.ttf', 32)
errorFont = pygame.font.Font('Resources\\OpenSans-Bold.ttf', 12)
consoleFont = pygame.font.Font('Resources\\Inconsolata\\Inconsolata-Regular.ttf', 14)
  #-----------------
  #---Define text---
lblFindEvtest = font.render(str("File EVTEST :"), True, black)
lblLoading = waitFont.render(str("WAIT..."), True, black)
lblFileError = errorFont.render(str("Error: Missing File"), True, red)

lblSingleError = errorFont.render(str("FILE TYPE : Should be Single-Touch mode"), True, red)
lblMultiError = errorFont.render(str("FILE TYPE : Should be Multi-Touch mode"), True, red)

lblFindPath = font.render(str("Search..."), True, black)
lblPlaySpeed = font.render(str("PLAY SPEED"), True, black)

lblScreenShotButton = font.render(str("Take ScreenShot"), True, black)

lblSimViewParameter = font.render(str("SIMULATION VIEW"), True, black)
lblSimViewParameterPartial = font.render(str("Partial"), True, black)
lblSimViewParameterTotal = font.render(str("Total"), True, black)

lblFileType = font.render("FILE TYPE", True, black)
lblFileTypeSingle = font.render("Single-Touch", True, black)
lblFileTypeMulti = font.render("Multi-Touch", True, black)

lblButton = secondFont.render("Calculate... ", True, black)
lblStopButton = secondFont.render("Stop... ", True, black)
user_input = font.render(user_input_value, True, red)

lblConsoleOutput = consoleFont.render(str(myConsoleMessage), True, black)
  #-----------------

rect = pygame.Rect(20, 20, 600, 500)
sub = ecran.subsurface(rect)

#-----------FUNCTION-------------

# GRAPHIC : Draw element on the screen
def drawVisualArea():
    # Visualiser Area
  pygame.draw.rect(ecran, whiteVisualiser, (20,20,600,500))

    # "Calculate" Button
  pygame.draw.rect(ecran, myChangingColor, (xButton, yButton, 140, 50))
  ecran.blit(lblButton, (xButton + 30, yButton + 10))

    # "Stop" Button
  pygame.draw.rect(ecran, stopButtonColor, (xStopButton, yStopButton, 140, 50))
  ecran.blit(lblStopButton, (xStopButton + 45, yStopButton + 10))


def console(myConsoleMessage, lblConsoleOutput, coordinateOfLayer, howManyPress, max47Code):

  # OUTPUT CONSOLE Area
  pygame.draw.rect(ecran, whiteVisualiser, (xOutput, yOutput, 550, 100))
  # MAIN LABEL
  ecran.blit(lblConsoleOutput, (xOutput, yOutput - 20))
  
  # LABEL1 (Mod touch)
  if iPressedMySingleButton:
      lblConsoleOutput1 = consoleFont.render("MOD : Single-Touch", True, black)
  else:
      lblConsoleOutput1 = consoleFont.render("MOD : Multi-Touch", True, black)
    
  # LABEL2 (there's an error ?)
  lblConsoleOutput2 = consoleFont.render("Error : " + errorMessage, True, black)

  # LABEL3 (Number of press)
  try:
    if howManyPress == None:
      howManyPress = "None"
  except UnboundLocalError:
    howManyPress = "None"
  
  if iPressedMyButton:
    if iPressedMySingleButton:
      stringOfCoordinatesOfLayer = []
      for u in coordinatesOfLayer:
        u = str(u)
        stringOfCoordinatesOfLayer.append(u)

      temp = '(?:% s)' % '|'.join(stringOfCoordinatesOfLayer) 
      array = re.findall(str(releaseSeparator), temp)
      howManyPress = len(array)
    else:
      stringOfmyFinalList = []
      for u in myFinalList:
        u = str(u)
        stringOfmyFinalList.append(u)

      temp = '(?:% s)' % '|'.join(stringOfmyFinalList) 
      array = re.findall(str(releaseSeparator), temp)
      howManyPress = len(array)

  lblConsoleOutput3 = consoleFont.render("Number Of Press : " + str(howManyPress), True, black)

  # LABEL4 (Max Finger)
  if iPressedMyButton:
    if max47Code == 0:
      max47Code = 1
  
  lblConsoleOutput4 = consoleFont.render("Number Of Fingers : " + str(max47Code), True, black)

  # LABEL5 (actual finger)
  if iAmOnMultipleTouch:
    if not(iPressedTotalButton):
      if myFinalList == []:
        label5Message = "None"
      else:
        label5Message = str(perkCount)
        if perkCount == 0:
          label5Message += " Red"
        elif perkCount == 1:
          label5Message += " Red"
        elif perkCount == 2:
          label5Message += " Blue"
        elif perkCount == 3:
          label5Message += " Green"
        elif perkCount == 4:
          label5Message += " Purple"
        elif perkCount == 5:
          label5Message += " Orange"
        else:
          label5Message += " Cyan"
    else:
      label5Message = "All"
  else:
    label5Message = "1"
  lblConsoleOutput5 = consoleFont.render("Actual Finger : " + str(label5Message), True, black)

  ecran.blit(lblConsoleOutput1, (xOutput + 5, yOutput))
  ecran.blit(lblConsoleOutput2, (xOutput + 210, yOutput))
  ecran.blit(lblConsoleOutput3, (xOutput + 20, yOutput + 32))
  ecran.blit(lblConsoleOutput4, (xOutput + 20, yOutput + 47))
  ecran.blit(lblConsoleOutput5, (xOutput + 20, yOutput + 62))
  return myConsoleMessage, howManyPress


# GRAPHIC : Show user key press and the path field
def drawPathArea(user_input, xText, yText):
  pygame.draw.rect(ecran, whiteVisualiser, (xPathField,yPathField,210,23))

  xText, yText, user_input = replaceText(user_input, user_input_value)
  
  if not(clickOnMe):
    pygame.draw.rect(ecran, customBlack, (posXInput,posYInput,widthInput,heightInput))

    #BLIT BLACK BACKGROUND
    ecran.blit(temp, (0,0))
  return xText, yText, user_input


# GRAPHIC : BACKGROUND COLOR
def setBackgroundColor():
  ecran.fill(whiteBackground)


# GRAPHIC
def mouseOnFocus():
    if mousePos[0] > xPathField:
      if mousePos[1] < 40:
        if mousePos[0] > 1010:
          clickOnMe = True
          focus = False
          pygame.mouse.set_visible(True)
        else:
          if pygame.mouse.get_pressed() == (1,0,0):
            clickOnMe = False
            focus = True
            pygame.mouse.set_visible(False)
          else:
            clickOnMe = True
            focus = False
      else:
        pygame.mouse.set_visible(True)
        clickOnMe = True
        focus = False
    else:
      pygame.mouse.set_visible(True)
      clickOnMe = True
      focus = False
    return clickOnMe, focus


def unFocusFilePath(focus):
    if not(clickOnMe):
      if pygame.mouse.get_pressed() == (1,0,0):
          if mousePos[0] > posXInput + widthInput:
            if mousePos[0] > 1010:
              focus = iUsedCtrlA = False
          elif mousePos[0] < posXInput:
            if mousePos[0] < xPathField:
              focus = iUsedCtrlA = False
          elif mousePos[1] > posYInput + heightInput:
            if mousePos[1] > 40:
              focus = iUsedCtrlA = False
          elif mousePos[1] < posYInput:
            if mousePos[1] < 15:
              focus = iUsedCtrlA = False
            if mousePos[1] > 50:
              focus = iUsedCtrlA = False
    else:
      if focus == True:
        if pygame.mouse.get_pressed() == (1,0,0):
          if mousePos[0] > 1010:
            focus = False
            iUsedCtrlA = False
          elif mousePos[0] < xPathField:
            focus = False
            iUsedCtrlA = False
          elif mousePos[1] > 40:
            focus = False
            iUsedCtrlA = False
          elif mousePos[1] < 15:
            focus = False
            iUsedCtrlA = False
    return focus


def unFocusCtrlA(iUsedCtrlA, user_input):
  if iUsedCtrlA == True:

    if pygame.mouse.get_pressed() == (1,0,0):
      if mousePos[0] > 1010:
        iUsedCtrlA = False
        user_input = font.render(user_input_value, True, black)
      elif mousePos[0] < xPathField:
        iUsedCtrlA = False
        user_input = font.render(user_input_value, True, black)
      elif mousePos[1] > 40:
        iUsedCtrlA = False
        user_input = font.render(user_input_value, True, black)
      elif mousePos[1] < 15:
        iUsedCtrlA = False
        user_input = font.render(user_input_value, True, black)
  return iUsedCtrlA, user_input


# PROGRAM : Will take the text of the clipboard
def getContentOfClipboard():
  try:
    clipboard = pygame.scrap.get(pygame.SCRAP_TEXT)
    try:
      clipboard = clipboard.decode("utf-8")
    except UnicodeDecodeError:
      clipboard = ''
  except AttributeError:
    pass
  try:
    clipboard = clipboard[:-1]
  except TypeError:
    pass
  
  try:
    if len(clipboard) > 400:
      clipboard = ""
      print("Error : Invalid Clipoard")
  except TypeError:
    pass 

  return clipboard


# PROGRAM : Will Put Text In The Clipboard
def textInsertInClipboard():
  pygame.scrap.put()


# GRAPHIC : Detect a CTRL + V or C
def keyboardCommandDetection(user_input_value):
  if event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
      user_input_value += str(clipboard)
      iUsedCtrlV = True
  else:
      iUsedCtrlV = False
  return iUsedCtrlV, user_input_value


# GRAPHIC : Detect a CTRL + A
def selectAllText(user_input_value):
  if event.key == pygame.K_a and pygame.key.get_mods() & pygame.KMOD_CTRL:
    iUsedCtrlA = True
  else:
    iUsedCtrlA = False
    user_input_value = user_input_value
  return iUsedCtrlA, user_input_value


# GRAPHIC : Replace cursor design.
def changeMyMouseLook():
  if moovingIsOk:
    ecran.blit(RESIZE_CURSOR, (xMouse - 8, yMouse)) 
  if not(clickOnMe):
    ecran.blit(MANUAL_CURSOR, (pygame.mouse.get_pos())) 
  if not(theresSomething):
    if clickOnMe:
      ecran.blit(lblFindPath, (805, 20))


# GRAPHIC : Change Simulation Option (PARTIAL to TOTAL)
def visualizeSimViewArea():
  #TITLE
  ecran.blit(lblSimViewParameter, (700, 250))

  #PARTIAL
    #Background
  pygame.draw.rect(ecran, partialButtonColor, (xPartialButton, yPartialButton, 170, 40))
    #Label
  ecran.blit(lblSimViewParameterPartial, (760, 300))

  #TOTAL
    #Background
  pygame.draw.rect(ecran, totalButtonColor, (xTotalButton, yTotalButton, 170, 40))
    #Label
  ecran.blit(lblSimViewParameterTotal, (960, 300))


# GRAPHIC : Take A SCreenShot
def screenShotArea():
    #Background
  pygame.draw.rect(ecran, screenShotButtonColor, (xScreenShotButton, yScreenShotButton, 170, 40))
    #Label
  ecran.blit(lblScreenShotButton, (xScreenShotButton + 28, yScreenShotButton + 9))


# GRAPHIC : Change File Type (SINGLE to MULTI)
def visualizeFileTypeArea():
  #TITLE
  ecran.blit(lblFileType, (700, 110))
  # SINGLE
    #Background
  pygame.draw.rect(ecran, singleColor, (xPartialButton, ySingleButton, 170, 40))
    #Label
  ecran.blit(lblFileTypeSingle, (745, ySingleButton + 8))
  # MULTI
    #Background
  pygame.draw.rect(ecran, multiColor, (xTotalButton, yMultiButton, 170, 40))
    #Label
  ecran.blit(lblFileTypeMulti, (945, yMultiButton + 8))

# PROGRAM : A function which allows to detect click on a BUTTON
def buttonClickMaster(font, xButton, yButton, buttonColor, pressedMainButton, labelButton, pressedButtonNeighbour, labelString):
    imOnFly = False

    if clickOnMe:
      if mousePos[0] > xButton:
        if mousePos[0] < xButton + 170:
          if mousePos[1] > yButton:
            if mousePos[1] < yButton + 40:
              buttonColor = customWhite
              imOnFly = True

      if pygame.mouse.get_pressed() == (1,0,0):
        if mousePos[0] > xButton:
          if mousePos[0] < xButton + 170:
            if mousePos[1] > yButton:
              if mousePos[1] < yButton + 40:
                pressedMainButton = True
                pressedButtonNeighbour = False

    if pressedMainButton:
      buttonColor = black
      labelButton = font.render(str(labelString), True, white)

    if not(imOnFly):
      if not(pressedMainButton):
        labelButton = font.render(str(labelString), True, black)
        buttonColor = otherWhite

    return xButton, yButton, buttonColor, pressedMainButton, labelButton, pressedButtonNeighbour

# GRAPHIC : Show UI Element for the speed controller
def numberOfFPSArea():
  ecran.blit(lblPlaySpeed, (700, 400))
  ecran.blit(lblNumberOfFps, (1000, 400))
  #INPUT BAR CONTROLLING
  pygame.draw.rect(ecran, whiteVisualiser, (700, 350 + 100, 400, 7))
  pygame.draw.rect(ecran, black, (xSpeedBar, ySpeedBar, 9, 30))

  #NUMBER OF FPS
  
# CONTROLLER : Bound the UI bar with the nulber of fps
def moovingBarSpeed(xSpeedBar, moovingIsOk, myTempSpeed):
    if pygame.mouse.get_pressed() == (0,0,0):
      moovingIsOk = False

    if clickOnMe:
      if pygame.mouse.get_pressed() == (1,0,0):
          if mousePos[0] > xSpeedBar - 3:
            if mousePos[0] < xSpeedBar + 9:
              if mousePos[1] > ySpeedBar:
                if mousePos[1] < ySpeedBar + 30:
                  moovingIsOk = True
    
    try:    
      if moovingIsOk:
        xSpeedBar = mousePos[0] 
        pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
      else:
        pygame.mouse.set_cursor((16, 16), (0, 0), (0, 0, 64, 0, 96, 0, 112, 0, 120, 0, 124, 0, 126, 0, 127, 0, 127, 128, 124, 0, 108, 0, 70, 0, 6, 0, 3, 0, 3, 0, 0, 0),
          (192, 0, 224, 0, 240, 0, 248, 0, 252, 0, 254, 0, 255, 0, 255, 128, 255, 192, 255, 224, 254, 0, 239, 0, 207, 0, 135, 128, 7, 128, 3, 0))
    except UnboundLocalError:
      pass
    
    if xSpeedBar < 700:
      xSpeedBar = 700
    if xSpeedBar > 1100:
      xSpeedBar = 1100

    myTempSpeed = (xSpeedBar / 2) - 330

    return xSpeedBar, moovingIsOk, myTempSpeed


# GRAPHIC : Put a default label if nothing has been wrote 
def itIsEmpty():
  if len(user_input_value) != 0:
    theresSomething = True
  else:
    theresSomething = False
  return theresSomething


# Change his placement when press on search
def replaceText(user_input, user_input_value):
  if clickOnMe:
    xText = 800
    yText = 20
    user_input = font.render(user_input_value, True, black)
  else:
    xText = posXInput + 11
    yText = posYInput + 15
    theresSomething = itIsEmpty()
    if not(theresSomething):
      user_input_value = "Place path..."
    user_input = secondFont.render(user_input_value, True, white)
  return xText, yText, user_input


# PROGRAM: Will look if the user changed the path
def pathChecker(path, iChangedMyPath, oldPath, firstTime):
  
  if oldPath != path:
    if firstTime != 0:
      iChangedMyPath = True
    firstTime += 1
    #oldPath = path
  else:
    oldPath = path
    iChangedMyPath = False
  
  return path, iChangedMyPath, oldPath, firstTime


# Detect If User Click On Button "Stop..."
def clickStopButtonDetect(stopButtonColor, iPressedMyStopButton, lblStopButton):
  if clickOnMe:
    if pygame.mouse.get_pressed() == (1,0,0):
        if mousePos[0] > xStopButton:
          if mousePos[0] < xStopButton + 140:
            if mousePos[1] > yStopButton:
              if mousePos[1] < yStopButton + 50:
                stopButtonColor = black
                lblStopButton = secondFont.render("Stop... ", True, white)
                iPressedMyStopButton = True
                
    else:
      stopButtonColor = (220,220,220)
      lblStopButton = secondFont.render("Stop... ", True, black)
  else:
    stopButtonColor = (220,220,220)
    lblStopButton = secondFont.render("stop... ", True, black)

    
  return stopButtonColor, iPressedMyStopButton, lblStopButton


def fileOpenning(part1, finalListOfData, count, doesMyFileExist, loopData, perkCount, tempLists):
  code47List = []

  # Try to open the file, if it cannot an error is show
  try:
    myFile = open(path, "r")
    doesMyFileExist = True
    errorMessage = "None"
    try:
      fileContent = myFile.read()
      errorMessage = "None"
    except UnicodeDecodeError:
      doesMyFileExist = False
      errorMessage = "Invalid Format"
  except OSError:
    errorMessage = "Unable to find the file"
    doesMyFileExist = False
    max47Code = 0
    iAmOnMultipleTouch = False

  if doesMyFileExist:
    
    #---------------REG-EX PART---------------

    #Find X Data
      #Delete useless data
    tempPressEvent = re.sub("\(ABS_MT_TRACKING_ID\)..", "", fileContent)
    tempPressEvent = re.sub("\(ABS_MT_.............", "", tempPressEvent)
    tempPressEvent = re.sub("Event code.*", "", tempPressEvent)
      #Find relevant data

    pressList = re.findall("code 57.*|code 53.*|code 54.*|code 47.*", tempPressEvent)

    finalListOfData = []
    
    for u in pressList:
      u = re.sub("code | value| alue", "", u)
      finalListOfData += re.split("\s", u)
    index = -1

    #finalListOfData.pop(0)
    for u in range(0, len(finalListOfData)):
      index += 2
      try:
        try:
          finalListOfData[index] = int(finalListOfData[index])
        except ValueError:
          finalListOfData.pop(index)
      except IndexError:
        pass

    # Detect how many finger have been pressed together.
    for u in range(0, len(finalListOfData)):
      if finalListOfData[u] == "47":
        code47List.append(finalListOfData[u + 1])
    try:
      max47Code = max(code47List) + 1
    except ValueError:
      max47Code = 0

    # WIPING LIST WITH FILE
    if max47Code > 1:
      #if not(pathHasChanged):    

        if finalListOfData[0] != "47":
          finalListOfData.insert(0, "47")
          finalListOfData.insert(1, 0)

        myFinalList = []
        tempLists = []

        open('appender.py', 'w').close()
        open('writecontroller.py', 'w').close()

        #perkCount = 0 

        fWriteController = open("writecontroller.py", "w+")
        fWhereToDraw = open("whereToDraw.py", "a+")
      
        # BUILD THE FIRST FILE (appender.py)
        with open("appender.py", "w+") as fAppender:
          fAppender.write("def addData():\n")
          for u in range(0, max47Code):
            fAppender.write("\tmyList" + str(u) + " = []\n")  
          for u in range(0, len(finalListOfData)):
            if finalListOfData[count] == "47":
              count += 2
              number = finalListOfData[count - 1]
              try:
                while finalListOfData[count] != "47":
                  fAppender.write("\tmyList" + str(number) + ".append(" + str(finalListOfData[count]) + ")\n")
                  count += 1  
              except IndexError:
                break     
            else:
              count += 1
          fAppender.write("\treturn myList0") 
          for u in range(1, max47Code):
            fAppender.write(", myList" + str(u))

        #BUILD THE SECOND FILE (writecontroller.py)
        fWriteController.write("from importlib import reload\n")
        fWriteController.write("def giveList(index):\n")
        fWriteController.write("\timport appender\n" + "\tmyLists = []" + "\n")
        fWriteController.write("\tappender = reload(appender)\n")
        
        fWriteController.write("\tmyLists = appender.addData()" + "\n")
        fWriteController.write("\treturn myLists[index]")

        fWriteController.close()

        tempLists = []
        with open("writecontroller.py", "r") as file:
          import writecontroller
          for u in range(0, max47Code):
            writecontroller = reload(writecontroller)
            data = writecontroller.giveList(u)
            tempLists.append(data)
          del writecontroller
        iAmOnMultipleTouch = True
    else:
      iAmOnMultipleTouch = False
      max47Code = 1

    #-----------------------------------------
  
  return finalListOfData, doesMyFileExist, max47Code, tempLists, iAmOnMultipleTouch, perkCount, errorMessage


# PROGRAM : A whereToDrawLine() but for MULTIPLE TOUCH 
def writingMultipleLines(lenOfMyList, perkCount, max47Code, tempLists, validState, justToCatchError, myDunnoList, iPressedMyButton, myFinalList, oldLoopData, oldPerkCount):
  import whereToDraw

  if iPressedPartialButton:
    if perkCount == max47Code:
      perkCount = 0
      oldLoopData = 0
      oldPerkCount = 0
      resetList = True
    else:
      resetList = False
  else:
    resetList = False
  
  if iPressedMyButton:
    perkCount = 0
    oldLoopData = 0
    oldPerkCount = 0
    resetList = True


  if iPressedMyButton:
    if iPressedPartialButton:
      if perkCount == max47Code:
          myFinalList = []
  if iPressedMySingleButton:
    tempLists = []
    perkCount = 0
  
  for u in range(perkCount, max47Code):
    try:
        myFinalList = whereToDraw.lineBuild(tempLists[u], myFinalList, iPressedTotalButton, resetList)
        lenOfMyList[0] = len(whereToDraw.lineBuild(tempLists[0], myFinalList, iPressedTotalButton, True))
        lenOfMyList[1] = len(whereToDraw.lineBuild(tempLists[1], myFinalList, iPressedTotalButton, True))
        lenOfMyList[1] += lenOfMyList[0]
        try:
          lenOfMyList[2] = len(whereToDraw.lineBuild(tempLists[2], myFinalList, iPressedTotalButton, True))
          lenOfMyList[2] += lenOfMyList[1]
        except IndexError:
          pass
        try:
          lenOfMyList[3] = len(whereToDraw.lineBuild(tempLists[3], myFinalList, iPressedTotalButton, True))
          lenOfMyList[3] += lenOfMyList[2]
        except IndexError:
          pass
        try:
          lenOfMyList[4] = len(whereToDraw.lineBuild(tempLists[4], myFinalList, iPressedTotalButton, True))
          lenOfMyList[4] += lenOfMyList[3]
        except IndexError:
          pass
        try:
          lenOfMyList[5] = len(whereToDraw.lineBuild(tempLists[5], myFinalList, iPressedTotalButton, True))
          lenOfMyList[5] += lenOfMyList[4]
        except IndexError:
          pass
    except IndexError:
      pass

    except UnboundLocalError:
      myDunnoList = []
      myFinalList = whereToDraw.lineBuild(tempLists[u], myDunnoList, iPressedTotalButton)
    perkCount += 1
    justToCatchError = False
    break
  
  if justToCatchError:
    myFinalList = []
  else:
    pass

  del whereToDraw

  return lenOfMyList, perkCount, myFinalList, justToCatchError, myDunnoList, tempLists, oldLoopData, oldPerkCount


# PROGRAM Prepare a list of coordinate for making simulation lines
def whereToDrawLine(finalListOfData, coordinatesOfLayer):


  firstPassOfX = firstPassOfY = True
  iHaveMyNextDataX = iHaveMyNextDataY = False
  press = yAdded = xAdded = False

  lineX = lineY = count = 0
  nextLineX = nextLineY = -1  

  for u in range(count, len(finalListOfData)):
    needToExit = False
    # Detect if Press or Release.
    try:
      # If its a press or a release
      if finalListOfData[count] == "57":
        count +=1
        if xAdded:
          if not(yAdded):
            coordinatesOfLayer.append(nextLineY * 2)

        xAdded = yAdded = False

        if not(firstPassOfX):
          if not(firstPassOfY):
            if nextLineX == lineX:
              if nextLineY == lineY:
                coordinatesOfLayer.append(lineX * 2)
                coordinatesOfLayer.append(lineY * 2)

        lineY = 0
        iHaveMyNextDataX = iHaveMyNextDataY = False  

        # Press
        if finalListOfData[count] >= 0:
          press = True
          count += 1
        # Release
        else:
          firstPassOfX = firstPassOfY = True
          press = False
          coordinatesOfLayer.append(releaseSeparator)
      
    except IndexError:
      break

    if xAdded:
      if yAdded:
        xAdded = yAdded = False
        firstPassOfX = firstPassOfY = False
    
    lineY = 0
    lineX = 0

    if press == True:
        # If its a X position
        if finalListOfData[count] == "53":
          count += 1

          if iHaveMyNextDataX:
            if not(yAdded):
              if xAdded:
                coordinatesOfLayer.append(nextLineY * 2)
                yAdded = True
                needToExit = True
                count -= 2

          xAdded = True
          if not(needToExit):
            if firstPassOfX:
              lineX = finalListOfData[count]
              nextLineX = lineX
              coordinatesOfLayer.append(lineX * 2)
              firstPassOfX = False
            else:
              nextLineX = finalListOfData[count]
              if xAdded:
                coordinatesOfLayer.append(nextLineX * 2)
              iHaveMyNextDataX = True
        else:
          if lineX != 0:
            coordinatesOfLayer.append(lineX * 2)
            xAdded = True
        

        # If its a Y position
        if finalListOfData[count] == "54":
          count += 1

          if not(xAdded):
              coordinatesOfLayer.append(nextLineX * 2)
              xAdded = True

          yAdded = True

          if firstPassOfY:
            lineY = finalListOfData[count]
            nextLineY = lineY
            coordinatesOfLayer.append(lineY * 2)
            firstPassOfY = False
          else:
            nextLineY = finalListOfData[count]
            coordinatesOfLayer.append(nextLineY * 2)
            iHaveMyNextDataY = True
        else:
          if lineY != 0:
            coordinatesOfLayer.append(lineY * 2)
            yAdded = True


        if not(iHaveMyNextDataY):
          if not(iHaveMyNextDataX):
            try:     
              pass       
              lineX = nextLineX
              lineY = nextLineY
            except UnboundLocalError:
              pass
    else:
      pass
    count += 1

  return coordinatesOfLayer


# GRAPHIC : Draw simulation line 
def drawLine(coordinatesOfLayer, validState, loopData, makeAFor, IfinishedToDraw, oldLoopData, oldPerkCount):
    IfinishedToDraw = False
    lineColor = red
    # Watch if we have to make a for-loop or just one pass (TOTAL/PARTIAL) 
    if iPressedTotalButton:
      makeAFor = len(coordinatesOfLayer)
      makeAFor = int(makeAFor)
    else:
      makeAFor += 1
      loopData = 0

    if iAmOnMultipleTouch:
      if iPressedPartialButton:
        if oldPerkCount != perkCount:
          makeAFor = oldLoopData

    for u in range(0, makeAFor):

      #----------COLOR CHOOSER PART---------
      if iAmOnMultipleTouch:
        try:
          if loopData < lenOfMyList[0]:
            lineColor = color0
        except IndexError:
          pass
        try:
          if loopData > lenOfMyList[0]:
            if loopData < lenOfMyList[1]:
              lineColor = color1
        except IndexError:
          pass
        try:
          if loopData > lenOfMyList[1]:
            if loopData < lenOfMyList[2]:
              lineColor = color2
        except IndexError:
          pass
        try:
          if loopData > lenOfMyList[2]:
            if loopData < lenOfMyList[3]:
              lineColor = color3
        except IndexError:
          pass
        try:
          if loopData > lenOfMyList[0]:
            if loopData < lenOfMyList[1]:
              lineColor = color4
        except IndexError:
          pass
        try:
          if loopData > lenOfMyList[0]:
            if loopData < lenOfMyList[1]:
              lineColor = color1
        except IndexError:
          pass
      else:
        lineColor = color0
      #--------------------------------------

      #print(len(coordinatesOfLayer), "++++" , makeAFor)
      firstPass = True
      try:
        lala = coordinatesOfLayer[loopData + 3]
        validState = True
      except IndexError:
        oldLoopData = makeAFor
        loopData = 0
        makeAFor = 0
        validState = False
        IfinishedToDraw = True

      if validState:
        try:
          if coordinatesOfLayer[loopData + 4] == releaseSeparator:
            if firstPass:
              firstPass = False
            else:
              loopData += 3
          try:
            lala = coordinatesOfLayer[loopData + 3]
          except IndexError:
            oldLoopData = makeAFor
            loopData = 0
            makeAFor = 0
            IfinishedToDraw = True
        except IndexError:
          oldLoopData = makeAFor
          loopData = 0
          makeAFor = 0
          IfinishedToDraw = True

        startx = coordinatesOfLayer[loopData]
        starty = coordinatesOfLayer[loopData + 1]
        endx = coordinatesOfLayer[loopData + 2]
        endy = coordinatesOfLayer[loopData + 3]

        try:
          if coordinatesOfLayer[loopData + 4] == releaseSeparator:
            loopData += 3
        except IndexError:
          oldLoopData = makeAFor
          loopData = 0
          makeAFor = 0
          IfinishedToDraw = True

        # BUILDER
        # Condition is just to change the width of the line
        if iPressedPartialButton:
          pygame.draw.line(ecran, lineColor, (startx, starty), (endx, endy), 5)
        else:
          pygame.draw.line(ecran, lineColor, (startx, starty), (endx, endy), 4)

        loopData += 2
    
    if not(iPressedTotalButton):
      if makeAFor >= (len(coordinatesOfLayer)):
        oldLoopData = makeAFor
        makeAFor = 0
        loopData = 0
        IfinishedToDraw = True

      if loopData >= (len(coordinatesOfLayer)):
        oldLoopData = makeAFor
        makeAFor = 0
        loopData = 0
        IfinishedToDraw = True
    else:
      IfinishedToDraw = True

    oldPerkCount = perkCount
    return loopData, makeAFor, IfinishedToDraw, oldLoopData, oldPerkCount
#--------------------------------


#-----------------------------------------START LOOP--------------------------------------------
while run:

  # NEED To reset the FPS Label
  lblNumberOfFps = font.render(str(myTempSpeed), True, black)

  # Getting mouse position
  mousePos = pygame.mouse.get_pos()
  xMouse, yMouse = pygame.mouse.get_pos()

  # Set the FPS
  clock.tick(numberOfFPS)

  # Get what you have in your clipboard
  clipboard = getContentOfClipboard()

  # Know If the user is into the dark field (Path Input)
  focus = unFocusFilePath(focus)

  if iUsedCtrlA:
    iUsedCtrlA, user_input = unFocusCtrlA(iUsedCtrlA, user_input)

  # WAIT TO QUIT 
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

    # KEYBOARD INTERACTION
    elif not(clickOnMe):
      if event.type == pygame.KEYDOWN:

        # Detect if user press CTRL + V
        iUsedCtrlV, user_input_value = keyboardCommandDetection(user_input_value)        

        # Delete element if Backspace is pressed
        if event.key == pygame.K_BACKSPACE:
            user_input_value = user_input_value[:-1]
            if iUsedCtrlA:
              user_input_value = ""
            
        else:
            if not(iUsedCtrlV):
              user_input_value += event.unicode

        #Detect if user press CTRL + A
        iUsedCtrlA, user_input_value = selectAllText(user_input_value)

        try:
            user_input = font.render(user_input_value, True, black)
        except pygame.error as message:
            user_input = ""

        if iUsedCtrlA:
          if event.key == pygame.K_BACKSPACE:
            user_input_value = ""
          user_input_value = user_input_value[:-1]
        else:
          user_input = font.render(user_input_value, True, black)

  theresSomething = itIsEmpty()

  #Detect when mouse is on a text field
  if focus == False:
    clickOnMe, focus = mouseOnFocus()
  
  if iPressedMyButton:

    path = user_input_value
    # Put double Backslash for searching the file
    path = re.sub("[\"]", "", path)

    # ------ GET THE NAME OF THE FILE ------
    while not(iHaveMyFile):
      try:
        for u in path[-count3]:
          if u == "\\":
            iHaveMyFile = True
            break

          myFileName += u
          count3 += 1
      except IndexError:
        pass
        iHaveMyFile = True
    try:
      for i in myFileName[-1]:
        finalFileName = myFileName[::-1]
    except IndexError:
      pass
    # ------------------------------------

    # PATH MANAGEMENT (Check if its a new and wait for reset coordinateOfLayer)
    if len(coordinatesOfLayer) > 1:
      path, iChangedMyPath, oldPath, firstTime = pathChecker(path, iChangedMyPath, oldPath, firstTime)
    if iChangedMyPath:
      if not(singleButtonError):
        print(singleButtonError)
        coordinatesOfLayer = []
        myFinalList = []
        oldPath = path
        pathHasChanged = True
        myFileName = ""
        iHaveMyFile = False
    else:
      pathHasChanged = False

    finalListOfData, doesMyFileExist, max47Code, tempLists, iAmOnMultipleTouch, perkCount, errorMessage = fileOpenning(part1, finalListOfData, count, doesMyFileExist, loopData, perkCount, tempLists)
    
    if iPressedMyMultiButton:
      if max47Code == 0:
        iPressedMyButton = False
        iPressedMyStopButton = True
        #finalListOfData = []
        tempLists = []
        perkCount = 0
    if iPressedMySingleButton:
      if max47Code > 1:
        iPressedMyButton = False
        iPressedMyStopButton = True
        #finalListOfData = []
        tempLists = []
        perkCount = 0    

    if doesMyFileExist:
      #perkCount = 0
      if not(iAmOnMultipleTouch):
        if not(multiButtonError):
          #if path != oldPath:
            coordinatesOfLayer = []
            oldPath = path
            coordinatesOfLayer = whereToDrawLine(finalListOfData, coordinatesOfLayer)
      iPressedMyButton = False
  
  if iPressedMyMultiButton:
      iAmOnMultipleTouch = True
      if max47Code == 0:
        iPressedMyButton = False
        iPressedMyStopButton = True
        iAmOnMultipleTouch = False
  else:
      iAmOnMultipleTouch = False

  # ---------- BUTTONS CHECK ----------  
  labelString = "Calculate..."
  xButton, yButton, myChangingColor, iPressedMyButton, lblButton, iPressedMyStopButton = buttonClickMaster(secondFont, xButton, yButton, myChangingColor, iPressedMyButton, lblButton, iPressedMyStopButton, labelString)

  stopButtonColor, iPressedMyStopButton, lblStopButton = clickStopButtonDetect(stopButtonColor, iPressedMyStopButton, lblStopButton)

    # PARTIAL Button Detect
  labelString = "Partial"
  xPartialButton, yPartialButton, partialButtonColor, iPressedPartialButton, lblSimViewParameterPartial, iPressedTotalButton = buttonClickMaster(font, xPartialButton, yPartialButton, partialButtonColor, iPressedPartialButton, lblSimViewParameterPartial, iPressedTotalButton, labelString)
  
    # TOTAL Button Detect
  labelString = "Total"
  xTotalButton, yTotalButton, totalButtonColor, iPressedTotalButton, lblSimViewParameterTotal, iPressedPartialButton = buttonClickMaster(font, xTotalButton, yTotalButton, totalButtonColor, iPressedTotalButton, lblSimViewParameterTotal, iPressedPartialButton, labelString)
  
    # MULTI Button detect
  labelString = "Multi-Touch"
  xMultiButton, yMultiButton, multiColor, iPressedMyMultiButton, lblFileTypeMulti, iPressedMySingleButton = buttonClickMaster(font, xMultiButton, yMultiButton, multiColor, iPressedMyMultiButton, lblFileTypeMulti, iPressedMySingleButton, labelString)
  
    # SINGLE Button detect
  labelString = "Single-Touch"
  xSingleButton, ySingleButton, singleColor, iPressedMySingleButton, lblFileTypeSingle, iPressedMyMultiButton = buttonClickMaster(font, xSingleButton, ySingleButton, singleColor, iPressedMySingleButton, lblFileTypeSingle, iPressedMyMultiButton, labelString)

    # SCREENSHOT Button detect
  labelString = "Take ScreenShot"
  xScreenShotButton, yScreenShotButton, screenShotButtonColor, iPressedMyScreenShotButton, lblScreenShotButton, iPressedMyStopButton = buttonClickMaster(font, xScreenShotButton, yScreenShotButton, screenShotButtonColor, iPressedMyScreenShotButton, lblScreenShotButton, iPressedMyStopButton, labelString)
  # -----------------------------------


  # SAVE A SCREENSHOT
  try:
    if iPressedMyScreenShotButton:
      if iPressedPartialButton:
        pygame.image.save(sub, "ScreenShots\\" + finalFileName + "-partial.jpg")
        iPressedMyScreenShotButton = False
      if iPressedTotalButton:
        pygame.image.save(sub, "ScreenShots\\" + finalFileName + "-total.jpg")
        iPressedMyScreenShotButton = False
  except NameError:
    print("Can't take a screenshot: No file ")
    iPressedMyScreenShotButton = False
  
  # VISUAL AND CONSTANT STUFF
  setBackgroundColor()
  drawVisualArea()
  myConsoleMessage, howManyPress = console(myConsoleMessage, lblConsoleOutput, coordinatesOfLayer, howManyPress, max47Code)

  # FPS MANAGEMENT
  if iPressedPartialButton:
    numberOfFPSArea()
    xSpeedBar, moovingIsOk, myTempSpeed = moovingBarSpeed(xSpeedBar, moovingIsOk, myTempSpeed)
    if not(focus):
      numberOfFPS = myTempSpeed
    else:
      numberOfFPS = 60
  else:
    numberOfFPS = 60

  # UI Component (Total/Partial)
  visualizeSimViewArea()
  # UI Component (SINGLE/MULTI)
  visualizeFileTypeArea()
  # UI Component (SCREENSHOT)
  screenShotArea()
  if iAmOnMultipleTouch:
    if IfinishedToDraw:
      try:
        lenOfMyList, perkCount, myFinalList, justToCatchError, myDunnoList, tempLists, oldLoopData, oldPerkCount = writingMultipleLines(lenOfMyList, perkCount, max47Code, tempLists, validState, justToCatchError, myDunnoList, iPressedMyButton, myFinalList, oldLoopData, oldPerkCount)
      except UnboundLocalError:
        # local variable "myFinalList" referenced before assignement
        pass

  if not(iPressedMyStopButton):  
    if iAmOnMultipleTouch == False:
      loopData, makeAFor, IfinishedToDraw, oldLoopData, oldPerkCount = drawLine(coordinatesOfLayer, validState, loopData, makeAFor, IfinishedToDraw, oldLoopData, oldPerkCount)
    else:
      loopData, makeAFor, IfinishedToDraw, oldLoopData, oldPerkCount = drawLine(myFinalList, validState, loopData, makeAFor, IfinishedToDraw, oldLoopData, oldPerkCount)

  if iPressedMyStopButton:
    tempLists = []
    myFinalList = []
    open('appender.py', 'w').close()
    open('writecontroller.py', 'w').close()

  # Draw a label "EV Test :"
  ecran.blit(lblFindEvtest, (700, 20))

  # ---------------- ERROR MANAGEMENT ------------------
  if not(doesMyFileExist):
    multiButtonError = False
    singleButtonError = False
    # Show ERROR Label
    ecran.blit(lblFileError, (xPathField, yPathField + 25))
    # Show grey Cross Image
    ecran.blit(greyCross, (250, 220))

  if iPressedMyButton:
    if iPressedMyMultiButton:
        if max47Code == 0:
          singleButtonError = True
          oldPath = "lala"
        else:
          singleButtonError = False
    else:
      singleButtonError = False

    if iPressedMySingleButton:
        if max47Code > 1:
          multiButtonError = True
        else:
          multiButtonError = False
    else:
      multiButtonError = False

  if singleButtonError:
    ecran.blit(lblSingleError, (xPathField, yPathField + 25))
    errorMessage = "FILE TYPE : Should be Single-Touch mode"
  if multiButtonError:
    ecran.blit(lblMultiError, (xPathField, yPathField + 25))
    errorMessage = "FILE TYPE : Should be Multi-Touch mode"
  #--------------------------------------------------------

  
  # Draw the PATH AREA and the letter input
  xText, yText, user_input = drawPathArea(user_input, xText, yText)

  # Write what the user is typping
  if iUsedCtrlA:
    user_input = secondFont.render(user_input_value, True, black, blue)
  ecran.blit(user_input, (xText, yText))

  if clickOnMe:
    # Hide if the text is going too far
    pygame.draw.rect(ecran, whiteBackground, (1010,20,200,23))

  if iPressedMyButton:
    
    if doesMyFileExist:
      # Show a wait label
      ecran.blit(lblLoading, (300,300))

  # Call mouse Manager
  changeMyMouseLook()  

  pygame.display.update() 

pygame.quit()