import cv2 as cv
import numpy as np
import logging as log
from scipy.spatial import distance as dist
from picamera import PiCamera

cam = PiCamera()

def prep(im, mode=True):
    if mode:
        # Convert to gray and blur it
        gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
        # Gaussian blur
        blur = cv.GaussianBlur(gray,(5,5),2)
        # Adaptive thresholding
        thresh = cv.adaptiveThreshold(blur,255,1,1,11,1)
        kernel = np.ones((5,5),np.uint8)
        ero = cv.erode(thresh,kernel,iterations=1)
        dil = cv.dilate(ero,kernel,iterations=1)
    else:
        print('got to here')
        gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
        # Gaussian blur
        blur = cv.GaussianBlur(gray,(9,9),2)
        # Adaptive thresholding
        thresh = cv.adaptiveThreshold(blur,255,1,1,11,1)
        kernel = np.ones((5,5),np.uint8)
        ero = cv.erode(thresh,kernel,iterations=1)
        dil = cv.dilate(ero,kernel,iterations=1)
        

    return gray, blur, thresh, ero, dil

def order_points(pts):
    ''' 
    Order points method from PyImageSearch:

    '''
    # Sort points from x-coordinates
    x_sort = pts[np.argsort(pts[:,0]),:]
    # Grab left-most and right-most points from sorted x points
    left = x_sort[:2, :]
    right = x_sort[2:,:]
    # Sort leftmost coordinates according to their y-coordinates
    left = left[np.argsort(left[:,-1]),:]
    (tl, bl) = left
    d = dist.cdist(tl[np.newaxis],right,"euclidean")[0]
    (br,tr) = right[np.argsort(d)[::-1],:]
    return np.array([tl,tr,br,bl],np.float32)

def canny_sort(dil=None, im=None, mode=True):
    if not (dil is None) and (im is None):
        edges = cv.Canny(dil, 0, 255)
        mask = edges != 0
        dst = im * (mask[:,:,None].astype(im.dtype))
        _, contours, _ = cv.findContours(edges,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
        cont_sort = sorted(contours,key=cv.contourArea,reverse=True)[:1]
        return cont_sort
    elif (dil is None):
        if (im is None):
            cam.capture('test.jpg')
            im = cv.imread('test.jpg')
        else:
            _, _, _, _, dil = prep(im,mode)
            edges = cv.Canny(dil, 0, 255)
            mask = edges != 0
            dst = im * (mask[:,:,None].astype(im.dtype))
            _, contours, _ = cv.findContours(edges,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
            cont_sort = sorted(contours,key=cv.contourArea,reverse=True)[:1]
            if (cont_sort[-1].size > 300):
                canny_sort(dil,im)
            else:
                return cont_sort

def find_card():
    rank = canny_sort()
    suit = canny_sort(mode=False)
    # Take a picture
    # cam.capture('test.jpg')
    # # Read in the card
    # im = cv.imread('test.jpg')
    # im_alt = im.copy()
    # Prep the image for the rest of everything else
    # gray, blur, thresh, ero, dil = prep(im)
    # _, _, _, _, dil_rank = prep(im)
    # _, _, _, _, dil_suit = prep(im_alt,True)
    # rank = canny_sort(dil_rank, im)
    # suit = canny_sort(dil_suit, im_alt)
    # print('rank size; ',rank[-1].size)
    # print('suit size: ',suit[-1].size)

    drawn_maxcont = np.zeros_like(im)
    drawn_can_maxcont = np.zeros_like(im)

    cv.drawContours(drawn_can_maxcont, suit, -1, (255,255,0),3)
    cv.imshow('suit',drawn_can_maxcont)
    cv.waitKey(0)
    cv.drawContours(drawn_maxcont, rank, -1, (255,255,0),3)
    cv.imshow('rank',drawn_maxcont)
    cv.waitKey(0)
    
if __name__=='__main__':
    find_card()
