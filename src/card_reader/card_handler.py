import cv2 as cv
import numpy
import threading
import os
import time
import logging
# import sys


# Local package definition for card macros
import CARD_DEFS

# Image and camera package imports
from PIL import Image
from picamera import PiCamera

# Global variables for things that will be used throughout
cam = PiCamera()
GEN_DECK = CARD_DEFS.GENERAL_DECK

#logging.basicConfig(filename=os.path.join(str(os.path.dirname(__file__)), 'log', 'calibrator.log'), level=logging.INFO)
logging.basicConfig(level=logging.INFO)
class Calibrator(threading.Thread):
    def __init__(self, trigger=None, path=None, deck=None):
        self.path = path
        self.deck = deck
        self._card_map = {}
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
            filename = os.path.join(self.path, card_name)
            
            # Snap the picture
            cam.capture(filename)
            
            # Add the file name to the map to keep track
            self._card_map[card] = filename
            # Set the flag that the picture has been taken
            self.snapped.set()
            logging.info('CL: Set snapped event!')

        # Exited the for-loop, so all cards have been snapped.
        self.img_prep()

        
    def img_prep(self):
        # For each card in the folder
        card_imgs = os.listdir(self.path)
        # Credit to OpenCV's tutorial: 'Creating Bounding boxes and
        # circles for contours'

        for img in card_imgs:
            # Read in the card
            card = cv.imread(img)
            # Use Canny algorithm to find edges
            can_out = cv.Canny(card, 100, 200)
            # Convert to gray and blur it
            card_g = cv.cvtColor(card, cv.COLOR_BGR2GRAY)
            card_g = cv.blur(card, (3,3))
            # Find contours, save them to vector
            contours, _ = cv.findContours(can_out, cv.RETR_TREE,
                                          cv.CHAIN_APPROX_SIMPLE)
            # Approximate contours to polygons + get bounding
            # rects/circles
            cont_poly = [None]*len(contours)
            bound_box = [None]*len(contours)

            # For each of the contours found, approximate a polygon
            # from the contour, then draw a bounding box for that
            # polygon            
            for i,c in enumerate(contours):
                cont_poly[i] = cv.approxPolyDP(c,3,True)
                bound_box[i] = cv.boundingRect(cont_poly[i])

            # Find the biggest bounding box
            areas = []
            for box in bound_box:
                areas.append(box[2]*box[3])
                
            big_box = bound_box.index(max(bound_box))

            x, y, w, h = big_box
            roi = card[y:y+h, x:x+w]
            cv.imwrite(img, roi)
            
        
         
class Tester(threading.Thread):
    def __init__(self, cls, trigger):
        threading.Thread.__init__(self)
        self.kaleb = cls
        self.snapped = trigger
        
    def run(self):
        while True:
            logging.info('TESTER: Waiting for Pi to finish snapping!')
            self.snapped.wait()
            if self.snapped.is_set():
                logging.info('TESTER: It\'s done! Clearing out ready flag...')            
                self.kaleb.ready.clear()
                logging.info('TESTER: Cleared out the ready flag.')
                time.sleep(1)
                self.kaleb.ready.set()
                logging.info('TESTER: Set ready!')
            logging.info('TESTER: EXITED IF')

class CardReader:
    def __init__(self, path=None, deck=None):
        snapped = threading.Event()
        kaleb = Calibrator(snapped, path, deck)
        kaleb.start()
        
        thr = Tester(kaleb, snapped)
        thr.start()
        
if __name__=='__main__':
    cr = CardReader()
