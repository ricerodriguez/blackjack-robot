import cv2 as cv
import numpy as np
import sys

cam = cv.VideoCapture(0)

class ImageProcessor:
    def __init__(self, im, test=False):
        self.im = im
        self.test = test

    def prep(self,im=self.im):
        gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(gray,(0,0),2)

        # Adaptive thresholding
        thresh = cv.adaptiveThreshold(blur,255,1,1,11,1)

        # Kernel for erosion, dilation
        kernel = np.ones((5,5),np.uint8)
        # Erosion
        ero = cv.erode(thresh,kernel,iterations=1)
        # Dilation
        dil = cv.dilate(ero,kernel,iterations=1)
        # Canny edge detection
        edges = cv.Canny(dil,0,255)
        # Masking algorithm from one of the tutorials on OpenCV
        mask = edges != 0
        dst = im * (mask[:,:,None].astype(im.dtype))

        return gray, blur, thresh, ero, dil, edges, dst

    def __sort_cont_area(self,contours,length=5):
        cont_sort = sorted(contours,key=cv.contourArea,reverse=True)[:length]
        self.comp = cont_sort[-1]
        return cont_sort

    def __sort_cont_dist(self,contours):
        comp = self.comp
        M = cv.moments(contours)
        x = M['m10']/M['m00']
        y = M['m01']/M['m00']
        center_this = [x,y]

        M_comp = cv.moments(comp)
        x_comp = M_comp['m10']/M_comp['m00']
        y_comp = M_comp['m01']/M_comp['m00']
        center_comp = [x_comp,y_comp]
        
        dx = center_this[0] - center_comp[0]
        dy = center_this[1] - center_comp[1]
        D = np.sqrt(dx*dx+dy*dy)
        return D

    def isolate_rank_suit(self,contours):
        cont_sort_area = self.__sort_cont_area(contours)
        cont_sort_dist = sorted(cont_sort_area,key=self.__sort_cont_dist,reverse=True)
        return cont_sort_dist[-2:]




if __name__=='__main__':
    test = False
    if (len(sys.argv) == 2):
        if ('-t' in sys.argv[1]):
            test = True
    else:
        test = False
    _, im = cam.read()
    ch = ImageProcessor(test,im)
    gray, blur, thresh, ero, dil, edges, masked = ch.prep(im)
    _, contours, _ = cv.findContours(edges,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    disp = ch.isolate_rank_suit(contours)
    draw = np.zeros_like(im)
    cv.drawContours(draw,disp,-1,(255,255,0),2)
    cv.waitKey(0)
    # cont_sort_area = ch.sort_cont_area(contours)
    # cont_sort_dist = ch.sort_cont_dist(cont_sort_area)
    
    


