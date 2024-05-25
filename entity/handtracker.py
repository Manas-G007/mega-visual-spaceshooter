import time,cv2
import numpy as np
import mediapipe as mp

cap=cv2.VideoCapture(0)
pTime=0
c1=10,10,123


class HandTracker:
    def __init__(self):
        self.myHand=mp.solutions.hands
        self.hands=self.myHand.Hands(max_num_hands=1)
        self.myDraw=mp.solutions.drawing_utils
    
    def findHand(self,img,draw=True):
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        results=self.hands.process(imgRGB)
        self.detect=results.multi_hand_landmarks

        if self.detect:
            for lms in self.detect:
                self.lmks=lms.landmark
                if draw:
                    self.myDraw.draw_landmarks(img,lms,self.myHand.HAND_CONNECTIONS)
        return img

    def getPos(self,img,lid,draw=True):
        ih,iw,ic=img.shape
        lmsList=[]
        if self.detect:
            for id,lm in enumerate(self.lmks):
                    x,y=lm.x*iw,lm.y*ih
                    lmsList.append([id,x,y])
                    if draw and lid and (id in lid):
                        x,y=int(x),int(y)
                        cv2.circle(img,(x,y),10,c1,
                                    cv2.FILLED)
        
        return lmsList

def getDist(a,b):
    x1,y1=a
    x2,y2=b
    return np.hypot((x1-x2),(y1-y2))<80

def update(detect):
    global pTime
    success,img = cap.read()
    img=detect.findHand(img)
    focusPoint=[8,12]
    lmList=detect.getPos(img,focusPoint)

    if lmList:
        a1=lmList[focusPoint[0]][1],lmList[focusPoint[0]][2]
        b1=lmList[focusPoint[0]-3][1],lmList[focusPoint[0]-3][2]
        d1=getDist(a1,b1)
        
        a2=lmList[focusPoint[1]][1],lmList[focusPoint[1]][2]
        b2=lmList[focusPoint[1]-3][1],lmList[focusPoint[1]-3][2]
        d2=getDist(a2,b2)

        
        if not d2 and not d1:
            print("shot")
        elif not d1:
            print("track")

    cTime=time.time()
    fps=int(1/(cTime-pTime))
    pTime=cTime

    cv2.putText(img,f"FPS : {fps}",(10,30),2,1,c1)

    cv2.imshow("Tracker",img)
    cv2.waitKey(10)



def main():
    detect=HandTracker()
    while 1:
        update(detect)

if __name__=="__main__":
    main()