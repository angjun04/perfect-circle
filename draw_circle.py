# draw line

import numpy as np
import cv2 as cv2
drawing = False  # true if mouse is pressed
mode = True
ix, iy = -1, -1
img = np.zeros((512, 512, 3), np.uint8)


def paint_draw(event, former_x, former_y, flags, param):
    global current_former_x, current_former_y, drawing, mode
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        current_former_x, current_former_y = former_x, former_y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            if mode == True:
                cv2.line(img, (current_former_x, current_former_y),
                         (former_x, former_y), (0, 0, 255), 5)
                current_former_x = former_x
                current_former_y = former_y
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if mode == True:
            cv2.line(img, (current_former_x, current_former_y),
                     (former_x, former_y), (0, 0, 255), 5)
            current_former_x = former_x
            current_former_y = former_y
    return former_x, former_y


cv2.namedWindow("OpenCV Paint Brush")
cv2.setMouseCallback("OpenCV Paint Brush", paint_draw)

while(1):
    cv2.imshow("OpenCV Paint Brush", img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
