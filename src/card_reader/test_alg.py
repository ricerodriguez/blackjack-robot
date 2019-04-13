import cv2 as cv
import numpy as np
import logging as log
from scipy.spatial import distance as dist
from picamera import PiCamera

cam = PiCamera()

class RankSuitNotFound(Exception):
    ''' Raised when detecting that the suit or rank was not found '''
    def __init__(self,expression,message):
        self.expression = expression
        self.message = message

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

def canny_sort(mode=True, dil=None, im=None):
    if not ((dil is None) and (im is None)):
        edges = cv.Canny(dil, 0, 255)
        mask = edges != 0
        dst = im * (mask[:,:,None].astype(im.dtype))
        _, contours, _ = cv.findContours(edges,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
        cont_sort = sorted(contours,key=cv.contourArea,reverse=True)[:1]
        return im, cont_sort
    elif (dil is None):
        if (im is None):
            cam.capture('test.jpg')
            im = cv.imread('test.jpg')
            # yield im
        _, _, _, _, dil = prep(im,mode)
        edges = cv.Canny(dil, 0, 255)
        mask = edges != 0
        dst = im * (mask[:,:,None].astype(im.dtype))
        _, contours, _ = cv.findContours(edges,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
        cont_sort = sorted(contours,key=cv.contourArea,reverse=True)[:1]
        if (cont_sort[-1].size > 350):
            # return canny_sort(mode,dil,im)
            if mode:
                raise RankSuitNotFound('rank', str(cont_sort[-1].size))
            else:
                raise RankSuitNotFound('suit',str(cont_sort[-1].size))
        else:
            return im, cont_sort

def find_card():
    found = False
    while not found:
        try:
            im, rank = canny_sort(True)
            _, suit = canny_sort(False)
            print('rank size: ',rank[-1].size)
            print('suit size: ',suit[-1].size)
            if ((cv.matchShapes(rank[-1],suit[-1],cv.CONTOURS_MATCH_I1,420.69)) < 1):
                log.warning('Accidentally found the same thing twice. Trying again.')
                found = False
            else:
                found = True
            # print(str(cv.matchShapes(rank[-1],suit[-1],cv.CONTOURS_MATCH_I1, 420.69)))
        except RankSuitNotFound as err:
            log.warning('The {0} found was of size {1}, which is too large to be correct. Trying again.'.format(err.expression, err.message))
            found = False
            
    draw_suit = np.zeros_like(im)
    draw_rank = np.zeros_like(im)

    cv.drawContours(draw_suit, suit, -1, (255,255,0),3)
    cv.imshow('suit',draw_suit)
    cv.waitKey(0)
    cv.drawContours(draw_rank, rank, -1, (255,255,0),3)
    cv.imshow('rank',draw_rank)
    cv.waitKey(0)
    
if __name__=='__main__':
    find_card()
