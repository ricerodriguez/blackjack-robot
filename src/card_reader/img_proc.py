import cv2 as cv
import numpy as np
import sys
import os

cam = cv.VideoCapture(0)

class ImageProcessor:
    def __init__(self, im, test=False):
        self.im = im
        self.test = test

    def real_prep(self,im):
        gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(gray,(0,0),2)

        # Adaptive thresholding
        thresh = cv.adaptiveThreshold(blur,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY_INV,11,1)
        # Kernel for erosion, dilation
        kernel = np.ones((5,5),np.uint8)
        # Erosion
        ero = cv.erode(thresh,kernel,iterations=1)
        # Dilation
        dil = cv.dilate(ero,kernel,iterations=1)
        # Canny edge detection
        edges = cv.Canny(dil,0,255)

        return gray, blur, ero, dil, edges

    def match_card(self,im):
        path = os.path.dirname(__file__)
        im_path = os.path.join(path, 'images')
        matches = {}
        for file in os.listdir(im_path):
            if file.endswith('.png'):
                print(file)
                test = cv.imread('images/{}'.format(file))
                # print(test)
                _,_,_,_,edges0 = self.real_prep(test)
                _,_,_,_,edges1 = self.real_prep(im)
                _, contours0, _ = cv.findContours(edges0,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
                _, contours1, _ = cv.findContours(edges1,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
                cont_sort0 = sorted(contours0,key=cv.contourArea,reverse=True)
                cont_sort1 = sorted(contours1,key=cv.contourArea,reverse=True)

                match = cv.matchShapes(cont_sort0[-1],cont_sort1[-1],cv.CONTOURS_MATCH_I1,1.0)
                print(match)
                
                

                

    def prep(self,im):
        t = self.test
        gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(gray,(0,0),2)

        # Adaptive thresholding
        thresh = cv.adaptiveThreshold(blur,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY_INV,11,1)
        if t:
            cv.imshow('thresh',thresh)
            cv.waitKey(0)
        # Kernel for erosion, dilation
        kernel = np.ones((5,5),np.uint8)
        # Erosion
        ero = cv.erode(thresh,kernel,iterations=1)
        # Dilation
        dil = cv.dilate(ero,kernel,iterations=1)
        if t:
            cv.imshow('dil',dil)
            cv.waitKey(0)

            # cv.imshow('thresh2',thresh2)
            # cv.waitKey(0)

        # Canny edge detection
        edges = cv.Canny(dil,0,255)
        # Masking algorithm from one of the tutorials on OpenCV
        mask = edges != 0
        dst = im * (mask[:,:,None].astype(im.dtype))
        if t:
            cv.imshow('masked',dst)
            cv.waitKey(0)

        return gray, blur, thresh, ero, dil, edges, dst

    # def __sort_cont_area(self,contours,length=5):
    #     cont_sort = sorted(contours,key=cv.contourArea,reverse=True)[:length]
    #     self.comp = cont_sort[-1]
    #     return cont_sort

    # def __sort_cont_dist(self,contours):
    #     comp = self.comp
    #     M = cv.moments(contours)
    #     x = M['m10']/M['m00']
    #     y = M['m01']/M['m00']
    #     center_this = [x,y]

    #     M_comp = cv.moments(comp)
    #     x_comp = M_comp['m10']/M_comp['m00']
    #     y_comp = M_comp['m01']/M_comp['m00']
    #     center_comp = [x_comp,y_comp]
        
    #     dx = center_this[0] - center_comp[0]
    #     dy = center_this[1] - center_comp[1]
    #     D = np.sqrt(dx*dx+dy*dy)
    #     return D

    # def isolate_rank_suit(self,contours):
    #     found = False
    #     while not found:
    #         cont_sort_area = self.__sort_cont_area(contours,4)
    #         cont_sort_dist = sorted(cont_sort_area,key=self.__sort_cont_dist)
    #         match = cv.matchShapes(cont_sort_dist[-1],cont_sort_dist[-2],cv.CONTOURS_MATCH_I1,420.69)
    #         print('match: ',match)
    #         found = True

    #     return cont_sort_dist[-2:]

if __name__=='__main__':
    test = False
    if (len(sys.argv) >= 2):
        if ('-t' in sys.argv[1]):
            test = True
    else:
        test = False
    _, im = cam.read()
    if test:
        cv.imshow('test',im)
        cv.waitKey(0)
    ch = ImageProcessor(im,test)
    # gray, blur, thresh, ero, dil, edges, masked = ch.prep(im)
    ranksuit = im[345:420,350:505]
    gray, blur, thresh, ero, dil, edges, masked = ch.prep(ranksuit)
    _, contours, _ = cv.findContours(edges,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)

    # disp = ch.isolate_rank_suit(contours)
    disp = sorted(contours,key=cv.contourArea,reverse=True)[:2]

    
    draw = np.zeros_like(ranksuit)
    cv.drawContours(draw,disp,-1,(255,255,0),2)
    # gray2 = cv.cvtColor(draw, cv.COLOR_BGR2GRAY)
    
    # thresh2 = cv.adaptiveThreshold(gray2,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY_INV,5,1)

    cv.imshow('test',draw)
    cv.waitKey(0)

    if (len(sys.argv) >= 2):
        if not ('-m' in sys.argv[1]):
            cv.imwrite(sys.argv[2],draw)
        else:
            draw2 = np.zeros_like(ranksuit)
            cv.drawContours(draw2,contours,-1,(255,255,0),2)
            ch.match_card(draw2)
        


