import cv2 as openCV
import mediapipe

class HandModule:
    def __init__(self):

        self.mediapipeHandsObject = mediapipe.solutions.hands

        # static_image_mode: If set to false, the solution treats the input images as a video stream.
        # max_num_hands = Maximum number of hands to detect.
        # min_detection_confidence = Minimum confidence value ([0.0, 1.0]) from the hand detection model for the detection to be considered successful. Default to 0.5.
        # min_tracking_confidence = Setting it to a higher value can increase robustness of the solution, at the expense of a higher latency. Default to 0.5.

        self.hands = self.mediapipeHandsObject.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.pointIndex = [4, 8, 12, 16, 20]

    def identifyHands(self, currentFrame):
        RGB = openCV.cvtColor(currentFrame, openCV.COLOR_BGR2RGB)
        self.processedHand = self.hands.process(RGB)
        handsData = []
        currentFrameHeight, currentFrameWidth, currentFrameChannels = currentFrame.shape
        if self.processedHand.multi_hand_landmarks:
            for type, lms in zip(self.processedHand.multi_handedness, self.processedHand.multi_hand_landmarks):
                handData = {}
                ## lmList
                mylmList = []
                xList = []
                yList = []
                for id, lm in enumerate(lms.landmark):
                    tempX, tempY, tempZ = int(lm.x * currentFrameWidth), int(lm.y * currentFrameHeight), int(lm.z * currentFrameWidth)
                    mylmList.append([tempX, tempY, tempZ])
                    xList.append(tempX)
                    yList.append(tempY)

                ## bbox
                xMinimum, xMaximum = min(xList), max(xList)
                yMinimum, yMaximum = min(yList), max(yList)
                boxW, boxH = xMaximum - xMinimum, yMaximum - yMinimum
                bbox = xMinimum, yMinimum, boxW, boxH
                centerX, centerY = bbox[0] + (bbox[2] // 2), bbox[1] + (bbox[3] // 2)

                handData["lmList"] = mylmList
                handData["bbox"] = bbox
                handData["center"] = (centerX, centerY)

                if type.classification[0].label != "Right":
                    handData["type"] = "Right"
                else:
                    handData["type"] = "Left"

                handsData.append(handData)

                mediapipe.solutions.drawing_utils.draw_landmarks(currentFrame, lms, self.mediapipeHandsObject.HAND_CONNECTIONS, mediapipe.solutions.drawing_utils.DrawingSpec(color=(255,255,255), thickness=2, circle_radius=3), mediapipe.solutions.drawing_utils.DrawingSpec(color=(0,0,0), thickness=2, circle_radius=3))
                openCV.putText(currentFrame, handData["type"], (bbox[0] - 30, bbox[1] - 30), openCV.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
        
        return handsData, currentFrame

    def identifyFingers(self, handData):
        myHandType = handData["type"]
        myLmList = handData["lmList"]
        if self.processedHand.multi_hand_landmarks:
            fingersShown = []
            # Thumb
            if myHandType == "Left":
                if myLmList[self.pointIndex[0]][0] < myLmList[self.pointIndex[0] - 1][0]:
                    fingersShown.append(1)
                else:
                    fingersShown.append(0)
            else:
                if myLmList[self.pointIndex[0]][0] > myLmList[self.pointIndex[0] - 1][0]:
                    fingersShown.append(1)
                else:
                    fingersShown.append(0)

            # 4 Fingers Shown
            for i in range(1, 5):
                if myLmList[self.pointIndex[i]][1] >= myLmList[self.pointIndex[i] - 2][1]:
                    fingersShown.append(0)
                else:
                    fingersShown.append(1)
        return fingersShown
