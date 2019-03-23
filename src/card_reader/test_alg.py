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
    return gray, blur, thresh

def test_crop():
    # Take a picture
    cam.capture('test.jpg')
    # Read in the card
    card = cv.imread('test.jpg')
    # Prep the image for the rest of everything else
    gray, blur, thresh = prep(card)
    
    # Find contours, save them to vector
    _, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
#    cont_drawn = cv.drawContours(card, contours, -1 (0,255,0),3)
    # Initialize lists for sorted contours and hierarchies
    cont_sort = []
    cont_inds = []
    cont_areas = []
    hier_sort = []
    cnt_card = None
    # Fill empty list with all the areas
    for cnt in contours:
        area = cv.contourArea(cnt)
        cont_areas.append(area)
    # New list is sorted version
    cont_areas_sort = cont_areas.copy()
    cont_areas_sort.sort()
#    print(cont_areas)
    # Find the index of each sorted one from the old one
    for cnt in cont_areas_sort:
        i_areas = cont_areas.index(cnt)
        cont_inds.append(i_areas)
    # Fill the sorted array with elements of the contours at the index found from last loop
    for i in cont_inds:
        cont_sort.append(contours[i])
        hier_sort.append(hierarchy[0][i])

    for i,cnt in enumerate(cont_sort):
        peri = cv.arcLength(cnt,True)
        poly = cv.approxPolyDP(cnt,0.01*peri,True)

        if ((hier_sort[i][3] == -1) and (len(poly) == 4)):
            cnt_card = cnt
            break
        else:
            pass

    im_card = cv.drawContours(thresh,cnt_card,0,(0,255,0),3)
    cv.imshow('card',im_card)
    cv.imwrite('contours.jpg',im_card)

    

    
        
    
    # # Approximate contours to polygons + get bounding
    # # rects/circles
    # cont_poly = [None]*len(contours)
    # bound_box = [None]*len(contours)

    # # For each of the contours found, approximate a polygon
    # # from the contour, then draw a bounding box for that
    # # polygon            
    # for i,c in enumerate(contours):
    #     cont_poly[i] = cv.approxPolyDP(c,3,True)
    #     bound_box[i] = cv.boundingRect(cont_poly[i])

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
