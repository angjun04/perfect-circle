from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.app import App
import kivy
import math
import numpy as np
import cv2 as cv2
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line

kivy.require('2.1.0')  # replace with your current kivy version !

drawing = False  # true if mouse is pressed
drawEnd = False
circleCompletionCheck = 512
img = np.zeros((512, 512, 3), np.uint8)
circleInputData = []


def worstCaseAssess(radius):
    return (4 * pow(radius, 3) + 3 * pow(radius, 2) + 2 * radius) / (12 * radius + 3)


def circleAssess(circleInput, center, radius):
    sum = 0
    #print(center[0] , center[1])
    for point in circleInput:
        #print("중심: (", center[0] , center[1],"), 그리고 점: (", point[0], point[1], ")")
        distance = radius - \
            math.sqrt(pow(point[0] - center[0], 2) +
                      pow(point[1] - center[1], 2))
        sum += pow(distance, 2)
    #print("오잉?", sum / len(circleInput))
    return sum / len(circleInput)


def circleInfer(circleInput):
    center = np.asarray(np.rint(np.mean(circleInput, axis=0)), dtype=int)
    # return Center

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


def paint_draw(event, former_x, former_y, flags, param): # event, flags == touch
    global current_former_x, current_former_y, drawing, drawEnd, img, circleInputData, circleCompletionCheck
    if event == cv2.EVENT_LBUTTONDOWN:
        if drawEnd == True:
            img = np.zeros((512, 512, 3), np.uint8)
            drawEnd = False
            circleInputData = []
            circleCompletionCheck = 512
        drawing = True
        current_former_x, current_former_y = former_x, former_y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            circleInputData.append([current_former_x, current_former_y])
            if len(circleInputData) > 60:
                circleCompletionCheck = min(circleCompletionCheck, math.sqrt(pow(
                    current_former_x - circleInputData[0][0], 2) + pow(current_former_y - circleInputData[0][1], 2)))
            # print(circleCompletionCheck)

            cv2.line(img, (current_former_x, current_former_y),
                     (former_x, former_y), (0, 0, 255), 5)
            current_former_x = former_x
            current_former_y = former_y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        drawEnd = True
        cv2.line(img, (current_former_x, current_former_y),
                 (former_x, former_y), (0, 0, 255), 5)
        current_former_x = former_x
        current_former_y = former_y

        if len(circleInputData) > 10:
            circleCompletionCheck = min(circleCompletionCheck, math.sqrt(pow(
                current_former_x - circleInputData[0][0], 2) + pow(current_former_y - circleInputData[0][1], 2)))
        circleInputData.append([former_x, former_y])

        center, radius = circleInfer(circleInputData)
        worstCase = worstCaseAssess(radius)
        inputCase = circleAssess(circleInputData, center, radius)
        circleCompletionValue = min(1, pow(19/20, circleCompletionCheck - 40))
        # print(worstCase)
        if radius > 0:
            circleScore = max(
                0, round((worstCase - inputCase) / worstCase * 100 * circleCompletionValue, 1))
            font = cv2.FONT_HERSHEY_SIMPLEX
            text = "Score : " + str(circleScore) + " / 100"
            # print(text)

            textsize = cv2.getTextSize(text, font, 1, 2)[0]

            textX = (img.shape[1] - textsize[0]) // 2
            textY = 50

            cv2.putText(img, text, (textX, textY), font, 1, (255, 255, 255), 2)
            print("제 점수는요..", circleScore, "점!!")
        else:
            font = cv2.FONT_HERSHEY_SIMPLEX
            text = "Draw Circle No Dot ):<"
            # print(text)

            textsize = cv2.getTextSize(text, font, 1, 2)[0]

            textX = (img.shape[1] - textsize[0]) // 2
            textY = 50

            cv2.putText(img, text, (textX, textY), font, 1, (255, 255, 255), 2)
            print("점 말고 원을 그리세요 뭐하시는건가요...")
        cv2.circle(img, center, radius, (255, 212, 0), 3)
    return former_x, former_y


class MyPaintWidget(Widget):
    def on_touch_down(self, touch):
        # cv2.namedWindow("OpenCV Paint Brush")
        # cv2.setMouseCallback("OpenCV Paint Brush", paint_draw)

        # while (1):
        #     cv2.imshow("OpenCV Paint Brush", img)
        #     k = cv2.waitKey(1) & 0xFF
        #     if k == 27 or cv2.getWindowProperty('OpenCV Paint Brush', cv2.WND_PROP_VISIBLE) < 1:
        #         break

        # cv2.destroyAllWindows()
        with self.canvas:
            Color(1, 0, 0)
            touch.ud['line'] = Line(points=(touch.x, touch.y))
            # paint_draw(touch.x, touch.y)

    def on_touch_move(self, touch):  # 2
        touch.ud['line'].points += [touch.x, touch.y]


class MyApp(App):
    def build(self):
        return MyPaintWidget()


if __name__ == '__main__':
    MyApp().run()
