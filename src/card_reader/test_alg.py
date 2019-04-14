import cv2 as cv
import numpy as np
import logging as log
# from scipy.spatial import distance as dist
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

'''
OpenCV Tutorial Code:
https://docs.opencv.org/3.4/da/d0c/tutorial_bounding_rects_circles.html
'''

def find_box(contours, canny_input):
    contours_poly = [None]*len(contours)
    boundRect = [None]*len(contours)
    centers = [None]*len(contours)
    for i, c in enumerate(contours):
        contours_poly[i] = cv.approxPolyDP(c, 3, True)
        boundRect[i] = cv.boundingRect(contours_poly[i])
        centers[i], _ = cv.minEnclosingCircle(contours_poly[i])
        
    drawing = np.zeros((canny_input.shape[0], canny_input.shape[1], 3), dtype=np.uint8)
    
    for i in range(len(contours)):
        # color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
        color1 = (255, 255, 0)
        color2 = (255, 128, 0)
        point1 = (int(boundRect[i][0]), int(boundRect[i][1]))
        point2 = (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3]))
        cv.drawContours(drawing, contours_poly, i, color1)
        cv.rectangle(drawing,point1,point2,color2,2)
        # print(str(test))
    
    return boundRect, contours_poly, centers, drawing

def find_rot_box(contours):
    # polys = []
    rects = []
    boxes = []
    for contour in contours:
        peri = cv.arcLength(contour,True)
        poly = cv.approxPolyDP(contour, 0.1*peri, True)
        rect = cv.minAreaRect(contour)
        box = cv.boxPoints(rect)
        box = np.int0(box)
        # polys.append(poly)
        rects.append(rect)
        boxes.append(box)
    return boxes, rects

        
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
            if mode:
                raise RankSuitNotFound('rank', str(cont_sort[-1].size))
            else:
                raise RankSuitNotFound('suit',str(cont_sort[-1].size))
        else:
            return im, contours, edges, cont_sort

def find_card():
    rank_found = False
    suit_found = False
    while not rank_found:
        try:
            im, rank_conts, rank_edges, rank = canny_sort(True)
            rank_found = True
        except RankSuitNotFound as err:
            log.warning('The {0} found was of size {1}, which is too large to be correct. Trying again.'.format(err.expression, err.message))
            rank_found = False

    while not suit_found:
        try:
            _, suit_conts, suit_edges, suit = canny_sort(False)
            # suit_found = True
        except RankSuitNotFound as err:
            log.warning('The {0} found was of size {1}, which is too large to be correct. Trying again.'.format(err.expression, err.message))
            suit_found = False
            continue

        finally:
            # print('rank size: ',rank[-1].size)
            # print('suit size: ',suit[-1].size)
            if (((cv.matchShapes(rank[-1],suit[-1],cv.CONTOURS_MATCH_I1,420.69)) < 3) or ((cv.matchShapes(rank[-1],suit[-1],cv.CONTOURS_MATCH_I1,420.69)) > 4)):
            # if ((cv.matchShapes(rank[-1],suit[-1],cv.CONTOURS_MATCH_I1,420.69)) > 4):
                match = cv.matchShapes(rank[-1],suit[-1],cv.CONTOURS_MATCH_I1,420.69)
                log.warning('Match was {}. Accidentally found the same thing twice. Trying again.'.format(match))
                suit_found = False
            else:
                print('Correct rank and suit sizes: \n',rank[-1].size,'\n',suit[-1].size,'\nContour match:',(cv.matchShapes(rank[-1],suit[-1],cv.CONTOURS_MATCH_I1,420.69)))
                suit_found = True
            # print(str(cv.matchShapes(rank[-1],suit[-1],cv.CONTOURS_MATCH_I1, 420.69)))
                

    
    _, rank_polys, _, rank_box_drawing = find_box(rank, rank_edges)
    _, suit_polys, _, suit_box_drawing = find_box(suit, suit_edges)
    rank_boxes, rank_rot_rects = find_rot_box(rank)
    suit_boxes, suit_rot_rects = find_rot_box(suit)

    def get_size(rect):
        return rect.size
    
    rank_rot_rects = sorted(rank_rot_rects)
    
    new_im_rank = np.zeros_like(im)
    cv.drawContours(new_im_rank, rank_polys, -1, (128,255,0),2)
    # rect = rank_rot_rect[-1]
    center, size, angle = rank_rot_rects[-1]
    center, size = tuple(map(int,center)),tuple(map(int,size))
    print(size)
    test = cv.getRectSubPix(new_im_rank, size, center)
    
    draw_suit = np.zeros_like(im)
    draw_rank = np.zeros_like(im)
    draw_min_suit = np.zeros_like(im)
    draw_min_rank = np.zeros_like(im)
    
    cv.drawContours(draw_suit, suit, -1, (255,255,0),3)
    cv.imshow('working',draw_suit)
    cv.waitKey(0)

    cv.drawContours(draw_min_suit,suit_boxes,0,(255,135,0),2)
    cv.imshow('working',draw_min_suit)
    cv.waitKey(0)

    cv.drawContours(draw_rank, rank, -1, (255,255,0),3)
    cv.imshow('working',draw_rank)
    cv.waitKey(0)

    cv.drawContours(draw_min_rank,rank_boxes,0,(255,135,0),2)
    cv.imshow('working',draw_min_rank)
    cv.waitKey(0)

    cv.imshow('working',test)
    cv.waitKey(0)

    # cv.imshow('working',rank_box_drawing)
    # cv.waitKey(0)
    
if __name__=='__main__':
    find_card()
