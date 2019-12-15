##============================================================ 
##===        Visualise the touch of the CD4500 screen
##===                       
##===                         v1.1.3
##============================================================ 

import pygame, os, re
#os.chdir("C:\\Users\\alimacher\\Desktop\\Work\\1ere annee\\Python\\PyGame\\Dalle_Detect")
os.chdir("C:\\Users\\alexi\\Desktop\\GIT\\CD4500-TouchScreen-1")
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
theresSomething = False
focus = False
iUsedCtrlV = False
iUsedCtrlA = False
iPressedMyButton = False
doesMyFileExist = True

#COLOR VAR
red = (208, 14, 14)
black = (0, 0, 0)
blue = (34,138,164)
white = (255,255,255)
customBlack = (33,29,50)
whiteBackground = (245, 245, 245)
whiteVisualiser = (220, 220, 220)
myChangingColor = whiteVisualiser

#POSITION VAR
pos = pos1 = 0, 0
xPathField = 800
heightInput = 50
widthInput = 860
posXInput = 180
posYInput = yText = 300
xText = 150
xButton = 1000
yButton = 620

#OTHER VAR
user_input_value = ""
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

pressList = ['']
count = -1
finalListOfData = ['']
#for test##################################################
#path = "C:\\Users\\alimacher\\Desktop\\Work\\1ere annee\\Python\\PyGame\\Dalle_Detect\\For test\\debug.txt"
#path = "C:\\Users\\alexi\\Desktop\\GIT\\CD4500-TouchScreen-1\\For Test\\debug.txt"

#-------------------------

#TEXT MANAGE
  #---Define font---
font = pygame.font.Font('Resources\\font.ttf', 14)
secondFont = pygame.font.Font('Resources\\font.ttf', 16)
font2 = pygame.font.Font('freesansbold.ttf', 32)
  #-----------------
  #---Define text---
lblFindEvtest = font.render(str("File EVTEST :"), True, black)
lblFindPath = font.render(str("Search..."), True, black)
lblButton = secondFont.render("Calculate... ", True, black)
user_input = font.render(user_input_value, True, red)
  #-----------------

#-----------FUNCTION-------------

#GRAPHIC : Draw element on the screen
def drawVisualArea():
  pygame.draw.rect(ecran, whiteVisualiser, (20,20,600,500))
  pygame.draw.rect(ecran, myChangingColor, (xButton,yButton,140,50))
  
  ecran.blit(lblButton, (xButton + 30, yButton + 10))

#GRAPHIC : Print user key press
def drawPathArea(user_input, xText, yText):
  pygame.draw.rect(ecran, whiteVisualiser, (xPathField,20,210,23))

  xText, yText, user_input = replaceText(user_input, user_input_value)
  
  if not(clickOnMe):
    pygame.draw.rect(ecran, customBlack, (posXInput,posYInput,widthInput,heightInput))

    #BLIT BLACK BACKGROUND
    ecran.blit(temp, (0,0))
  return xText, yText, user_input

#GRAPHIC
def setBackgroundColor():
  ecran.fill(whiteBackground)

#GRAPHIC
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

#GRAPHIC : Will take the text of the clipboard
def getContentOfClipboard():
  try:
    clipboard = pygame.scrap.get(pygame.SCRAP_TEXT)
    clipboard = clipboard.decode("utf-8")
  except AttributeError:
    pass
  try:
    clipboard = clipboard[:-1]
  except TypeError:
    pass
  return clipboard

#GRAPHIC : Will Put Text In The Clipboard
def textInsertInClipboard():
  pygame.scrap.put()

#GRAPHIC : Detect a CTRL + V or C
def keyboardCommandDetection(user_input_value):
  if event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
      user_input_value += str(clipboard)
      iUsedCtrlV = True
  else:
      iUsedCtrlV = False
  return iUsedCtrlV, user_input_value

