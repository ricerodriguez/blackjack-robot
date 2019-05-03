import numpy as np
import sys, os
import math
import random

curr_path = os.path.dirname(__file__)
sys.path.append(curr_path.replace('app','card_reader'))

import CARD_DEFS
from PIL import Image

GENERAL_DECK = CARD_DEFS.GENERAL_DECK
CARD_VALUES = CARD_DEFS.CARD_VALUES

class PlayerHand:
    def __init__(self, card, player='Jack',card_size='medium'):
        self.__card_size = card_size
        self.__deck_01()

        self.hand_pic = Image.new('RGBA',(600,300),(205,38,38,255)) # 1980/5 x 1080/5
        self.player_name = player
        self.hand = [card]

    def is_valid_draw(self,draw):
        if (draw <= 51):
            return True
        else:
            return False

    def add_card(self,draw):
        if (self.is_valid_draw(draw)):
            card = GENERAL_DECK[draw]
            self.hand.append(card)
            self.update_images()

    def del_card(self,card='none',pos=-1):
        if ((pos == -1) and card == 'none'):
            self.hand.pop()
        elif (card == 'none'):
            self.hand.pop(pos)
        else:
            self.hand.remove(card)

    def clear_hand(self):
        self.hand.clear()
        self.pillows.clear()
        self.img_paths.clear()

    def update_images(self):
        self.img_paths = []
        
        for card in self.hand:
            path = self.deck.get(card)
            self.img_paths.append(path)
        
        for i,path in enumerate(self.img_paths):
            image = Image.open(path)
            if (i == 0):
                self.pillows = [image]
            else:
                self.pillows.append(image)

        self.update_hand_pic()

    def update_hand_pic(self):
        canvas = Image.new('RGBA',(600,300),(205,38,38,0))
        card_w,card_h = self.pillows[0].size
        card_canvas = Image.new('RGBA',(10*card_w,6*card_h),(205,38,38,0))

        # card_canvas.save('cardcanvas.png')

        angles = [0,90,45,30,15,0,-15]
        upper_lcorners = [(406,83),(368,25),(326,24),(236,28),(182,79),(177,166)]
        lower_rcorners = [(571,235),(518,194),(429,162),(389,194),(347,232),(317,269)]

        for i,img in enumerate(self.pillows):
            working = self.pillows[i]
            
            # working.save('00working{}.png'.format(i))
            
            working = working.rotate(90,expand=True)
            working = self.crop_img(working)

            # working.save('01working{}.png'.format(i))
            
            ctr_can_x = int(5*card_w - (card_h/2))
            ctr_can_y = int(3*card_h - (card_w/2))
            card_canvas.paste(working,(ctr_can_x, ctr_can_y),working)

            # card_canvas.save('02cardcanvas{}.png'.format(i))
            
            btm_ctr = (ctr_can_x-100,2*card_h+100)
            rotated = card_canvas.rotate(angle=30*(i+1),center=btm_ctr,expand=False)
            rotated = self.crop_img(rotated)

            # rotated.save('03rotated{}.png'.format(i))
            
            x = int(canvas.size[0]/2 - rotated.size[0]/2)
            y = int(canvas.size[1]/2 - rotated.size[1]/2)
            
            canvas.paste(rotated,upper_lcorners[i],rotated)

            # canvas.save('04canvas{}.png'.format(i))

        def crop(im):
            im.load()
            imSize = im.size
            imBox = im.getbbox()
            imComps = im.split()

            rgbIm = Image.new('RGB',imSize,(0,0,0))
            rgbIm.paste(im,mask=imComps[3])
            cropbox = rgbIm.getbbox()

            if (imBox != cropbox):
                crop=im.crop(cropbox)
                return crop
            
        canvas = crop(canvas)
        angle_offset = angles[len(self.pillows)]
        self.hand_pic = canvas.rotate(angle_offset,expand=True)
        self.hand_pic.save('{}_hand.png'.format(self.player_name))

    def crop_img(self,img):
        box = img.getbbox()
        return img.crop(box)
        
    @property
    def deck(self):
        return self.__deck_01()

    @property
    def card_size(self):
        return self.__card_size

    @card_size.setter
    def card_size(self,size):
        self.__card_size = size
        deck = self.deck
        self.update_images()

    def __deck_01(self):
        deck = {
            "Clubs Ace": "resources/deck_01/{}/Clubs_1.png".format(self.__card_size),
            "Clubs 2": "resources/deck_01/{}/Clubs_2.png".format(self.__card_size),
            "Clubs 3": "resources/deck_01/{}/Clubs_3.png".format(self.__card_size),
            "Clubs 4": "resources/deck_01/{}/Clubs_4.png".format(self.__card_size),
            "Clubs 5": "resources/deck_01/{}/Clubs_5.png".format(self.__card_size),
            "Clubs 6": "resources/deck_01/{}/Clubs_6.png".format(self.__card_size),
            "Clubs 7": "resources/deck_01/{}/Clubs_7.png".format(self.__card_size),
            "Clubs 8": "resources/deck_01/{}/Clubs_8.png".format(self.__card_size),
            "Clubs 9": "resources/deck_01/{}/Clubs_9.png".format(self.__card_size),
            "Clubs 10": "resources/deck_01/{}/Clubs_10.png".format(self.__card_size),
            "Clubs Jack": "resources/deck_01/{}/Clubs_11.png".format(self.__card_size),
            "Clubs Queen": "resources/deck_01/{}/Clubs_12.png".format(self.__card_size),
            "Clubs King": "resources/deck_01/{}/Clubs_13.png".format(self.__card_size),
            "Diamonds Ace": "resources/deck_01/{}/Diamond_1.png".format(self.__card_size),
            "Diamonds 2": "resources/deck_01/{}/Diamond_2.png".format(self.__card_size),
            "Diamonds 3": "resources/deck_01/{}/Diamond_3.png".format(self.__card_size),
            "Diamonds 4": "resources/deck_01/{}/Diamond_4.png".format(self.__card_size),
            "Diamonds 5": "resources/deck_01/{}/Diamond_5.png".format(self.__card_size),
            "Diamonds 6": "resources/deck_01/{}/Diamond_6.png".format(self.__card_size),
            "Diamonds 7": "resources/deck_01/{}/Diamond_7.png".format(self.__card_size),
            "Diamonds 8": "resources/deck_01/{}/Diamond_8.png".format(self.__card_size),
            "Diamonds 9": "resources/deck_01/{}/Diamond_9.png".format(self.__card_size),
            "Diamonds 10": "resources/deck_01/{}/Diamond_10.png".format(self.__card_size),
            "Diamonds Jack": "resources/deck_01/{}/Diamond_11.png".format(self.__card_size),
            "Diamonds Queen": "resources/deck_01/{}/Diamond_12.png".format(self.__card_size),
            "Diamonds King": "resources/deck_01/{}/Diamond_13.png".format(self.__card_size),
            "Hearts Ace": "resources/deck_01/{}/Hearts_1.png".format(self.__card_size),
            "Hearts 2": "resources/deck_01/{}/Hearts_2.png".format(self.__card_size),
            "Hearts 3": "resources/deck_01/{}/Hearts_3.png".format(self.__card_size),
            "Hearts 4": "resources/deck_01/{}/Hearts_4.png".format(self.__card_size),
            "Hearts 5": "resources/deck_01/{}/Hearts_5.png".format(self.__card_size),
            "Hearts 6": "resources/deck_01/{}/Hearts_6.png".format(self.__card_size),
            "Hearts 7": "resources/deck_01/{}/Hearts_7.png".format(self.__card_size),
            "Hearts 8": "resources/deck_01/{}/Hearts_8.png".format(self.__card_size),
            "Hearts 9": "resources/deck_01/{}/Hearts_9.png".format(self.__card_size),
            "Hearts 10": "resources/deck_01/{}/Hearts_10.png".format(self.__card_size),
            "Hearts Jack": "resources/deck_01/{}/Hearts_11.png".format(self.__card_size),
            "Hearts Queen": "resources/deck_01/{}/Hearts_12.png".format(self.__card_size),
            "Hearts King": "resources/deck_01/{}/Hearts_13.png".format(self.__card_size),
            "Spades Ace": "resources/deck_01/{}/Spades_1.png".format(self.__card_size),
            "Spades 2": "resources/deck_01/{}/Spades_2.png".format(self.__card_size),
            "Spades 3": "resources/deck_01/{}/Spades_3.png".format(self.__card_size),
            "Spades 4": "resources/deck_01/{}/Spades_4.png".format(self.__card_size),
            "Spades 5": "resources/deck_01/{}/Spades_5.png".format(self.__card_size),
            "Spades 6": "resources/deck_01/{}/Spades_6.png".format(self.__card_size),
            "Spades 7": "resources/deck_01/{}/Spades_7.png".format(self.__card_size),
            "Spades 8": "resources/deck_01/{}/Spades_8.png".format(self.__card_size),
            "Spades 9": "resources/deck_01/{}/Spades_9.png".format(self.__card_size),
            "Spades 10": "resources/deck_01/{}/Spades_10.png".format(self.__card_size),
            "Spades Jack": "resources/deck_01/{}/Spades_11.png".format(self.__card_size),
            "Spades Queen": "resources/deck_01/{}/Spades_12.png".format(self.__card_size),
            "Spades King": "resources/deck_01/{}/Spades_13.png".format(self.__card_size)
            }
        return deck
        
