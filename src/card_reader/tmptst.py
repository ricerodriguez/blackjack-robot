import cv2 as cv
import numpy as np
from picamera import PiCamera

cam = PiCamera()

# def crop_minAreaRect(img, rect):

#     # rotate img
#     angle = rect[2]
#     print(angle)
#     rows,cols = img.shape
#     M = cv.getRotationMatrix2D((cols/2,rows/2),angle,1)
#     img_rot = cv.warpAffine(img,M,(cols,rows))

#     # rotate bounding box
#     rect0 = (rect[0], rect[1], 0.0) 
#     box = cv.boxPoints(rect0)
#     pts = np.int0(cv.transform(np.array([box]), M))[0]    
#     pts[pts < 0] = 0

#     # crop
#     img_crop = img_rot[pts[1][1]:pts[0][1], 
#                        pts[1][0]:pts[2][0]]

#     return img_crop



cam.capture('test.jpg')
im = cv.imread('test.jpg')
gray = cv.cvtColor(im,cv.COLOR_BGR2GRAY)
blur = cv.GaussianBlur(gray, (7,7),2)
thresh = cv.adaptiveThreshold(blur,255,1,1,11,1)
kernel = np.ones((5,5),np.uint8)
ero = cv.erode(thresh,kernel,iterations=1)
dil = cv.dilate(ero,kernel,iterations=1)

cv.imshow('thresholded',thresh)
cv.waitKey(0)

cv.imshow('erosion + dilation',dil)
cv.waitKey(0)

_, conts, hiers = cv.findContours(dil,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
tmpconts = conts.copy()

for i in range(len(tmpconts)):
    try:
        peri = cv.arcLength(tmpconts[i],True)
        approx = cv.approxPolyDP(tmpconts[i],0.01*peri,True)
        if ((cv.contourArea(tmpconts[i]) > 25000) and (len(approx) == 4)):
            del tmpconts[i]
    except:
        break
print(len(tmpconts))
print(len(conts))

areas = [None] * len(tmpconts)
for i in range(len(tmpconts)):
    areas[i] = cv.contourArea(tmpconts[i])
maxcnt = tmpconts[areas.index(max(areas))]
print(cv.contourArea(maxcnt))
crdcnts0 = np.zeros_like(im)
crdcnts1 = np.zeros_like(im)
crdcnts2 = np.zeros_like(im)

cv.drawContours(crdcnts0, tmpconts, -1, (255,255,0),3)
cv.imshow('contours',crdcnts0)
cv.waitKey(0)

cv.drawContours(crdcnts1, maxcnt, -1, (255,255,0),3)
cv.imshow('contours',crdcnts1)
cv.waitKey(0)

rect = cv.minAreaRect(tmpconts)
box = cv.boxPoints(rect)
box = np.int0(box)
cv.drawContours(crdcnts2, [box], -1, (255,255,0),3)
cv.imshow('min area rect',crdcnts2)
cv.waitKey(0)

angle = rect[2]
print(angle)
rows,cols = im.shape[0],im.shape[1]
M = cv.getRotationMatrix2D((cols/2,rows/2),angle,1)
im_rot = cv.warpAffine(im,M,(cols,rows))
cv.imshow('rotated',im_rot)
cv.waitKey(0)
