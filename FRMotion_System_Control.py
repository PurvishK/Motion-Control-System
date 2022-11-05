from HelperFunctions import HandModule
import time
from subprocess import call
import numpy as np
import cv2 as openCV
import os
import autopy
import glob
import pyautogui
import face_recognition



flag = 0
widthScreen, heightScreen = 640, 480
frame = 100  # Frame Reduction

videoCapture = openCV.VideoCapture(0)
videoCapture.set(4, heightScreen)
videoCapture.set(3, widthScreen)

previousTimeValue = 0
previousXCoordinate, previousYCoordinate, currentXCoordinate, currentYCoordinate = 0, 0, 0, 0


screenWidth, screenHeight = autopy.screen.size()

handModuleObject = HandModule()


###

known_users = ['/data/faces/khush.jpg', '/data/faces/sasank.jpg']

facesEncodings = []
facesNames = []
currentDirectory = os.getcwd()
path = os.path.join(currentDirectory, 'data/faces/')
listOfFiles = [f for f in glob.glob(path+'*.jpg')]
numberOfFiles = len(listOfFiles)
names = listOfFiles.copy()

print(listOfFiles)

for i in range(numberOfFiles):
    globals()['image_{}'.format(i)] = face_recognition.load_image_file(listOfFiles[i])
    globals()['image_encoding_{}'.format(i)] = face_recognition.face_encodings(globals()['image_{}'.format(i)])[0]
    facesEncodings.append(globals()['image_encoding_{}'.format(i)])
# Create array of known names
    names[i] = names[i].replace(currentDirectory, "")  
    facesNames.append(names[i])

useCurrentFrame = True
name = None
###


