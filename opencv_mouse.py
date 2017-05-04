import cv2
import numpy as np
import scipy.ndimage as nd
import chanvese

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

loaded_img = cv2.imread('3063.jpg')
img = np.zeros(loaded_img.shape, np.uint8)
img[:,:] = loaded_img

cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

while(1):
    cv2.imshow('image',img)
    img_seg = rgb2gray(loaded_img)
    mask = np.zeros(img_seg.shape) 

    k = cv2.waitKey(1) & 0xFF
    if k == ord('m'):
        mode = not mode
    elif k == 27:
        break

    elif k == ord('s'):
        if ix > 0 and ix2 > 0 and iy > 0 and iy2 > 0:
            mask[iy:iy2, ix:ix2] = 1
            chanvese.chanvese(img_seg, mask, max_its=1000, display=True, alpha=0.2)
            continue


cv2.destroyAllWindows()
