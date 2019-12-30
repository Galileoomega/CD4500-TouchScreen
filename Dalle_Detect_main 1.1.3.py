##============================================================ 
##===        Visualise the touch of the CD4500 screen
##===                       
##===                         v1.1.3
##============================================================ 

import pygame, os, re, time
#os.chdir("C:\\Users\\alimacher\\Desktop\\Work\\1ere annee\\Python\\PyGame\\Dalle_Detect")
##os.chdir("C:\\Users\\alexi\\Desktop\\GIT\\CD4500-TouchScreen-1")
del os

#INITIALISATION
pygame.init()
ecran = pygame.display.set_mode((1180, 700))
pygame.display.set_caption("Screen touch Visualiser")
pygame.scrap.init()


#-----------VAR-----------
#SETTING FPS
clock = pygame.time.Clock()
dt = clock.tick(60)

#LOOP VAR
run = clickOnMe = part1 = fingerPress = True
theresSomething = focus = iUsedCtrlV = iUsedCtrlA = iPressedMyButton = iPressedMyStopButton = False
doesMyFileExist = True
validState = False

#COLOR VAR
red = (208, 14, 14)
black = (0, 0, 0)
blue = (34,138,164)
white = (255,255,255)
customBlack = (33,29,50)
whiteBackground = (245, 245, 245)
whiteVisualiser = (220, 220, 220)
myChangingColor = stopButtonColor = whiteVisualiser

#POSITION VAR
pos = pos1 = 0, 0
xPathField = 800
yPathField = 20
heightInput = 50
widthInput = 860
posXInput = 180
posYInput = yText = 300
xButton = 1000
loopData = countOf = 0
yButton = 620
xText = 150
xStopButton = 50
yStopButton = yButton

#OTHER VAR
user_input_value = ""
path = ""
  # Cursor look
MANUAL_CURSOR = pygame.image.load('Resources\\cursor.png').convert_alpha()
blackBackground = pygame.image.load('Resources\\00.png').convert_alpha()
blackBackground = pygame.transform.scale(ecran, (1300,800))

location = (0,0)
x = location[0]
y = location[1]
temp = pygame.Surface((blackBackground.get_width(), blackBackground.get_height())).convert()
temp.blit(ecran, (-x, -y))
temp.blit(blackBackground, (0, 0))
temp.set_alpha(100)

count = -1
finalListOfData = pressList = ['']
coordinatesOfLayer = [int]
coordinatesOfLayer.pop(0)
releaseSeparator = 111111
oldPath = ""

numberOfFPS = 60

#-------------------------

#TEXT MANAGE
  #---Define font---
font = pygame.font.Font('Resources\\OpenSans-Light.ttf', 14)
waitFont = pygame.font.Font('Resources\\OpenSans-Light.ttf', 24)
secondFont = pygame.font.Font('Resources\\OpenSans-Light.ttf', 16)
font2 = pygame.font.Font('freesansbold.ttf', 32)
errorFont = pygame.font.Font('Resources\\OpenSans-Bold.ttf', 14)
  #-----------------
  #---Define text---
lblFindEvtest = font.render(str("File EVTEST :"), True, black)
lblLoading = waitFont.render(str("Wait..."), True, black)
lblFileError = errorFont.render(str("Error: Missing File"), True, red)
lblFindPath = font.render(str("Search..."), True, black)
lblButton = secondFont.render("Calculate... ", True, black)
lblStopButton = secondFont.render("Stop... ", True, black)
user_input = font.render(user_input_value, True, red)
  #-----------------

#-----------FUNCTION-------------

# GRAPHIC : Draw element on the screen
def drawVisualArea():
  
    # Visualiser Area
  pygame.draw.rect(ecran, whiteVisualiser, (20,20,600,500))

    # "Calculate" Button
  pygame.draw.rect(ecran, myChangingColor, (xButton, yButton, 140, 50))
  ecran.blit(lblButton, (xButton + 30, yButton + 10))

    #"Stop" Button
  pygame.draw.rect(ecran, stopButtonColor, (xStopButton, yStopButton, 140, 50))
  ecran.blit(lblStopButton, (xStopButton + 45, yStopButton + 10))

