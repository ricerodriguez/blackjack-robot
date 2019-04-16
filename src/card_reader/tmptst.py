import cv2 as cv
import numpy as np
from picamera import PiCamera

def prep(im, mode=True, window):
      # Convert to gray and blur it
    gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    if mode:
        # Gaussian blur
        blur = cv.GaussianBlur(gray,(5,5),2)
    else:
        # Gaussian blur
        blur = cv.GaussianBlur(gray,(9,9),2)
    # Adaptive thresholding
    thresh = cv.adaptiveThreshold(blur,255,1,1,11,1)
    cv.imshow(window,thresh)
    cv.waitKey(0)
    
    kernel = np.ones((5,5),np.uint8)
    ero = cv.erode(thresh,kernel,iterations=1)
    dil = cv.dilate(ero,kernel,iterations=1)
    cv.imshow(window,dil)
    cv.waitKey(0)

    edges = cv.Canny(dil,0,255)
    mask = edges != 0
    dst = im * (mask[:,:,None].astype(im.dtype))
    _, contours, _ = cv.findContours(edges,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    cont_sort = sorted(contours,key=cv.contourArea,reverse=True)[:1]

    draw_all = np.zeros_like(im)
    draw_one = np.zeros_like(im)
    cv.drawContours(draw_all,contours,-1,(255,255,0),2)
    cv.drawContours(draw_one,[cont_sort[-1]],-1,(255,255,0),2)
    cv.imshow(window,draw_all)
    cv.waitKey(0)

    cv.imshow(window,draw_one)
    cv.waitKey(0)



cam = PiCamera()

cam.capture('test.jpg')
im = cv.imread('test.jpg')
prep(im,True,'rank')
prep(im,False,'suit')
