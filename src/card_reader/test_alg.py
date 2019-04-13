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
        # print('got to here')
        gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
        # Gaussian blur
        blur = cv.GaussianBlur(gray,(9,9),2)
        # Adaptive thresholding
        thresh = cv.adaptiveThreshold(blur,255,1,1,11,1)
        kernel = np.ones((5,5),np.uint8)
        ero = cv.erode(thresh,kernel,iterations=1)
        dil = cv.dilate(ero,kernel,iterations=1)
        

    return gray, blur, thresh, ero, dil

def find_box(contours, canny_input):
    contours_poly = [None]*len(contours)
    boundRect = [None]*len(contours)
    # centers = [None]*len(contours)
    # radius = [None]*len(contours)
    for i, c in enumerate(contours):
        contours_poly[i] = cv.approxPolyDP(c, 3, True)
        boundRect[i] = cv.boundingRect(contours_poly[i])
        # centers[i], radius[i] = cv.minEnclosingCircle(contours_poly[i])
    
    
    drawing = np.zeros((canny_input.shape[0], canny_input.shape[1], 3), dtype=np.uint8)
    return boundRect, contours_poly, drawing
    
    
    for i in range(len(contours)):
        color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
        cv.drawContours(drawing, contours_poly, i, color)
        cv.rectangle(drawing, (int(boundRect[i][0]), int(boundRect[i][1])), \
          (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), color, 2)
        cv.circle(drawing, (int(centers[i][0]), int(centers[i][1])), int(radius[i]), color, 2)
        
def canny_sort(mode=True, dil=None, im=None):
    if not ((dil is None) and (im is None)):
        edges = cv.Canny(dil, 0, 255)
        mask = edges != 0
        dst = im * (mask[:,:,None].astype(im.dtype))
        _, contours, _ = cv.findContours(edges,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
        cont_sort = sorted(contours,key=cv.contourArea,reverse=True)[:1]
        return im, contours, edges, cont_sort
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
            return im, contours, edges, cont_sort

def find_card():
    found = False
    while not found:
        try:
            im, rank_conts, rank_edges, rank = canny_sort(True)
            _, suit_conts, suit_edges, suit = canny_sort(False)
            # print('rank size: ',rank[-1].size)
            # print('suit size: ',suit[-1].size)
            if ((cv.matchShapes(rank[-1],suit[-1],cv.CONTOURS_MATCH_I1,420.69)) < 1):
                log.warning('Accidentally found the same thing twice. Trying again.')
                found = False
            else:
                found = True
            # print(str(cv.matchShapes(rank[-1],suit[-1],cv.CONTOURS_MATCH_I1, 420.69)))
        except RankSuitNotFound as err:
            log.warning('The {0} found was of size {1}, which is too large to be correct. Trying again.'.format(err.expression, err.message))
            found = False

    rank_box, _, rank_box_drawing = find_box(rank_conts, rank_edges)
    suit_box, _, suit_box_drawing = find_box(suit_conts, suit_edges)
    draw_suit = np.zeros_like(im)
    draw_rank = np.zeros_like(im)
    # draw_rank_box = np.zeros_like(im)
    # rect_rank = cv.minAreaRect(rank[-1])
    # box_rank = np.int0(cv.boxPoints(rect_rank))
    # print(str(rank))
    # print(str(suit))
    cv.drawContours(draw_suit, suit, -1, (255,255,0),3)
    cv.imshow('suit',draw_suit)
    cv.waitKey(0)

    cv.drawContours(suit_box_drawing, suit, -1, (255,255,0),3)
    cv.imshow('suit',suit_box_drawing)
    cv.waitKey(0)

    cv.drawContours(draw_rank, rank, -1, (255,255,0),3)
    cv.imshow('rank',draw_rank)
    cv.waitKey(0)

    cv.drawContours(rank_box_drawing, rank, -1, (255,255,0),3)
    cv.imshow('rank',rank_box_drawing)
    cv.waitKey(0)
    # cv.drawContours(draw_rank_box, [box_rank], 0, (255,255,0), 2)
    # cv.imshow('rank box', draw_rank_box)
    # cv.waitKey(0)
    
if __name__=='__main__':
    find_card()
