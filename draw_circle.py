# draw line

import math
import numpy as np
import cv2 as cv2
drawing = False  # true if mouse is pressed
drawEnd = False
img = np.zeros((512, 512, 3), np.uint8)
circleInputData = []

def worstCaseAssess(radius):
    n = 2 * radius
    return 2 * n * (n+1) / 3

def circleAssess(circleInput, center, radius):
    sum = 0
    #print(center[0] , center[1])
    for point in circleInput:
        #print("중심: (", center[0] , center[1],"), 그리고 점: (", point[0], point[1], ")")
        distance = radius - math.sqrt(pow(point[0] - center[0], 2) + pow(point[1] - center[1], 2))
        sum += pow(distance, 2)
    print("오잉?", sum / len(circleInput))
    return sum / len(circleInput)
    
def circleInfer(circleInput):
    center = np.asarray(np.rint(np.mean(circleInput , axis = 0)), dtype = int)
    #return Center
    
    UpRadius = 512
    DownRadius = 0
    for i in range(20):
        #print(UpRadius, DownRadius)
        TargetRadius1 = (2 * UpRadius + DownRadius) / 3
        TargetRadius2 = (UpRadius + 2 * DownRadius) / 3
        
        if circleAssess(circleInput, center, TargetRadius1) >= circleAssess(circleInput, center, TargetRadius2):
            UpRadius = TargetRadius1
        else:
            DownRadius = TargetRadius2
    
    return center, round(UpRadius)       

def paint_draw(event, former_x, former_y, flags, param):
    global current_former_x, current_former_y, drawing, drawEnd, img, circleInputData
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        current_former_x, current_former_y = former_x, former_y
        
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            if drawEnd == True:
                img = np.zeros((512, 512, 3), np.uint8)
                drawEnd = False;
                circleInputData = [];
            
            circleInputData.append([current_former_x, current_former_y])
            
            cv2.line(img, (current_former_x, current_former_y),
                    (former_x, former_y), (0, 0, 255), 5)
            current_former_x = former_x
            current_former_y = former_y
    
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        drawEnd = True;
        cv2.line(img, (current_former_x, current_former_y),
                 (former_x, former_y), (0, 0, 255), 5)
        current_former_x = former_x
        current_former_y = former_y
        
        circleInputData.append([former_x, former_y])
        
        center, radius = circleInfer(circleInputData)
        worstCase = worstCaseAssess(radius)
        print(worstCase)
        print("제 점수는요.." , round(worstCase - circleAssess(circleInputData, center, radius) / worstCase , 1), "점!!")
        cv2.circle(img, center, radius, (255,212,0), 3) 
    return former_x, former_y


cv2.namedWindow("OpenCV Paint Brush")
cv2.setMouseCallback("OpenCV Paint Brush", paint_draw)

while(1):
    cv2.imshow("OpenCV Paint Brush", img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27 or cv2.getWindowProperty('OpenCV Paint Brush', cv2.WND_PROP_VISIBLE) < 1:
        break

cv2.destroyAllWindows()