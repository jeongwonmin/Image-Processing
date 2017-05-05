#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import scipy.ndimage as nd
import scipy.signal as sig

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
MOSAIC_SCALE = 10

drawing = False # true if mouse is pressed
mode = True # if True, draw rectangle. Press 'm' to toggle to curve
ix,iy = -1,-1
ix2, iy2 = -1,-1
finish=False

# mouse callback function
def draw_circle(event,x,y,flags,param):
    global ix,iy,ix2,iy2,drawing,mode,finish

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            #if mode == True:
                #cv2.rectangle(img,(ix,iy),(x,y),(255,255,255),-0)
            if mode == False:
                cv2.circle(img,(x,y),2,(0,0,255),-1)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if mode == True:
            cv2.rectangle(img,(ix,iy),(x, y),(0,255,0),1)
            ix2,iy2 = x, y
        else:
            cv2.circle(img,(x,y),2,(0,0,255),-1)
            ix2, iy2 = x, y

loaded_img = cv2.imread('cucumber_sand.jpg')
img = np.zeros(loaded_img.shape, np.uint8)
img[:,:] = loaded_img

cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)

#####################filters######################

sobelX = np.array([[-1, 0, 1],
[-2, 0, 2],
[-1, 0, 1]])
sobelY = sobelX.T

##################################################

if __name__=="__main__":
    while(1):
    
        k = cv2.waitKey(1) & 0xFF
        if k == ord('m'):
            mode = not mode
        elif k == 27:
            break

        filter_image = img[iy:iy2, ix:ix2]
        #選択した領域の輪郭を出す(Sobel Filter)
        if ix > 0 and ix2 > 0 and iy > 0 and iy2 > 0:
            if k == ord('a'):
                filter_image = cv2.cvtColor(filter_image, cv2.COLOR_RGB2GRAY)
                filter_imageX = np.zeros(filter_image.shape)
                filter_imageY = np.zeros(filter_image.shape)
                #nd.sobel(filter_image, 1, filter_imageX)
                #nd.sobel(filter_image, 0, filter_imageY)
                filter_imageX = sig.convolve2d(filter_image, sobelX, 'same')
                filter_imageY = sig.convolve2d(filter_image, sobelY, 'same')
                filter_image = np.sqrt(filter_imageX**2 + filter_imageY**2).astype(np.uint8)
                filter_image = cv2.cvtColor(filter_image,cv2.COLOR_GRAY2RGB)
                img[iy:iy2, ix:ix2] = filter_image
            
            if k == ord('s'):
                mosaic = filter_image
                mosaic_size = filter_image.shape[:2][::-1]
                mosaic = cv2.resize(mosaic,(int(mosaic_size[0]/MOSAIC_SCALE), int(mosaic_size[1]/MOSAIC_SCALE)))
                mosaic = cv2.resize(mosaic,mosaic_size,interpolation = cv2.INTER_NEAREST)
                img[iy:iy2, ix:ix2] = mosaic

            #クリアというか、元のイメージを見せる
            if k == ord('c'):
                img[:,:]=loaded_img

        cv2.imshow('image',img)

    cv2.destroyAllWindows()
