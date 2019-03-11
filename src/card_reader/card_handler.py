# import cv2 as cv
# import sys
# import numpy
import threading
import os
import time
import logging

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
        
        # t1 = threading.Thread(target=calibrate_cards)
        # t1.start()

        # # Thread is used to simulate the MSP430 sending a signal that
        # # it has moved the servo for the next card.
        # t2 = threading.Thread(target=next_card)
        # t2.start()

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
            self.path = os.path.join(path, 'data', 'calib_cards', deck)
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

 
            # If the card is ready
            if self.ready.is_set():
                # Clear the flag
                self.ready.clear()
                # Make sure there are no spaces in the file name to
                # avoid confusion
                card_name = card.replace(' ', '_')
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
#        else:
#            pass
        
class CardReader:
    def __init__(self, path=None, deck=None):
        snapped = threading.Event()
        kaleb = Calibrator(snapped, path, deck)
        kaleb.start()
        
        thr = Tester(kaleb, snapped)
        thr.start()

#        thr = threading.Thread(target=self.next_card)
#        thr.start()
        
#        print('Calibrating cards, please wait...')

#        kaleb.join()
#        thr.join()

    # Placeholder function to simulate the signal the MSP430 will send
    # to the Pi after it has finished moving the servo
#    def next_card(self):
        
if __name__=='__main__':
    cr = CardReader()
        
    #     self._calibrated_cards = []
    #     self._calibrated_decks = []

    # @property
    # def calibrated_cards(self):
    #     return self._calibrated_cards

    # @calibrated_cards.setter
    # def calibrated_cards(self, card):
    #     if not (len(self._calibrated_cards) == 0):
    #         self._calibrated_cards.append(card)
    #     else:
    #         self._calibrated_cards = [card]
