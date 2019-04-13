import cv2 as cv
import numpy as np
from picamera import PiCamera

def preprocess(im):
    gray = cv.cvtColor(im,cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (7,7),2)
    thresh = cv.adaptiveThreshold(blur, 255, 1, 1, 11, 1)
    return gray, blur, thresh

cam = PiCamera()

cam.capture('test.jpg')
im = cv.imread('test.jpg')
gray = cv.cvtColor(im,cv.COLOR_BGR2GRAY)
blur = cv.GaussianBlur(gray, (7,7),2)
thresh = cv.adaptiveThreshold(blur,255,1,1,11,1)
kernel = np.ones((5,5),np.uint8)
ero = cv.erode(thresh,kernel,iterations=1)
dil = cv.dilate(ero,kernel,iterations=1)

_, conts, hiers = cv.findContours(dil,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
tmpconts = conts.copy()
conts = sorted(conts, key=cv.contourArea,reverse=True)[:1]
for i in range(len(tmpconts)):
    try:
        print('got to here')
        size = cv.contourArea(conts[i])
        peri = cv.arcLength(conts[i],True)
        approx = cv.approxPolyDP(conts[i],0.01*peri,True)
        h = np.array([ [0,0], [500,0], [500,500], [0, 500]], np.float32)
        tf = cv.getPerspectiveTransform(approx,h)
        warp = cv.warpPerspective(thresh, tf, (500,500))
        cv.imshow('warp {}'.format(i), warp)
        cv.waitKey(0)
        # # if ((cv.contourArea(tmpconts[i]) > 25000) and (cv.contourArea(tmpconts[i]) < 6000)
        #     # and (hiers[i][3] == -1) and (len(approx) == 4)):
        # if (((size > 25000) or (size < 6000)) and ((hiers[i][3] != -1) and (len(approx) != 4))):
        #     del tmpconts[i]
    except:
        break
print(len(tmpconts))
print(len(conts))

#areas = [None] * len(tmpconts)
#for i in range(len(tmpconts)):
#    areas[i] = cv.contourArea(tmpconts[i])
#maxcnt = tmpconts[areas.index(max(areas))]
#print(cv.contourArea(maxcnt))
crdcnts0 = np.zeros_like(im)
crdcnts1 = np.zeros_like(im)
crdcnts2 = np.zeros_like(im)

#cv.drawContours(crdcnts0, tmpconts, -1, (255,255,0),3)
maxcnt = conts[-1]
cv.drawContours(crdcnts1, maxcnt, -1, (255,255,0),3)
cv.drawContours(crdcnts0, conts, -1, (255, 255, 0), 3)
rect = cv.minAreaRect(maxcnt)
box = cv.boxPoints(rect)
box = np.int0(box)
cv.drawContours(crdcnts2, [box], -1, (255,255,0),3)

center, size, angle = rect
center, size = tuple(map(int, center)), tuple(map(int, size))
rows,cols = im.shape[0], im.shape[1]
mat = cv.getRotationMatrix2D(center,angle,1)
im_rot = cv.warpAffine(dil,mat,(dil.shape[1], dil.shape[0]))

im_copy = im_rot.copy()
alt = cv.getRectSubPix(im_copy, size, center)

cv.imshow('thresholded',thresh)
cv.waitKey(0)

cv.imshow('erosion + dilation',dil)
cv.waitKey(0)
cv.imshow('contours',crdcnts0)
cv.waitKey(0)
# cv.imshow('contours',crdcnts1)
# cv.waitKey(0)
# cv.imshow('min area rect',crdcnts2)
# cv.waitKey(0)

cv.imshow('alt', alt)
cv.waitKey(0)
#print(str(warp))
#g_warp, b_warp, t_warp = preprocess(warp)

#cv.imshow('warp',t_warp)
#cv.waitKey(0)
