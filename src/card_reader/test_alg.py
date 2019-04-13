import cv2 as cv
import numpy as np
import logging as log

from picamera import PiCamera

cam = PiCamera()

def prep(im):
    # Convert to gray and blur it
    gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    # Gaussian blur
    blur = cv.GaussianBlur(gray,(7,7),2)
    # Adaptive thresholding
    thresh = cv.adaptiveThreshold(blur,255,1,1,11,1)
    kernel = np.ones((5,5),np.uint8)
    ero = cv.erode(thresh,kernel,iterations=1)
    dil = cv.dilate(ero,kernel,iterations=1)

    return gray, blur, thresh, ero, dil

#############  Function to put vertices in clockwise order ######################
def rectify(h):
    ''' 
    This function put vertices of square we got, in clockwise order 
    Credit: http://git.io/vGi60A
    '''
    h = h.reshape((4,2))
    hnew = np.zeros((4,2),dtype = np.float32)

    add = h.sum(1)
    hnew[0] = h[np.argmin(add)]
    hnew[2] = h[np.argmax(add)]

    diff = np.diff(h,axis = 1)
    hnew[1] = h[np.argmin(diff)]
    hnew[3] = h[np.argmax(diff)]

return hnew

def find_card():
    # Take a picture
    cam.capture('test.jpg')
    # Read in the card
    im = cv.imread('test.jpg')
    # Prep the image for the rest of everything else
    gray, blur, thresh, ero, dil = prep(im)
    # Find contours, save them to vector
    _, contours, hiers = cv.findContours(ero, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    # Sort contours (Credit: https://github.com/arnabdotorg/Playing-Card-Recognition/blob/master/card_img.py)
    cont_sort = sorted(contours,key=cv.contourArea,reverse=True)[:1]
    card = cont_sort[-1]
    peri = cv.arcLength(card, True)
    approx = rectify(cv.approxPolyDP(card,0.02*peri,True))
    h = np.array([ [0,0], [500, 0], [500,500], [0,500]], np.float32)
    tf = cv.getPerspectiveTransform(approx,h)
    warp = cv.warpPerspective(im,tf,(500,500))
    cv.imshow('warp',warp)
    cv.waitKey(0)
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
    test_crop()
