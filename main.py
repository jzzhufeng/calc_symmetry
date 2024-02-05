import cv2
import numpy as np
import sys
import math
from find_hanger_point import check_img
import os

BLACK = [0 ,0 ,0]

def line(h, w, h1, w1, h2, w2):
    k = (w2-w1)/(h2-h1)  # 直线斜率
    b = w1 - k*h1        # 偏移量
    return (h * k + b) <= w   # 返回bool值，如果该点在斜线下方，返回False
    
def cut(img, point_A, point_B):
    h1, w1 = point_A[0], point_A[1]
    h2, w2 = point_B[0], point_B[1]
    height, width, _ = img.shape
    
    up = np.zeros((height, width, 3), dtype='uint8')
    down = np.zeros((height, width,3), dtype='uint8')   # 黑底, 一定要加uint8
    
    for i in range(height):
        for j in range(width):
            if line(i,j, h1, w1, h2, w2):
                up[i,j] = img[i,j]
            else:
                down[i,j] = img[i,j]
    return np.array(up), np.array(down)


def startCalc(path, testDir):
    img = cv2.imread(path)
    img = cv2.copyMakeBorder(img, 50, 50, 0, 0, cv2.BORDER_CONSTANT, value=BLACK) #用黑色拓展上下边界，防止翻转的时候丢失像素
    totalHeight, totalwidth, _ = img.shape

    h = check_img(img, testDir, 2)
    roteate_matrix = cv2.getRotationMatrix2D(center = (totalwidth/2, totalHeight/2), angle=h,scale=1)
    rotated_image = cv2.warpAffine(src=img, M= roteate_matrix, dsize=(totalwidth, totalHeight))
    cv2.imwrite(testDir + 'hanger_rotate.jpg', rotated_image)

    r_circle = check_img(rotated_image, testDir + 'r_', 0)

    cut_x = round(r_circle[0])
    cut_y = r_circle[1]
    point_A = (cut_y, cut_x)
    point_B = (cut_y + 100, cut_x) #构造出一条直线  

    right_raw, left_raw = cut(rotated_image, point_A, point_B)

    left_raw = np.fliplr(left_raw)

    cv2.imwrite(testDir + 'right_raw.jpg', right_raw)
    cv2.imwrite(testDir + 'left_raw.jpg', left_raw)

    right = right_raw[0:right_raw.shape[0], cut_x:right_raw.shape[1]]
    cv2.imwrite(testDir + 'right.jpg', right)
    left = left_raw[0:left_raw.shape[0], totalwidth - cut_x:left_raw.shape[1]]
    cv2.imwrite(testDir + 'left.jpg', left)

    right_new = right
    left_new = left
    if (right.shape[1] < left.shape[1]):
        zeroMat = np.zeros((right.shape[0], left.shape[1] - right.shape[1]))
        print(zeroMat.shape)
        right_new = np.concatenate((right_new, zeroMat), axis = 1)
    elif (right.shape[1] > left.shape[1]):
        zeroMat = np.zeros((right.shape[0], right.shape[1] - left.shape[1], 3))
        print(zeroMat.shape)
        left_new = np.concatenate((left_new, zeroMat), axis = 1)

    dst = cv2.addWeighted(left_new.astype(np.uint8), 0.8, right_new.astype(np.uint8), 0.4, 3)
    cv2.imwrite(testDir + 'dst.jpg', dst)
    list_r = right_new.ravel().tolist()
    list_l = left_new.ravel().tolist()
    total = 0
    piece = 0
    for i, v in enumerate(list_l):
        if v != 0 or list_r[i] != 0:
            total += 1
        if v!= 0 and list_r[i] != 0:
            piece += 1
    print(piece)
    print(total)
    rate = piece / total
    print(rate)

if __name__ == "__main__":
    path = '6-1.png'
    imgName = path.split(".", 1)[0]
    outputDir = 'output/' + imgName + '/'
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
    startCalc(path, outputDir)
