import cv2 as cv
import numpy as np
import logging as log
from scipy.spatial import distance as dist
from picamera import PiCamera

cam = PiCamera()

def prep(im, mode=None):
    if mode is None:
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

def canny_sort(dil, im):
    edges = cv.Canny(dil, 0, 255)
    mask = edges != 0
    dst = im * (mask[:,:,None].astype(im.dtype))
    _, contours, _ = cv.findContours(edges,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    cont_sort = sorted(contours,key=cv.contourArea,reverse=True)[:1]
    return cont_sort

def find_card():
    # Take a picture
    cam.capture('test.jpg')
    # Read in the card
    im = cv.imread('test.jpg')
    im_alt = im.copy()
    # Prep the image for the rest of everything else
    # gray, blur, thresh, ero, dil = prep(im)
    _, _, _, _, dil_rank = prep(im)
    _, _, _, _, dil_suit = prep(im_alt,True)
    rank = canny_sort(dil_rank, im)
    suit = canny_sort(dil_suit, im_alt)
    print('rank size; ',rank[-1].size)
    print('suit size: ',suit[-1].size)
    # Find contours, save them to vector
    # _, contours, hiers = cv.findContours(dil, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    # # Sort contours (Credit: https://github.com/arnabdotorg/Playing-Card-Recognition/blob/master/card_img.py)
    # cont_sort = sorted(contours,key=cv.contourArea,reverse=True)[:1]
    # print(str(cont_sort))
    # card = cont_sort[-1]
    # peri = cv.arcLength(card, True)
    # approx = cv.approxPolyDP(card,0.02*peri,True)
    # edges = cv.Canny(dil, 0, 255)
    # mask = edges != 0
    # dst = im * (mask[:,:,None].astype(im.dtype))
    # # print(str(dst.shape))
    # _, cont_rank, _ = cv.findContours(edges,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    # cont_sort = sorted(cont_rank,key=cv.contourArea,reverse=True)[:1]
    # # _, cont_suit, _ = 
    
    # drawn_can_conts = np.zeros_like(im)
    # drawn_conts = np.zeros_like(im)
    drawn_maxcont = np.zeros_like(im)
    drawn_can_maxcont = np.zeros_like(im)
    # cv.imshow('edges',edges)
    # cv.waitKey(0)

    # cv.imshow('mask',dst)
    # cv.waitKey(0)

    # cv.drawContours(drawn_conts, contours, -1, (255,255,0),3)
    # cv.imshow('contours',drawn_conts)
    # cv.waitKey(0)

    # cv.drawContours(drawn_can_conts, can_contours, -1, (255,255,0),3)
    # cv.imshow('canny contours',drawn_can_conts)
    # cv.waitKey(0)

    # cv.drawContours(drawn_maxcont, cont_sort, -1, (255,255,0),3)
    # cv.imshow('max contour',drawn_maxcont)
    # cv.waitKey(0)

    cv.drawContours(drawn_can_maxcont, suit, -1, (255,255,0),3)
    cv.imshow('suit',drawn_can_maxcont)
    cv.waitKey(0)
    cv.drawContours(drawn_maxcont, rank, -1, (255,255,0),3)
    cv.imshow('rank',drawn_maxcont)
    cv.waitKey(0)

    # print(str(dst))
    # print(str(mask))
    # print(str(edges))

    # print(str(cv.contourArea(edges)))
    
    # approx_2d = np.zeros((4,2))
    # h = np.array([ [0,0], [500, 0], [500,500], [0,500]], np.float32)

    # for i,row in enumerate(approx):
    #     approx_2d[i] = row[0]

    # print(str(approx_2d))
    # tf = cv.getPerspectiveTransform(order_points(approx_2d),h)
    # warp = cv.warpPerspective(im,tf,(500,500))
    # card_conts = np.zeros_like(im)
    # cv.drawContours(card_conts, cont_sort[-1], -1, (255,255,0),3)

    # cv.imshow('contours',card_conts)
    # cv.waitKey(0)
    # # cv.imshow('im',im)
    # # cv.waitKey(0)

    # # cv.imshow('dil',dil)
    # # cv.waitKey(0)
    
    # # cv.imshow('warp',warp)
    # _, _, thr_warp, _, dil_warp = prep(warp)
    # cv.imshow('warp',thr_warp)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
#    cont_drawn = cv.drawContours(card, contours, -1 (0,255,0),3)
    # Initialize lists for sorted contours and hierarchies
    # # Find the biggest bounding box
    # areas = []
    # for box in bound_box:
    #     areas.append(box[2]*box[3])

    # big_box_i = areas.index(max(areas))
    # big_box = bound_box[big_box_i]
    # logging.warning('big_box is ' + str(big_box))
    # logging.warning('bound_box is ' + str(bound_box))
    # logging.warning('areas is ' + str(areas))
    # x, y, w, h = big_box
    # roi = card[y:y+h, x:x+w]
    # cv.imwrite('test1.jpg', roi)
    
if __name__=='__main__':
    find_card()
