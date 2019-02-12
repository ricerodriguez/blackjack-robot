import cv2 as cv

class ImageProcessor:
    def __init__(self, pathname):
        self.path = pathname
        self.img = cv.imgread(cv.samples.findFile(pathname))
        # Exit if can't find source file
        if self.img is None:
            print('ERROR: CANNOT FIND FILE ' + str(pathname))
            exit(0)
        # Do the rest

    def threshold_img(self):
        gray = cv.cvtColor(self.img,cv.COLOR_BGR2GRAY)
        
