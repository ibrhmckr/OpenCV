import cv2
import numpy as np
#from time import sleep
#import pgio
#pi = pigpio.pi()

servoPinVer = 17
servoPinHor = 18

#frame Size
frameWidth = 248
frameHeight = 168

#Read from camera => 0
cap = cv2.VideoCapture(0)

#frame size
cap.set(3,frameWidth) #3 -> frame width
cap.set(4,frameHeight) #4 -> frame height
cap.set(10,100) #10 brightness 

# init x and y kordinates
posX = 0
posY = 0

#h_min, h_max,s_min,s_max, v_min,v_max
hsvVal = [61,109,55,203,125,255]

#PlaceHolder function

def empty(a):
    pass

cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",648,240)
cv2.createTrackbar("Threshold1","Parameters",15,255,empty) #tackbar_name,include_to_this_frame,min,max,function
cv2.createTrackbar("Threshold2","Parameters",30,255,empty)
cv2.createTrackbar("Area","Parameters",300,2000,empty)


def getContours(img,imgContour):
    cx,cy = 0,0 #obj center vals
    contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        areaMin = cv2.getTrackbarPos("Area","Parameters") #Get value from trackbars
        if area > areaMin:
            #cv2.drawContours(imgContour, cnt,-1,(255,0,255),7) #img, points, how_many_corner_to_draw,color,thickness
            peri = cv2.arcLength(cnt,True)#parameters ?
            approx = cv2.approxPolyDP(cnt,0.02 * peri, True) #Number of corner point based on paremeters
            #print(len(approx))
            x, y, w, h = cv2.boundingRect(approx) #?
            cv2.rectangle(imgContour, (x,y), (x+w, y+h),(0,255,0),2) #coordinate left_up_cor and right _bottom_cor, color, thickness    

            cx = int(x + (w/2)) #mid of x dimension
            cy = int(y + (h/2)) #mid of y dimension
                                    #center of frame                    #center of obj
            cv2.line(imgContour,(int(frameWidth/2), int(frameHeight/2)), (cx,cy), (0,0,255),2)
            # line from center of the frame to center of obj
    return cx,cy

def conRange(oldMin, oldMax, newMin, newMax, oldValue):
    return ( ((oldValue - oldMin) * (newMax - newMin)) / (oldMax - oldMin) ) + newMin



while True:
    ###############################################
    ########## 1. image Processing
    ###############################################
    succes,img = cap.read() #succes store return value from cap.read()
    img = cv2.resize(img,(frameWidth,frameHeight))
    imgContour = img.copy() #img coloned
    imgHsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)#Color channel changed to HSV           
                     #h_min , s_min  , v_min
    lower = np.array([hsvVal[0],hsvVal[2],hsvVal[4]])
                    #hmax,s_max,v_max
    upper = np.array([hsvVal[1], hsvVal[3], hsvVal[5]])
    mask = cv2.inRange(imgHsv, lower, upper) #?
    result = cv2.bitwise_and(img,img, mask = mask) #merge image and mask
    mask = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
    

    imgBlur = cv2.GaussianBlur(mask, (7,7),1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
    #trackbar_name, window_name
    threshold1 = cv2.getTrackbarPos("Treshold1","Parameters")
    threshold2 = cv2.getTrackbarPos("Treshold2","Parameters")
    imgCanny = cv2.Canny(imgGray, threshold1, threshold2) # detects edges
    kernel = np.ones((5,5)) #1 lerden olusan 5X5 matrix
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)
    cx,cy = getContours(imgDil, imgContour)
    print("cx , cy: ",cx,cy)


##########################
##### Moving Motors
##########################

    ###Vertical
    if cy!=0: #if obj is not on the corner of window
        centerY = frameWidth //2
        if cy > centerY + 20: #if obj is up than window center move up
            posY = int(np.clip(posY+10,1400,2000)) #move posY+10 up
        elif cy < centerY - 20:
            posY = int(np.clip(posY-10,1400,2000)) #if obj is down window center move down
        #pi.set_servo_pulsewidth(servoPinVer,posY)

    ###Horizontal
    if cx!=0: #if obj is not on the corner of window
        posX = int(conRange(frameWidth,0,1100,1700,cx))
        #pi.set_servo_pulsewidth(servoPinHor,posX)
        
    
    
    
    cv2.imshow("VideQoFrame",imgContour)
    cv2.imshow("imgDial",imgDil)

    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break
    
