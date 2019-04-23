import os
import sys
import cv2 as cv
import numpy as np
import logging as log
# from picamera import PiCamera
# cam = PiCamera()
cam = cv.VideoCapture(0)

class RankSuitNotFound(Exception):
    ''' Raised when detecting that the suit or rank was not found '''
    def __init__(self,expression,message):
        self.expression = expression
        self.message = message

def prep(im,test, mode=True):
      # Convert to gray and blur it
    gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray,(0,0),2)
    # Adaptive thresholding
    thresh = cv.adaptiveThreshold(blur,255,1,1,11,1)
    if test:
        cv.imshow('Adaptive Thresholding',thresh)
        cv.waitKey(0)
    kernel = np.ones((5,5),np.uint8)
    ero = cv.erode(thresh,kernel,iterations=1)
    if mode:
        # Gaussian blur
        dil = cv.dilate(ero,kernel,iterations=2)
        if test:
            cv.imshow('Dilation (2 iterations)',dil)
            cv.waitKey(0)
    else:
        dil = cv.dilate(ero,kernel,iterations=3)
        if test:
            cv.imshow('Dilation (3 iterations)',dil)
            cv.waitKey(0)
            

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
        color1 = (255, 255, 0)
        color2 = (255, 128, 0)
        point1 = (int(boundRect[i][0]), int(boundRect[i][1]))
        point2 = (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3]))
        cv.drawContours(drawing, contours_poly, i, color1)
        cv.rectangle(drawing,point1,point2,color2,2)
    
    return boundRect, contours_poly, centers, drawing

def find_rot_box(contours):
    rects = []
    boxes = []
    for contour in contours:
        peri = cv.arcLength(contour,True)
        poly = cv.approxPolyDP(contour, 0.1*peri, True)
        rect = cv.minAreaRect(contour)
        box = cv.boxPoints(rect)
        box = np.int0(box)
        rects.append(rect)
        boxes.append(box)
    return boxes, rects

        
def canny_sort(mode, test, im):
    _, _, _, _, dil = prep(im,test,mode)
    edges = cv.Canny(dil, 0, 255)
    mask = edges != 0
    dst = im * (mask[:,:,None].astype(im.dtype))
    _, contours, _ = cv.findContours(edges,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    cont_sort = sorted(contours,key=cv.contourArea,reverse=True)[:1]
    if not test:
        if ((cont_sort[-1].size > 350) or cont_sort[-1].size < 200) and mode:
            raise RankSuitNotFound('rank', str(cont_sort[-1].size))
        elif ((cont_sort[-1].size > 400) or cont_sort[-1].size < 200) and not mode:
            raise RankSuitNotFound('suit', str(cont_sort[-1].size))
        else:
            return im, contours, edges, cont_sort
    else:
        return im, contours, edges, cont_sort
        

def find_rank_suit(mode,test,im=None):
    found = False
    if im is None:
        # cam.capture('test.jpg')
        # im = cv.imread('test.jpg')
        s, im = cam.read()
        
    while not found:
        try:
            im, conts, edges, conts_sort = canny_sort(mode,test,im)
            found = True
        except RankSuitNotFound as err:
            log.warning('The {0} found was of size {1}, which is too large to be correct. Trying again.'.format(err.expression, err.message))
            # cam.capture('test.jpg')
            # im = cv.imread('test.jpg')
            s, im = cam.read()
            found = False

    return im, conts, edges, conts_sort

def crop_to_area(im,rect):
    width = int(rect[1][0])
    height = int(rect[1][1])
    box = cv.boxPoints(rect)
    box = np.int0(box)
    src = box.astype('float32')
    dst = np.array([[0, height-1],
                    [0,0],
                    [width-1,0],
                    [width-1, height-1]],np.float32)
    mat = cv.getPerspectiveTransform(src,dst)
    warp = cv.warpPerspective(im,mat,(width,height))
    return warp    

def find_card(test, path=None):
    im, rank_conts, rank_edges, rank = find_rank_suit(True,test)
    _, suit_conts, suit_edges, suit = find_rank_suit(False,test,im)
    i = 0

    match = cv.matchShapes(rank[-1],suit[-1],cv.CONTOURS_MATCH_I1,420.69)
    # if (len(sys.argv[1]) >= 2):
    #     if not ('-t' in sys.argv[1]):
    if not test:
        while (match < 1 or match > 2):
            match = cv.matchShapes(rank[-1],suit[-1],cv.CONTOURS_MATCH_I1,420.69)
            log.warning('Match was {}. Accidentally found the same thing twice. Trying again.'.format(match))
            i+=1
            if (i >= 5):
                im, rank_conts, rank_edges, rank = find_rank_suit(True,test)
                _, suit_conts, suit_edges, suit = find_rank_suit(False,test,im)
            else:
                im, rank_conts, rank_edges, rank = find_rank_suit(True,test)
        
    print('rank: \n\t size: ',rank[-1].size,'\n\t shape: ',rank[-1].shape)
    print('suit: \n\t size: ',suit[-1].size,'\n\t shape: ',suit[-1].shape)
    print('match: ',match)
    
    _, rank_polys, _, rank_box_drawing = find_box(rank, rank_edges)
    _, suit_polys, _, suit_box_drawing = find_box(suit, suit_edges)
    rank_boxes, rank_rot_rects = find_rot_box(rank)
    suit_boxes, suit_rot_rects = find_rot_box(suit)

    rank_rot_rects = sorted(rank_rot_rects)
    
    new_im_rank = np.zeros_like(im)
    cv.drawContours(new_im_rank, rank_polys, -1, (128,255,0),2)
    new_im_suit = np.zeros_like(im)
    cv.drawContours(new_im_suit, suit_polys, -1, (128,255,0),2)
    rank_rect = rank_rot_rects[-1]
    suit_rect = suit_rot_rects[-1]
    
    rank_warp = crop_to_area(new_im_rank,rank_rect)
    suit_warp = crop_to_area(new_im_suit,suit_rect)

    cv.imshow('test',rank_warp)
    cv.waitKey(0)

    cv.imshow('test',suit_warp)
    cv.waitKey(0)

    max_x = max(rank_warp.shape[0], suit_warp.shape[0])
    max_y = max(rank_warp.shape[1], suit_warp.shape[1])
    max_z = max(rank_warp.shape[2], suit_warp.shape[2])

    sw_copy = suit_warp.copy()
    sw_copy.resize((max_x, max_y, max_z))
    # cv.imshow('suit copy',sw_copy)
    # cv.waitKey(0)
    rw_copy = rank_warp.copy()
    rw_copy.resize((max_x, rw_copy.shape[1], max_z))
    # cv.imshow('rank copy',rw_copy)
    # cv.waitKey(0)

    final_im = np.hstack((rw_copy, sw_copy))
    cv.imshow('test',final_im)
    cv.waitKey(0)

    print('final image: \n\t size: ',final_im.size,'\n\t shape: ',final_im.shape)

    if not path is None:
        if not os.path.exists('images'):
            os.makedirs('images')
        cv.imwrite('images/{}'.format(path),final_im)

    # if (len(sys.argv) == 2):
    #     if not ('-t' in sys.argv[1]):
    #         if not os.path.exists('images'):
    #             os.makedirs('images')
    #         cv.imwrite('images/{}'.format(sys.argv[1]),final_im)
    #     else:
    #         pass
    
if __name__=='__main__':
    test = False
    if (len(sys.argv) == 2):
        if ('-t' in sys.argv[1]):            
            test = True
    else:
        test = False
    find_card(test)