# GRAPHIC : Print user key press and the path field
def drawPathArea(user_input, xText, yText):
  pygame.draw.rect(ecran, whiteVisualiser, (xPathField,yPathField,210,23))

  xText, yText, user_input = replaceText(user_input, user_input_value)
  
  if not(clickOnMe):
    pygame.draw.rect(ecran, customBlack, (posXInput,posYInput,widthInput,heightInput))

    #BLIT BLACK BACKGROUND
    ecran.blit(temp, (0,0))
  return xText, yText, user_input

# GRAPHIC
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

# GRAPHIC : Will take the text of the clipboard
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
  return clipboard

# GRAPHIC : Will Put Text In The Clipboard
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
  if not(clickOnMe):
    ecran.blit(MANUAL_CURSOR, ( pygame.mouse.get_pos() ) ) 
  if not(theresSomething):
    if clickOnMe:
      ecran.blit(lblFindPath, (805, 20))

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


# MAYBE TO DELETE ???? AND HIS CHILD
def pathChecker(path):
  oldPath = path
  return path

# Detect If User Click On Button "Calculate..."
def clickButtonDetect(myChangingColor, iPressedMyButton, lblButton, iPressedMyStopButton, pathChecker, path):
  if clickOnMe:
    if pygame.mouse.get_pressed() == (1,0,0):
        if mousePos[0] > xButton:
          if mousePos[0] < xButton + 140:
            if mousePos[1] > yButton:
              if mousePos[1] < yButton + 50:
                myChangingColor = black
                lblButton = secondFont.render("Calculate... ", True, white)
                iPressedMyButton = True
                iPressedMyStopButton = False

                pathChecker(path)

    else:
      myChangingColor = (220,220,220)
      iPressedMyButton = False
      lblButton = secondFont.render("Calculate... ", True, black)
  else:
    myChangingColor = (220,220,220)
    iPressedMyButton = False
    lblButton = secondFont.render("Calculate... ", True, black)

    
  return myChangingColor, iPressedMyButton, lblButton, iPressedMyStopButton, pathChecker

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


def fileOpenning(part1, finalListOfData, count, doesMyFileExist):
  try:
    myFile = open(path, "r")
    doesMyFileExist = True
    try:
      fileContent = myFile.read()
    except UnicodeDecodeError:
      doesMyFileExist = False
      print("Error... Invalid Format")
  except OSError:
    print("Error... Unable to find the file")
    doesMyFileExist = False

  if doesMyFileExist:
    
    #---------------REG-EX PART---------------

    #Find X Data
      #Delete useless data
    tempPressEvent = re.sub("\(ABS_MT_..............", "", fileContent)
    tempPressEvent = re.sub("Event code.*", "", tempPressEvent)
      #Find relevant data

    pressList = re.findall("code 57.*|code 53.*|code 54.*", tempPressEvent)

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

    #-----------------------------------------
  return finalListOfData, doesMyFileExist

def dataOfCoordinatesSorting(finalListOfData):
  count = 0
  for u in range(0, len(finalListOfData)):
    #Detect if Press or Release.
    try:
      if finalListOfData[count] == "57":
        count += 1
        if finalListOfData[count] >= 0:
          fingerPress = True
          print("Press")
        else:
          fingerPress = False
          print("Released")
    except IndexError:
      fingerPress = False
      break

    try:
      if fingerPress:
        count += 1
        if finalListOfData[count] == '53':
          print("Pos X : ",finalListOfData[count + 1])
          count += 1
        if finalListOfData[count] == '54':
          print("Pos Y : ", finalListOfData[count + 1])
          count += 1
      else:
        count += 1
    except UnboundLocalError:
      break

