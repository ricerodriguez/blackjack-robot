import cv2 as cv
import numpy
import threading
import os
import time
import logging
import RPi.GPIO as GPIO
from serial import Serial, serialutil
from time import sleep

# Global variables for camera and pin values
cam = cv.VideoCapture(0)
P0 = 10
P1 = 11

# Local package definition for card macros
import CARD_DEFS

# Image and camera package imports

# Global variables for things that will be used throughout
GEN_DECK = CARD_DEFS.GENERAL_DECK

#logging.basicConfig(filename=os.path.join(str(os.path.dirname(__file__)), 'log', 'calibrator.log'), level=logging.INFO)
logging.basicConfig(level=logging.INFO)
class Calibrator(threading.Thread):
    def __init__(self, trigger=None, path=None, deck=None):
        self.path = path
        self.deck = deck
        self._card_map = {}
        self.progress = 0
        self._init_path(path, deck)

        # Initialize the superclass
        threading.Thread.__init__(self)

        # Thread event indicates that the Pi has taken the picture of
        # the card. This means that it is safe for the MSP430 to move
        # the servo for the next card.
        if trigger is None:
            self.snapped = threading.Event()
        else:
            self.snapped = trigger

        # Thread event indicates that the next card is in place for
        # the Pi to take a picture of.
        self.ready = threading.Event()
        self.ready.set()

        # Thread event indicates that the calibration image processing has finished
        
    # Initialize the card map, which maps the card name to the
    # pathname of the image taken of the card
    def _init_path(self, path=None, deck=None):
        # If there is no path indicated and no deck indicated, assume
        # there is only one deck and just create a folder in the
        # current directory
        
        if path is None and deck is None:
            path = os.path.dirname(__file__)
            self.path = os.path.join(path, 'data', 'calib_cards', 'deck_01')
            if not os.path.exists(self.path):
                os.makedirs(self.path)

        # If there is no path given but there is a deck given, create
        # a folder in the current directory and a subfolder to that
        # folder for the current deck
        elif path is None and deck is not None:
            path = os.path.dirname(__file__)
            self.path = os.path.join(path, 'data', 'calib_cards', 'deck_0{}'.format(deck))
            if not os.path.exists(self.path):
                os.makedirs(self.path)

    def run(self):
        # For each kind of card possible...
        for card in GEN_DECK:
            # Wait until the next card is in position to take a picture
            logging.info('CL: Waiting until ready for ' + card)
            self.ready.wait()
            logging.info('CL: Ready to start the process for ' + card)
            print('Taking a picture of ' + card)
            logging.info('CL: Starting the process for ' + card)
            # Clear out the flag for the snapped event
            self.snapped.clear()
            
            # Wait until the ready flag is set
            while not self.ready.is_set():
                self.ready.wait()

            # Clear the flag
            self.ready.clear()
            
            # Make sure there are no spaces in the file name to
            # avoid confusion
            card_name = card.replace(' ', '_')

            # Add the file extension so data type can be inferred
            card_name = card_name + '.png'
            
            # Join the path created earlier with the card_name
            self.filename = os.path.join(self.path, card_name)
            
            # Snap the picture
            _, self.im = cam.read()
            cv.imwrite(self.filename,self.im)
            
            # Add the file name to the map to keep track
            self._card_map[card] = self.filename
            # Set the flag that the picture has been taken
            self.snapped.set()
            logging.info('CL: Set snapped event!')
            self.progress += 1

class CardPhotographer(threading.Thread):
    def __init__(self,trigger):
        self.snapped = trigger
        self.progress = 0
        threading.Thread.__init__(self)
        self.ready = threading.Event()
        self.ready.set()

    def run(self):
        self.snapped.clear()
        self.ready.wait()

        while not self.ready.is_set():
            self.ready.wait()
            
        self.ready.clear()
        _, self.im = cam.read()
        cv.imwrite('card.jpg',self.im)
        self.progress += 1
        self.snapped.set()
        
