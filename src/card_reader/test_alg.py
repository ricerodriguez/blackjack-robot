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
    card_g = cv.blur(card, (3,3))
    # Find contours, save them to vector
    contours, _ = cv.findContours(can_out, cv.RETR_TREE,
                                  cv.CHAIN_APPROX_SIMPLE)
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

    big_box = bound_box.index(max(bound_box))

    x, y, w, h = big_box
    roi = card[y:y+h, x:x+w]
    cv.imwrite(img, roi)
