import cv2 as cv
import sys, numpy, pytesseract
from PIL import Image

class ImageProcessor:
    def __init__(self, img1, img2):
        # self.path = pathname
        self.img = cv.imread(cv.samples.findFile(img1))
        self.img2 = cv.imread(cv.samples.findFile(img2))
        # Exit if can't find source file
        if self.img is None:
            print('ERROR: CANNOT FIND FILE ' + str(img1))
            exit(0)
        # Do the rest
        self.diff_pics()

    def diff_pics(self):
        img1 = self.threshold_img(self.img)
        img2 = self.threshold_img(self.img2)
        diff = cv.absdiff(img1,img2)
        diff = cv.GaussianBlur(diff,(3,3),5)
        flag, diff = cv.threshold(diff,200,255,cv.THRESH_BINARY)
        print(numpy.sum(diff))
        print(pytesseract.image_to_string(Image.fromarray(img2)))
        cv.imshow('image1',img1)
        cv.imshow('image2',img2)
        cv.imshow('diff',diff)
        cv.waitKey(0)
        cv.destroyAllWindows

    def threshold_img(self,img):
        gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(gray,(7,7),2)
        thresh = cv.adaptiveThreshold(blur,255,1,1,11,1)
        return thresh

if __name__ == "__main__":
    ImageProcessor(sys.argv[1], sys.argv[2])
