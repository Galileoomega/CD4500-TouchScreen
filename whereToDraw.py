import appender
from importlib import reload

appender = reload(appender)

releaseSeparator = 111111
myFinalList = []

def lineBuild(myList, myFinalList):

  if myList[1] >= 0:
    for u in range(0, len(myList)):
      myList[u] = (str(myList[u]))

    index = -1
    print("MY ENTRY ::::", myList)

    for u in range(0, len(myList)):
        index += 2
        try:
          try:
            myList[index] = int(myList[index])
          except ValueError:
            myList.pop(index)
        except IndexError:
          pass

  firstPassOfX = firstPassOfY = True
  iHaveMyNextDataX = iHaveMyNextDataY = False
  press = yAdded = xAdded = False

  lineX = lineY = count = 0
  nextLineX = nextLineY = -1
  

  for u in range(count, len(myList)):
    needToExit = False
    # Detect if Press or Release.
    try:
      # If its a press or a release
      if myList[count] == "57":
        count +=1
        if xAdded:
          if not(yAdded):
            myFinalList.append(nextLineY * 2)

        xAdded = yAdded = False

        if not(firstPassOfX):
          if not(firstPassOfY):
            if nextLineX == lineX:
              if nextLineY == lineY:
                myFinalList.append(lineX * 2)
                myFinalList.append(lineY * 2)

        lineY = 0
        iHaveMyNextDataX = iHaveMyNextDataY = False  

        # Press
        if myList[count] >= 0:
          press = True
          count += 1
        # Release
        else:
          firstPassOfX = firstPassOfY = True
          press = False
          myFinalList.append(releaseSeparator)
      
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
        if myList[count] == "53":
          count += 1

          if iHaveMyNextDataX:
            if not(yAdded):
              if xAdded:
                myFinalList.append(nextLineY * 2)
                yAdded = True
                needToExit = True
                count -= 2

          xAdded = True
          if not(needToExit):
            if firstPassOfX:
              lineX = myList[count]
              nextLineX = lineX
              myFinalList.append(lineX * 2)
              firstPassOfX = False
            else:
              nextLineX = myList[count]
              if xAdded:
                myFinalList.append(nextLineX * 2)
              iHaveMyNextDataX = True
        else:
          if lineX != 0:
            myFinalList.append(lineX * 2)
            xAdded = True
        

        # If its a Y position
        if myList[count] == "54":
          count += 1

          if not(xAdded):
              myFinalList.append(nextLineX * 2)
              xAdded = True

          yAdded = True

          if firstPassOfY:
            lineY = myList[count]
            nextLineY = lineY
            myFinalList.append(lineY * 2)
            firstPassOfY = False
          else:
            nextLineY = myList[count]
            myFinalList.append(nextLineY * 2)
            iHaveMyNextDataY = True
        else:
          if lineY != 0:
            myFinalList.append(lineY * 2)
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


  return myFinalList