while True:
    try:
        _, currentFrame = videoCapture.read()
        handsData, currentFrame = handModuleObject.identifyHands(currentFrame)


        ###
        if flag == 0:
            tempFrame = openCV.resize(currentFrame, (0, 0), fx=0.25, fy=0.25)
            rgbTempFrame = tempFrame[:, :, ::-1]
            if useCurrentFrame:
                name = None
                faceLocations = face_recognition.face_locations(rgbTempFrame)
                faceEncodings = face_recognition.face_encodings(rgbTempFrame, faceLocations)
                faces = []
                for face_encoding in faceEncodings:
                    matches = face_recognition.compare_faces(facesEncodings, face_encoding)
                    name = "Unknown"
                    faceDistances = face_recognition.face_distance(facesEncodings, face_encoding)
                    bestMatchIndex = np.argmin(faceDistances)
                    if matches[bestMatchIndex]:
                        name = facesNames[bestMatchIndex]
                    faces.append(name)
            useCurrentFrame = not useCurrentFrame
            print(name)
        ###


        if handsData:
            # Hand-1
            hand1 = handsData[0]
            lmList1 = hand1["lmList"]
            handType1 = hand1["type"]  # Hand Type Left or Right

            # Debugging
            # print(len(lmList1),lmList1)
            fingers1Shown = handModuleObject.identifyFingers(hand1); print(f"Fingers1: {fingers1Shown}")

            if len(handsData) == 1 and flag == 1:

                # 2. Get the tip of the index and middle fingers
                if len(lmList1) != 0:
                    x1, y1 = lmList1[8][0], lmList1[8][1]
                    x2, y2 = lmList1[12][0], lmList1[12][1]  

                    # 4. Only Index Finger : Moving Mode
                    if fingers1Shown[1] == 1 and fingers1Shown[2] == 0 and fingers1Shown[4] == 0:

                        # 5. Convert Coordinates
                        x3 = np.interp(x1, (frame, widthScreen - frame), (0, screenWidth))
                        y3 = np.interp(y1, (frame, heightScreen - frame), (0, screenHeight))

                        # 6. Smoothen Values
                        currentXCoordinate = previousXCoordinate + (x3 - previousXCoordinate) / 7
                        currentYCoordinate = previousYCoordinate + (y3 - previousYCoordinate) / 7

                        # 7. Move Mouse
                        autopy.mouse.move(screenWidth - currentXCoordinate, currentYCoordinate)
                        openCV.circle(currentFrame, (x1, y1), 8, (255,255,255), openCV.FILLED)
                        previousXCoordinate, previousYCoordinate = currentXCoordinate, currentYCoordinate

                    # 8. Both Index and middle fingers are up : Clicking Mode
                    if fingers1Shown[1] == 1 and fingers1Shown[2] == 1 and fingers1Shown[3] != 1 and fingers1Shown[4] != 1:

                        autopy.mouse.click()

                    # Right Click
                    if fingers1Shown[1] == 1 and fingers1Shown[2] == 1 and fingers1Shown[3] == 1 and fingers1Shown[4] != 1:

                        # autopy.mouse.toggle(down=False, button = autopy.mouse.Button.RIGHT)
                        pyautogui.click(button='right')

                    # Scroll
                    if fingers1Shown[1] == 1 and fingers1Shown[2] == 1 and fingers1Shown[3] == 1 and fingers1Shown[4] == 1:

                        try:

                            tempSuccess2, tempCurrentFrame = videoCapture.read()
                            tempHandsData, tempCurrentFrame  = handModuleObject.identifyHands(tempCurrentFrame)
                            tempLmList2 = tempHandsData[0]["lmList"] 
                            tempx1, tempy1 = tempLmList2[8][0], tempLmList2[8][1]

                            if tempy1 > y1 and fingers1Shown[1] == 1:

                                pyautogui.scroll(100)
                                print("UP")
                            
                            elif tempy1 < y1 and fingers1Shown[1] == 1:

                                pyautogui.scroll(-100)
                                print("Down")
                            
                        except Exception as ScrollError:

                            print(f"ScrollError: {ScrollError}")

                    # Zoom In
                    if fingers1Shown[0] == 1 and fingers1Shown[1] == 1 and fingers1Shown[2] == 1 and fingers1Shown[3] == 0 and fingers1Shown[4] == 1:
                      
                        pyautogui.keyDown('ctrl') 
                        pyautogui.scroll(1)
                        pyautogui.keyUp('ctrl') 

                    # Zoom Out
                    if fingers1Shown[0] == 1 and fingers1Shown[1] == 1 and fingers1Shown[2] == 0 and fingers1Shown[3] == 0 and fingers1Shown[4] == 1:
                    
                        pyautogui.keyDown('ctrl') 
                        pyautogui.scroll(-1)
                        pyautogui.keyUp('ctrl') 

            elif len(handsData) == 2:
                hand2 = handsData[1]
                handType2 = hand2["type"]

                fingers2Shown = handModuleObject.identifyFingers(hand2); print(f"Fingers2: {fingers2Shown}")

                # Pause
                if fingers1Shown[0] == 1 and fingers1Shown[1] == 1 and fingers1Shown[2] == 1 and fingers1Shown[3] == 1 and fingers1Shown[4] == 1 and fingers2Shown[0] == 1 and fingers2Shown[1] == 1 and fingers2Shown[2] == 1 and fingers2Shown[3] == 1 and fingers2Shown[4] == 1:
                    
                    flag = 0
                    print("Pause")
                    name = None
                
                # Play
                elif name in known_users and fingers1Shown[0] == 0 and fingers1Shown[1] == 0 and fingers1Shown[2] == 0 and fingers1Shown[3] == 0 and fingers1Shown[4] == 0 and fingers2Shown[0] == 0 and fingers2Shown[1] == 0 and fingers2Shown[2] == 0 and fingers2Shown[3] == 0 and fingers2Shown[4] == 0:
                    
                    flag = 1
                    print("Play")
                    

                if flag == 1:

                    # Volume Up
                    if fingers1Shown[0] == 1 and fingers1Shown[1] == 1 and fingers1Shown[2] == 1 and fingers1Shown[3] == 0 and fingers1Shown[4] == 1:
                    
                        # pyautogui.press("volumeup")
                        print("Volume Up")
                        call(["amixer", "-D", "pulse", "sset", "Master", "2%+"])


                    # Volume Down
                    if fingers1Shown[0] == 1 and fingers1Shown[1] == 1 and fingers1Shown[2] == 0 and fingers1Shown[3] == 0 and fingers1Shown[4] == 1:
                        
                        # pyautogui.press("volumedown")
                        print("Volume Down")
                        call(["amixer", "-D", "pulse", "sset", "Master", "2%-"])

        if flag == 0:

            openCV.putText(currentFrame, "Pause", (460, 50), openCV.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)

        # 11. Frame Rate
        currentTimeValue = time.time()
        fps = 1 / (currentTimeValue - previousTimeValue)
        previousTimeValue = currentTimeValue
        openCV.putText(currentFrame, str(int(fps)), (20, 50), openCV.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)
        
        # 12. Display
        openCV.imshow("Image", currentFrame)

        if openCV.waitKey(1) == ord('q'):

            break

    except Exception as MainError:
        print(MainError)