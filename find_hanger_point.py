import cv2
import numpy as np


ball_color = 'purple'
color_dist = {'red': {'Lower': np.array([0, 60, 60]), 'Upper': np.array([6, 255, 255])},
              'blue': {'Lower': np.array([100, 80, 46]), 'Upper': np.array([124, 255, 255])},
              'green': {'Lower': np.array([35, 43, 35]), 'Upper': np.array([90, 255, 255])},
              'purple': {'Lower': np.array([125, 43, 46]), 'Upper': np.array([155, 255, 255])}
              }

def check_img(imgSrc, testDir, returnIndex):
    img = imgSrc.copy()

    gs_frame = cv2.GaussianBlur(img, (5, 5), 0)# 高斯模糊
    hsv = cv2.cvtColor(gs_frame, cv2.COLOR_BGR2HSV)# 转化成HSV图像
    erode_hsv = cv2.erode(hsv, None, iterations=2) # 腐蚀 粗的变细
    inRange_hsv = cv2.inRange(erode_hsv, color_dist[ball_color]['Lower'], color_dist[ball_color]['Upper'])
    cnts = cv2.findContours(inRange_hsv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    c = max(cnts, key=cv2.contourArea)
    rect = cv2.minAreaRect(c)#返回最小外接矩形的中心点坐标，宽高和倾角
    print(rect)
    box = cv2.boxPoints(rect)

    cv2.drawContours(img, [np.int0(box)], -1, (0, 255, 255), 2)
    cv2.imwrite(testDir + 'find_hanger_box.jpg', img)

    print(rect[returnIndex])
    return rect[returnIndex]




    