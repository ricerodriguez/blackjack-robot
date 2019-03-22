import cv2 as cv
import numpy
import logging

from picamera import PiCamera

cam = PiCamera()

def test_crop():
    cam.capture('test.jpg')
    # Read in the card
    card = cv.imread('test.jpg')
    # Use Canny algorithm to find edges
    can_out = cv.Canny(card, 100, 200)
    
    # Convert to gray and blur it
    card_g = cv.cvtColor(card, cv.COLOR_BGR2GRAY)

    # Gaussian blur
    blur = cv.GaussianBlur(card_g,(7,7),2)

    # Adaptive thresholding
    thresh = cv.adaptiveThreshold(blur,255,1,1,11,1)
    #card_g = cv.blur(card, (3,3))
    # _, thresh = cv.threshold(card_g, 127, 255, 0)
    #cv.imshow('blurred', card_g)
    # Find contours, save them to vector
    img, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    # Approximate contours to polygons + get bounding
    # rects/circles
    cont_poly = [None]*len(contours)
    bound_box = [None]*len(contours)

    # For each of the contours found, approximate a polygon
    # from the contour, then draw a bounding box for that
    # polygon            
    for i,c in enumerate(contours):
        cont_poly[i] = cv.approxPolyDP(c,3,True)
        bound_box[i] = cv.boundingRect(cont_poly[i])

    # Find the biggest bounding box
    areas = []
    for box in bound_box:
        areas.append(box[2]*box[3])

    big_box_i = areas.index(max(areas))
    big_box = bound_box[big_box_i]
    logging.warning('big_box is ' + str(big_box))
    logging.warning('bound_box is ' + str(bound_box))
    logging.warning('areas is ' + str(areas))
    x, y, w, h = big_box
    roi = card[y:y+h, x:x+w]
    cv.imwrite('test1.jpg', roi)
    
if __name__=='__main__':
    test_crop()
