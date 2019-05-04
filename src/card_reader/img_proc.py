import cv2 as cv
import numpy as np
import sys
import os

# cam = cv.VideoCapture(0)

class ImageProcessor:
    def __init__(self, im, test=False):
        self.im = im
        self.test = test

    def find_rot_box(self,contours):
        rects = []
        boxes = []
        for contour in contours:
            peri = cv.arcLength(contour,True)
            poly = cv.approxPolyDP(contour, 0.1*peri, True)
            rect = cv.minAreaRect(contour)
            box = cv.boxPoints(rect)
            box = np.int0(box)
            rects.append(rect)
            boxes.append(box)
        return boxes, rects

    def min_xy(self,points,i):
        minxy = points[0]
        for x in points:
            if x[i] < minxy[i]:
                minxy = x

        return minxy

    def max_xy(self,points,i):
        maxxy = points[0]
        for x in points:
            if x[i] > maxxy[i]:
                maxxy = x

        return maxxy

    
    def crop_to_area(self,im,rects):
        rect_r = rects[-1]
        rect_s = rects[-2]
        box_r = cv.boxPoints(rect_r)
        box_r = np.int0(box_r)
        print(box_r)
        box_s = cv.boxPoints(rect_s)
        box_s = np.int0(box_s)
        print(box_s)
        # box = [[min(box_s[0][0],box_s[1][0]),max(box_s[0][1],box_s[1][1])],
        #        box_s[1],
        #       [max(box_s[2][0],box_s[3][0]),box_s[2][1]],
        #       [box_r[3][0],max(box_r[3][1],box_s[3][1])]]
        points = np.concatenate((box_s, box_r))
        # print(self.max_xy(points,0))
        points = sorted(points,key=lambda x:x[0])
        points_l = points[:2]
        points_r = points[-2:]
        bl = self.max_xy(points_l,1)
        tl = self.min_xy(points_l,1)

        br = self.max_xy(points_r,1)
        tr = self.min_xy(points_r,1)
        if (abs(br[0] - tr[0]) >= 15):
            newx = max(br[0],tr[0])
            br[0] = newx
            tr[0] = newx

        if (abs(tl[1] - tr[1]) >= 15):
            newy = min(tl[1],tr[1])
            tl[1] = newy
            tr[1] = newy
            
        box = [bl,tl,tr,br]
        # print(points,bl)
        # box = [self.maxxy(box_s+box_r, 0)
        box = np.int0(box)
        # width = int(rect_r[1][0]+rect_s[1][0])
        # height = int(rect_r[1][1])
        width = int(abs(br[0]-bl[0]))
        height = int(abs(tr[1]-br[1]))
        print(box)
        src = box.astype('float32')
        dst = np.array([[0, height-1],
                        [0,0],
                        [width-1,0],
                        [width-1, height-1]],np.float32)
        mat = cv.getPerspectiveTransform(src,dst)
        warp = cv.warpPerspective(im,mat,(width,height))
        return warp
        

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
                # print(file)
                test = cv.imread('images/{}'.format(file))
                # print(test)
                _,_,_,_,edges0 = self.real_prep(test)
                _,_,_,_,edges1 = self.real_prep(im)
                _, contours0, _ = cv.findContours(edges0,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
                _, contours1, _ = cv.findContours(edges1,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
                cont_sort0 = sorted(contours0,key=cv.contourArea,reverse=True)
                cont_sort1 = sorted(contours1,key=cv.contourArea,reverse=True)

                # boxes0, rects0 = self.find_rot_box(contours0)
                # boxes1, rects1 = self.find_rot_box(contours1)

                # cropped0 = self.crop_to_area(im)
                

                # match = cv.matchShapes(cont_sort0[-1],cont_sort1[-1],cv.CONTOURS_MATCH_I1,1.0)
                # print(match)

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
        _, contours, _ = cv.findContours(edges,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
        
        cont_sort = sorted(contours,key=cv.contourArea,reverse=True)[:2]

        canvas = np.zeros_like(dil)
        cv.drawContours(canvas,cont_sort,-1,(255,255,0),2)
        boxes, rects = self.find_rot_box(cont_sort)
        print(rects[-1])
        final_im = np.zeros_like(dil)
        cv.drawContours(final_im,contours,-1,(255,255,0),2)
        cropped = self.crop_to_area(final_im,rects)

        
        
        
        if t:
            cv.imshow('contours',canvas)
            cv.waitKey(0)
            cv.imshow('masked',dst)
            cv.waitKey(0)

        return gray, blur, thresh, ero, dil, edges, contours, boxes, rects, cropped

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
    # _, im = cam.read()
    im = cv.imread('test.jpg')
    if test:
        cv.imshow('test',im)
        cv.waitKey(0)
    ch = ImageProcessor(im,test)
    # gray, blur, thresh, ero, dil, edges, masked = ch.prep(im)
    ranksuit = im[345:420,350:505]
    gray, blur, thresh, ero, dil, edges, contours, boxes, rects, cropped = ch.prep(ranksuit)

    # disp = ch.isolate_rank_suit(contours)
    disp = sorted(contours,key=cv.contourArea,reverse=True)[:2]
    
    draw = np.zeros_like(ranksuit)
    cv.drawContours(draw,disp,-1,(255,255,0),2)
    # gray2 = cv.cvtColor(draw, cv.COLOR_BGR2GRAY)
    
    # thresh2 = cv.adaptiveThreshold(gray2,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY_INV,5,1)

    cv.imshow('cropped',cropped)
    cv.waitKey(0)

    if (len(sys.argv) >= 2):
        if not ('-m' in sys.argv[1] or '-t' in sys.argv[1]):
            cv.imwrite(sys.argv[1],cropped)
        else:
            draw2 = np.zeros_like(ranksuit)
            cv.drawContours(draw2,contours,-1,(255,255,0),2)
            ch.match_card(draw2)
        