# PROGRAM Prepare a list of coordinate for making simulation lines
def whereToDrawLine(finalListOfData, coordinatesOfLayer):

  press = yAdded = xAdded = False
  firstPassOfX = firstPassOfY = True
  iHaveMyNextDataX = iHaveMyNextDataY = False

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
            coordinatesOfLayer.append(nextLineY)
            
        xAdded = yAdded = False

        if not(firstPassOfX):
          if not(firstPassOfY):
            if nextLineX == lineX:
              if nextLineY == lineY:
                coordinatesOfLayer.append(lineX)
                coordinatesOfLayer.append(lineY)

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
                coordinatesOfLayer.append(nextLineY)
                yAdded = True
                needToExit = True
                count -= 2

          xAdded = True
          if not(needToExit):
            if firstPassOfX:
              lineX = finalListOfData[count]
              nextLineX = lineX
              coordinatesOfLayer.append(lineX)
              firstPassOfX = False
            else:
              nextLineX = finalListOfData[count]
              if xAdded:
                coordinatesOfLayer.append(nextLineX)
              iHaveMyNextDataX = True
        else:
          if lineX != 0:
            coordinatesOfLayer.append(lineX)
            xAdded = True
        

        # If its a Y position
        if finalListOfData[count] == "54":
          count += 1

          if not(xAdded):
              coordinatesOfLayer.append(nextLineX)
              xAdded = True

          yAdded = True

          if firstPassOfY:
            lineY = finalListOfData[count]
            nextLineY = lineY
            coordinatesOfLayer.append(lineY)
            firstPassOfY = False
          else:
            nextLineY = finalListOfData[count]
            coordinatesOfLayer.append(nextLineY)
            iHaveMyNextDataY = True
        else:
          if lineY != 0:
            coordinatesOfLayer.append(lineY)
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

  print(coordinatesOfLayer)
  return coordinatesOfLayer

# Graphic Draw simulation line 
def drawLine(coordinatesOfLayer, validState, loopData):
  firstPass = True
  try:
    lala = coordinatesOfLayer[loopData + 3]
    validState = True
  except IndexError:
    loopData = 0
    validState = False

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
        loopData = 0
    except IndexError:
      loopData = 0

    startx = coordinatesOfLayer[loopData]
    starty = coordinatesOfLayer[loopData + 1]
    endx = coordinatesOfLayer[loopData + 2]
    endy = coordinatesOfLayer[loopData + 3]
    try:
      if coordinatesOfLayer[loopData + 4] == releaseSeparator:
        loopData += 3
    except IndexError:
      loopData = 0

    pygame.draw.line(ecran, red, (startx, starty), (endx, endy), 4)

    loopData += 2

  return loopData

#--------------------------------

while run:

  clock.tick(numberOfFPS)
  mousePos = pygame.mouse.get_pos()

  # Get what you have in your clipboard
  clipboard = getContentOfClipboard()

  focus = unFocusFilePath(focus)

  if iUsedCtrlA:
    iUsedCtrlA, user_input = unFocusCtrlA(iUsedCtrlA, user_input)

  # WAIT TO QUIT 
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

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

    finalListOfData, doesMyFileExist = fileOpenning(part1, finalListOfData, count, doesMyFileExist)

    if doesMyFileExist:
        if iPressedMyButton:

          dataOfCoordinatesSorting(finalListOfData)

          ##if len(coordinatesOfLayer) == 0:
          coordinatesOfLayer = whereToDrawLine(finalListOfData, coordinatesOfLayer)

          iPressedMyButton = False

  # Check If I Pressed My Button
  myChangingColor, iPressedMyButton, lblButton, iPressedMyStopButton, pathChecker = clickButtonDetect(myChangingColor, iPressedMyButton, lblButton, iPressedMyStopButton, pathChecker, path)
  stopButtonColor, iPressedMyStopButton, lblStopButton = clickStopButtonDetect(stopButtonColor, iPressedMyStopButton, lblStopButton)
  
  if iPressedMyButton:
    if pathChecker != path:
      coordinatesOfLayer = []

  # VISUAL AND CONSTANT STUFF
  setBackgroundColor()
  drawVisualArea()

  # Draw the path area and the letter input
  xText, yText, user_input = drawPathArea(user_input, xText, yText)
  
  # Draw a label "EV Test :"
  ecran.blit(lblFindEvtest, (700, 20))

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

  if not(doesMyFileExist):
    # Show an error when the file cannot be found
    ecran.blit(lblFileError, (xPathField, yPathField + 25))

  # Call mouse Manager
  changeMyMouseLook()  

  if not(iPressedMyStopButton):
    loopData = drawLine(coordinatesOfLayer, validState, loopData)

  pygame.display.update() 

pygame.quit()