import cv2 as cv
import numpy as np
# from picamera import PiCamera
class Test:
    def __init__(self, comp):
        self.comp = comp
    
    def sort_by_dist(self,cont):
        # centers = []
        # for cont in contours:
        comp = self.comp
        M = cv.moments(cont)
        # print(M['m10'])
        # print(M['m00'])
        # print(M['m01'])
        x = M['m10']/M['m00']
        y = M['m01']/M['m00']
        center_this = [x,y]
        
        M_comp = cv.moments(comp)
        # print(M_comp['m10'])
        # print(M_comp['m00'])
        # print(M_comp['m01'])
        x_comp = M_comp['m10']/M_comp['m00']
        y_comp = M_comp['m01']/M_comp['m00']
        center_comp = [x_comp,y_comp]
        
        dx = center_this[0] - center_comp[0]
        dy = center_this[1] - center_comp[1]
        D = np.sqrt(dx*dx+dy*dy)
        return D

    # def __sort_match(self,cont):
    #     comp = self.comp
    #     match = cv.match(cont[-1],comp[-1],cv.CONTOURS_MATCH_I1,420.69)

    # def sort_match(self,contours):
    #     for i,cont in enumerate(contours):
    #         if i > 0:
    #             comp = contours[i-1]
    #             match = cv.match(cont,comp,cv.CONTOURS_MATCH_I1,420.69)
            
def prep(im, mode=True, window='working'):
      # Convert to gray and blur it
    gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray,(0,0),2)
    # Adaptive thresholding
    thresh = cv.adaptiveThreshold(blur,255,1,1,11,1)
    # cv.imshow(window,thresh)
    # cv.waitKey(0)
    
    kernel = np.ones((5,5),np.uint8)
    # test_kernel = np.ones((1,1),np.uint8)
    ero = cv.erode(thresh,kernel,iterations=1)
    cv.imshow(window,ero)
    cv.waitKey(0)
    if mode:
        dil = cv.dilate(ero,kernel,iterations=1)        
    else:
        dil = cv.dilate(ero,kernel,iterations=3)        
    # cv.imshow(window,dil)
    # cv.waitKey(0)

    edges = cv.Canny(dil,0,255)
    mask = edges != 0
    dst = im * (mask[:,:,None].astype(im.dtype))
    cv.imshow(window,dst)
    cv.waitKey(0)

    # ero2 = cv.erode(dst,test_kernel,iterations=1)
    # cv.imshow(window,ero2)
    # cv.waitKey(0)
    _, contours, _ = cv.findContours(edges,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    cont_sort = sorted(contours,key=cv.contourArea,reverse=True)[:5]
    for cont in cont_sort:
        print(cv.contourArea(cont))
    tmp = Test(cont_sort[-1])
    # print(COMP)
    cont_dist_sort = sorted(cont_sort,key=tmp.sort_by_dist)

    for i,cont in enumerate(cont_dist_sort):
        print('distance {}: '.format(i),tmp.sort_by_dist(cont))
        print('size {}: '.format(i),cont.size)
        print('shape {}: '.format(i),cont.shape)
    # for i,cont in enumerate(cont_sort):
    #     print('size {}: '.format(i),cont.size)

    draw_all = np.zeros_like(im)
    draw_one = np.zeros_like(im)
    draw_test = np.zeros_like(im)
    cv.drawContours(draw_all,cont_sort[:-2],-1,(128,128,0),3)
    # cv.drawContours(draw_all,contours[1:],-1,(255,255,0),2)
    cv.drawContours(draw_one,cont_sort,-1,(255,255,0),2)
    cv.drawContours(draw_test,cont_dist_sort[-2:],-1,(255,255,0),2)
    cv.imshow(window,draw_all)
    cv.waitKey(0)
    cv.imshow(window,draw_one)
    cv.waitKey(0)

    cv.imshow(window,draw_test)
    cv.waitKey(0)


cam = cv.VideoCapture(0)
_, im = cam.read()
cv.imshow('test',im)
cv.waitKey(0)
prep(im,True,'rank')
# prep(im,False,'suit')