class Player:
    discard_pile = []
    
    def __init__(self, name='Jack',payout=0,bet=0,deck=1):
        self.name = name
        self.payout = payout
        self.bet = bet
        self.deck = deck
        self.rematch(name)
        # self.score = 0
        # self.num_cards = 0
        # self.aces = 0

        # # Deal initial cards
        # draw = random.randint(0,51)
        # self.update_score(draw)
        # self.discard_pile.append(draw)
        # card = GENERAL_DECK[draw]

        # self.hand = PlayerHand(card,name)
        # self.num_cards += 1
    
        # self.hit()

    def rematch(self,name=None):            
        self.score = 0
        self.num_cards = 0
        self.aces = 0
        self.temp_score = 0

        # Deal initial cards
        draw = random.randint(0,51)
        self.update_score(draw)
        self.discard_pile.append(draw)
        card = GENERAL_DECK[draw]

        try:
            del self.hand
        except AttributeError:
            pass
        finally:
            self.hand = PlayerHand(card,name)

        self.num_cards += 1
    
        self.hit()
        

    def in_deck(self,draw):
        for card in self.discard_pile:
            if (card == draw):
                return False
            else:
                continue
            
        return True

    def busted(self):
        if self.aces <= 0:
            if (self.score > 21):
                return True
            else:
                return False
        else:
            max_score = self.aces * 10 + self.score
            min_score = self.aces + self.score
            all_scores = []
            for i in range(self.aces):
                tmp = self.score + i*10 + (self.aces - 1)
                if ((tmp > 21) and (prev is None)):
                    return True
                elif (tmp <= 21):
                    prev = tmp
                    continue
                else:
                    self.score = tmp
                    return False
        
    def hit(self):
        draw = random.randint(0,51)
        if (self.in_deck(draw)):
            self.discard_pile.append(draw)
            card = GENERAL_DECK[draw]
            self.hand.add_card(draw)
            self.num_cards += 1
            self.update_score(draw)
            return card
        else:
            self.hit()

    def update_score(self,draw):
        global CARD_VALUES
        if (draw > 47):
            if (self.score + 10 < 21):
                self.score += 10
                self.aces += 1
            else:
                self.score += 1
                self.aces += 1
        #     all_scores = []
        #     print('aces: ',self.aces)
        #     if self.aces > 0:
        #         for i in range(self.aces):
        #             i+=1
        #             tens = abs(range(self.aces) - i)
        #             tmpscore = self.score + i + 10*tens
        #             if (tmpscore > 21):
        #                 print(tmpscore)
        #                 continue
        #             else:
        #                 print(tmpscore)
        #                 all_scores.append(tmpscore)
        #         self.score = max(all_scores)
        #         self.aces += 1
        #     else:
                
                
                    
            
                
        #     # for i in range(self.aces):
        #     #     tmp = self.score + i*10 + (self.aces - 1)
        #     #     if ((tmp > 21) and (prev is None)):
        #     #         self.score += 1
        #     #     elif (tmp <= 21):
        #     #         prev = tmp
        #     #         continue
        #     #     else:
        #     #         self.score = tmp                    
            
        else:
            self.score += CARD_VALUES[draw]
            # for i in range(self.aces):
            #     tmp = self.score + i*10 + (self.aces - 1)
            #     if ((tmp > 21) and (prev is None)):
            #         self.score += 1
            #     elif (tmp <= 21):
            #         prev = tmp
            #         continue
            #     else:
            #         self.score = tmp                 