#GRAPHIC : Detect a CTRL + A
def selectAllText(user_input_value):
  if event.key == pygame.K_a and pygame.key.get_mods() & pygame.KMOD_CTRL:
    iUsedCtrlA = True
  else:
    iUsedCtrlA = False
    user_input_value = user_input_value
  return iUsedCtrlA, user_input_value

#GRAPHIC
def changeMyMouseLook():
  if not(clickOnMe):
    ecran.blit(MANUAL_CURSOR, ( pygame.mouse.get_pos() ) ) 
  if not(theresSomething):
    if clickOnMe:
      ecran.blit(lblFindPath, (805, 20))

#GRAPHIC : Put a default label if nothing has been wrote 
def itIsEmpty():
  if len(user_input_value) != 0:
    theresSomething = True
  else:
    theresSomething = False
  return theresSomething

#Change his placement when press on search
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

def clickButtonDetect(myChangingColor, iPressedMyButton, lblButton):
  if clickOnMe:
    if pygame.mouse.get_pressed() == (1,0,0):
        if mousePos[0] > xButton:
          if mousePos[0] < xButton + 140:
            if mousePos[1] > yButton:
              if mousePos[1] < yButton + 50:
                myChangingColor = black
                lblButton = secondFont.render("Calculate... ", True, white)
                iPressedMyButton = True
    else:
      myChangingColor = (220,220,220)
      iPressedMyButton = False
      lblButton = secondFont.render("Calculate... ", True, black)
  else:
    myChangingColor = (220,220,220)
    iPressedMyButton = False
    lblButton = secondFont.render("Calculate... ", True, black)
    
  return myChangingColor, iPressedMyButton, lblButton

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
      #Find relevant data
    pressList = re.findall("code 57.*|code 53.*|code 54.*", tempPressEvent)
    
    for u in pressList:
      if u == "Event code 53 (ABS_MT_POSITION_X)":
        pressList.pop(0)
      elif u == "Event code 54 (ABS_MT_POSITION_Y)":
        pressList.pop(0)
      elif u == "Event code 57 (ABS_MT_TRACKING_ID)":
        pressList.pop(0)

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
        if finalListOfData[count] > 0:
          fingerPress = True
          print("Press")
        else:
          fingerPress = False
          print("Released")
      ##else:
      ##  fingerPress = False
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

  return xLine, yLine, xLineEnd, yLineEnd

#--------------------------------

while run:

  clock.tick(60)
  mousePos = pygame.mouse.get_pos()

  #Get what you have in your clipboard
  clipboard = getContentOfClipboard()

  focus = unFocusFilePath(focus)

  if iUsedCtrlA:
    iUsedCtrlA, user_input = unFocusCtrlA(iUsedCtrlA, user_input)

  #WAIT TO QUIT 
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

    elif not(clickOnMe):
      if event.type == pygame.KEYDOWN:

        #Detect if user press CTRL + V
        iUsedCtrlV, user_input_value = keyboardCommandDetection(user_input_value)        

        #Delete element if Backspace is pressed
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
      dataOfCoordinatesSorting(finalListOfData)
      iPressedMyButton = False

  else:
    xLine = 0
    yLine = 0
    xLineEnd = 0
    yLineEnd = 0

  myChangingColor, iPressedMyButton, lblButton = clickButtonDetect(myChangingColor, iPressedMyButton, lblButton)
  
  #VISUAL AND CONSTANT STUFF
  setBackgroundColor()
  drawVisualArea()

  pygame.draw.line(ecran, red, (int(xLine), int(yLine)), (int(xLineEnd), int(yLineEnd)), 5)

  xText, yText, user_input = drawPathArea(user_input, xText, yText)
  
  ecran.blit(lblFindEvtest, (700, 20))

  #Write what the user is typping
  if iUsedCtrlA:
    user_input = secondFont.render(user_input_value, True, black, blue)
  ecran.blit(user_input, (xText, yText))

  if clickOnMe:
    #Hide if the text is going too far
    pygame.draw.rect(ecran, whiteBackground, (1010,20,200,23))

  #Call mouse Manager
  changeMyMouseLook()  

  pygame.display.update() 

pygame.quit()