class ImageProcessor(threading.Thread):
    def __init__(self,cls,trigger):
        self.kaleb = cls
        self.snapped = trigger
        # Initialize the superclass
        threading.Thread.__init__(self)
        self.progress = 0

    def run(self):
        # Credit to OpenCV's tutorial: 'Creating Bounding boxes and
        # circles for contours'
        # Convert to gray and blur it
        while True:
            logging.info('IMAGE PROCESSOR: Waiting for Pi to finish snapping!')
            self.snapped.wait()
            if self.snapped.is_set():
                im_full = self.kaleb.im
                im = im_full[315:415,280:450]
                self.progress += 1
                gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
                blur = cv.blur(im, (3,3))
                # Adaptive thresholding
                thresh = cv.adaptiveThreshold(blur,255,1,1,11,1)
                self.progress += 1
                # Kernel for erosion, dilation
                kernel = np.ones((5,5),np.uint8)
                # Erosion
                ero = cv.erode(thresh,kernel,iterations=1)
                # Dilation
                dil = cv.dilate(ero,kernel,iterations=1)
                self.progress += 1
                # Canny edge detection
                edges = cv.Canny(dil,0,255)
                # Masking algorithm from one of the tutorials on OpenCV
                mask = edges != 0
                dst = im * (mask[:,:,None].astype(im.dtype))
                self.progress += 1
                _, contours, _ = cv.findContours(edges,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
                disp = sorted(contours,key=cv.contourArea,reverse=True)[:2]
                self.progress += 1
                draw = np.zeros_like(ranksuit)
                cv.drawContours(draw,disp,-1,(255,255,0),2)
                cv.imwrite(self.kaleb.filename,draw)
                self.progress += 1
         
class PCBListener(threading.Thread):
    def __init__(self,cls):
        self.kaleb = cls
        # Initialize the superclass
        threading.Thread.__init__(self)
        # GPIO.output(P0, False)
        # GPIO.output(P1, True)        

    def run(self):
        while True:
            if (GPIO.input(trigPin)):
                self.kaleb.ready.set()
                GPIO.output(P0, False)
                GPIO.output(P1, False)

            else:
                GPIO.output(P0, False)
                GPIO.output(P1, True)


class PCBTalker(threading.Thread):
    def __init__(self,trigger):
        self.snapped = trigger
        # Initialize the superclass
        threading.Thread.__init__(self)

    def run(self):
        while True:
            self.snapped.wait()
            if self.snapped.is_set():
                GPIO.output(P0, True)
                GPIO.output(P1, True)

class LuckyCharms(threading.Thread):
    def __init__(self):
        self.cereal = Serial()
        # Initialize the superclass
        threading.Thread.__init__(self)

    def run(self):
        while True:
            try:
                self.cereal = Serial('dev/ttyUSB0',timeout=1)
                logging.info('SUCCESSFULLY CONNECTED')
                # Connected, now listening for what to do
                cmd_raw = self.cereal.readline()
                cmd = str(cmd_raw)
                if (cmd == 'hit'):
                    GPIO.output(P0, False)
                    GPIO.output(P1, True)
                elif (cmd == 'double'):
                    GPIO.output(P0, False)
                    GPIO.output(P1, False)
                elif (cmd == 'stay'):
                    GPIO.output(P0, True)
                    GPIO.output(P1, False)
                else:
                    GPIO.output(P0, False)
                    GPIO.output(P1, False)
                
            except serialutil.SerialException:
                logging.warning('CONNECTION FAILED, TRYING AGAIN')
                
class CardReader:
    def __init__(self, calibrate=False, path=None, deck=None):
        # Event that should trigger when camera has finished taking a picture
        snapped = threading.Event()
        # Thread will take pictures of the card and trigger the snapped event
        kaleb = CardPhotographer(snapped)
        kaleb.start()

        # Thread will process the images Kaleb took when the snapped event triggers it
        preppy = ImageProcessor(kaleb,snapped)
        preppy.start()

        # Thread will constantly poll the pins of the Pi for input and trigger the ready flag when it receives input, signifying that a new card has been pushed out
        ear = PCBListener(kaleb)
        ear.start()

        # Thead will set pin when snapped event is triggered from Kaleb the photographer
        mouth = PCBTalker(snapped)
        mouth.start()

        kelloggs = LuckyCharms()
        kelloggs.start()
        
if __name__=='__main__':
    cr = CardReader()
