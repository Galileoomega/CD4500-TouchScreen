# THIS CONTROLLER CONTAIN A MARSHAL
# Related to v1.1.9

import appender
from importlib import reload

appender = reload(appender)

releaseSeparator = 111111


def lineBuild(myList, myFinalList, iPressedMyTotalButton, resetList):

  if not(iPressedMyTotalButton):
    if resetList:
      myFinalList = []
  
  if iPressedMyTotalButton:
    if len(myFinalList) > (len(myList) * 2):
      myFinalList = []

  marshallLineX = 0
  marshallLineY = 0
  goodNumberMarshall = 0
  valid = True

  if myList[1] >= 0:
    for u in range(0, len(myList)):
      myList[u] = (str(myList[u]))

    index = -1
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
            myFinalList.append(nextLineY * 1.5 + 50)
            goodNumberMarshall += 1

        xAdded = yAdded = False

        if not(firstPassOfX):
          if not(firstPassOfY):
            if nextLineX == lineX:
              if nextLineY == lineY:
                myFinalList.append(lineX * 1.5 + 50)
                myFinalList.append(lineY * 1.5 + 50)
                goodNumberMarshall += 2

        
        iHaveMyNextDataX = iHaveMyNextDataY = False  

        # IF Code 57 is POSITIVE (PUSHED)
        if myList[count] >= 0:
          press = True
          count += 1
        # IF Code 57 is NEGATIVE (RELEASED)
        else:
          firstPassOfX = firstPassOfY = True
          press = False
          if (goodNumberMarshall % 4) != 0:
                if lineY != 0:
                  if lineX != 0:
                    myFinalList.append(lineX * 1.5 + 50)
                    myFinalList.append(lineY * 1.5 + 50)
                    goodNumberMarshall += 2

                elif marshallLineX != 0:
                  if marshallLineY != 0:
                    myFinalList.append(marshallLineX * 1.5 + 50)
                    myFinalList.append(marshallLineY * 1.5 + 50)
                    goodNumberMarshall += 2

                else:
                  myFinalList.append(nextLineX * 1.5 + 50)
                  myFinalList.append(nextLineY * 1.5 + 50)
                  goodNumberMarshall += 2
          if (goodNumberMarshall % 4) != 0:
            myFinalList.append(nextLineY * 1.5 + 50)


          myFinalList.append(releaseSeparator)
          goodNumberMarshall = 0

        marshallLineY = lineY
        lineY = 0
      
    except IndexError:
      break

    if xAdded:
      if yAdded:
        xAdded = yAdded = False
        firstPassOfX = firstPassOfY = False
    
    marshallLineX = lineX
    marshallLineY = lineY

    if press == True:
        
        lineY = 0
        lineX = 0
        # If its a X position
        if myList[count] == "53":
          count += 1

          if iHaveMyNextDataX:
            if not(yAdded):
              if xAdded:
                myFinalList.append(nextLineY * 1.5 + 50)
                goodNumberMarshall += 1

                yAdded = True
                needToExit = True
                count -= 2

          xAdded = True
          if not(needToExit):
            if firstPassOfX:
              lineX = myList[count]
              marshallLineX = lineX

              nextLineX = lineX
              myFinalList.append(lineX * 1.5 + 50)
              goodNumberMarshall += 1

              firstPassOfX = False
            else:
              nextLineX = myList[count]
              if xAdded:
                myFinalList.append(nextLineX * 1.5 + 50)
                goodNumberMarshall += 1

              iHaveMyNextDataX = True
        else:
          if lineX != 0:
            myFinalList.append(lineX * 1.5 + 50)
            goodNumberMarshall += 1

            xAdded = True
        

        # If its a Y position
        if myList[count] == "54":
          count += 1

          if not(xAdded):
              myFinalList.append(nextLineX * 1.5 + 50)
              goodNumberMarshall += 1

              xAdded = True

          yAdded = True

          if firstPassOfY:
            lineY = myList[count]
            marshallLineY = lineY

            nextLineY = lineY
            myFinalList.append(lineY * 1.5 + 50)
            goodNumberMarshall += 1

            firstPassOfY = False
          else:
            nextLineY = myList[count]
            myFinalList.append(nextLineY * 1.5 + 50)
            goodNumberMarshall += 1

            iHaveMyNextDataY = True
        else:
          if lineY != 0:
            myFinalList.append(lineY * 1.5 + 50)
            goodNumberMarshall += 1

            yAdded = True

        if not(iHaveMyNextDataY):
          if not(iHaveMyNextDataX):
                try:     
                  pass       
                  lineX = nextLineX
                  lineY = nextLineY
                except UnboundLocalError:
                  pass
    if lineX != 0:
      if lineY != 0:
        marshallLineX = lineX
        marshallLineY = lineY
    else:
      pass
    count += 1

  marshallLineX = 0
  marshallLineY = 0

  # FOR DEBUG
  #f = open("output.txt", "w+")
  #for u in myFinalList:
  #  f.write(str(u) + "\n")

  #f.close()

  return myFinalList