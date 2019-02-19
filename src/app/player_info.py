import numpy as np
import random
from PIL import Image
# from resource_loader import ResourceLoader

GENERAL_DECK = [
   "Clubs 2",
   "Clubs 3",
   "Clubs 4",
   "Clubs 5",
   "Clubs 6",
   "Clubs 7",
   "Clubs 8",
   "Clubs 9",
   "Clubs 10",
    "Clubs Jack",
    "Clubs Queen",
    "Clubs King",
    "Diamonds 2",
    "Diamonds 3",
    "Diamonds 4",
    "Diamonds 5",
    "Diamonds 6",
    "Diamonds 7",
    "Diamonds 8",
    "Diamonds 9",
    "Diamonds 10",
    "Diamonds Jack",
    "Diamonds Queen",
    "Diamonds King",
    "Hearts 2",
    "Hearts 3",
    "Hearts 4",
    "Hearts 5",
    "Hearts 6",
    "Hearts 7",
    "Hearts 8",
    "Hearts 9",
    "Hearts 10",
    "Hearts Jack",
    "Hearts Queen",
    "Hearts King",
    "Spades 2",
    "Spades 3",
    "Spades 4",
    "Spades 5",
    "Spades 6",
    "Spades 7",
    "Spades 8",
    "Spades 9",
    "Spades 10",
    "Spades Jack",
    "Spades Queen",
    "Spades King",
    "Clubs Ace",
    "Spades Ace",
    "Hearts Ace",
    "Diamonds Ace"
]

CARD_VALUES = [
   2,
   3,
   4,
   5,
   6,
   7,
   8,
   9,
   10,
    10,
    10,
    10,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    10,
    10,
    10,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    10,
    10,
    10,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    10,
    10,
    10
]


class PlayerHand:
    def __init__(self, card, deck=2, player='Jack',card_size='medium'):
        self.__card_size = card_size
        which_deck = {
            1: self.__deck_01,
            2: self.__deck_02,
            3: self.__deck_03
        }
        get_deck = which_deck.get(deck,lambda:__deck_01)
        get_deck()

        self.deck_pick = deck
        self.hand_pic = Image.new('RGBA',(396,216),(51,255,51,255)) # 1980/5 x 1080/5
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
        img_w, img_h = self.hand_pic.size
        canvas = Image.new('RGBA',(img_w,img_h),(51,255,51,255))
        rotate = True
        angles = []
        offset = []
        if (len(self.pillows) == 2):
            angles = [30, 330]
            offset = [2/6,4/6]
        elif (len(self.pillows) == 3):
            angles = [60, 0, 300]
            offset = [2/6,3/6,4/6]
        elif (len(self.pillows) == 4):
            angles = [45, 15, 345, 315]
            offset = [1/5,2/5,3/5,4/5]
        elif (len(self.pillows) == 5):
            angles = [60, 30, 0, 330, 300]
            offset = [1/6,2/6,3/6,4/6,5/6]
        elif (len(self.pillows) == 6):
            angles = [90, 60, 30, 330, 300, 270]
            offset = [1/6,2/6,3/6,4/6,5/6,6/6]
        else:
            rotate = False

        for i,img in enumerate(self.pillows):
            if (rotate):
                working = self.pillows[i]
                rotated = working.rotate(angles[i],expand=True)
                half_w = int((canvas.size[0]-rotated.size[0])/2)
                half_w = int((half_w + 2*offset[i]*half_w)/2+half_w/4)
                half_h = int((canvas.size[1]-rotated.size[1])/2)
                # rotated.show()
                canvas.paste(rotated,(half_w, half_h),rotated)

            else: 
                working = self.pillows[i]
                canvas.paste(working,(half_w, half_h))

        pixdata = canvas.load()
        for x in range(canvas.size[0]):
            for y in range(canvas.size[1]):
                if pixdata[x, y] == (51, 255, 51, 255):
                    pixdata[x, y] = (0, 0, 0, 0)

        canvasBox = canvas.getbbox()
        self.hand_pic = canvas.crop(canvasBox)
        self.hand_pic.save('{}_hand.png'.format(self.player_name))

    @property
    def deck(self):
        which_deck = {
            1: self.__deck_01,
            2: self.__deck_02,
            3: self.__deck_03
        }
        get_deck = which_deck.get(self.deck_pick,lambda:__deck_01)
        return get_deck()

    @deck.setter
    def deck(self,pick):
        self.deck_pick = pick
        which_deck = {
            1: self.__deck_01,
            2: self.__deck_02,
            3: self.__deck_03
        }
        get_deck = which_deck.get(pick,lambda:__deck_01)
        self.deck = get_deck()

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
            "Clubs Ace": "Cards/deck_01/{}/Clubs_1.png".format(self.__card_size),
            "Clubs 2": "Cards/deck_01/{}/Clubs_2.png".format(self.__card_size),
            "Clubs 3": "Cards/deck_01/{}/Clubs_3.png".format(self.__card_size),
            "Clubs 4": "Cards/deck_01/{}/Clubs_4.png".format(self.__card_size),
            "Clubs 5": "Cards/deck_01/{}/Clubs_5.png".format(self.__card_size),
            "Clubs 6": "Cards/deck_01/{}/Clubs_6.png".format(self.__card_size),
            "Clubs 7": "Cards/deck_01/{}/Clubs_7.png".format(self.__card_size),
            "Clubs 8": "Cards/deck_01/{}/Clubs_8.png".format(self.__card_size),
            "Clubs 9": "Cards/deck_01/{}/Clubs_9.png".format(self.__card_size),
            "Clubs 10": "Cards/deck_01/{}/Clubs_10.png".format(self.__card_size),
            "Clubs Jack": "Cards/deck_01/{}/Clubs_11.png".format(self.__card_size),
            "Clubs Queen": "Cards/deck_01/{}/Clubs_12.png".format(self.__card_size),
            "Clubs King": "Cards/deck_01/{}/Clubs_13.png".format(self.__card_size),
            "Diamonds Ace": "Cards/deck_01/{}/Diamond_1.png".format(self.__card_size),
            "Diamonds 2": "Cards/deck_01/{}/Diamond_2.png".format(self.__card_size),
            "Diamonds 3": "Cards/deck_01/{}/Diamond_3.png".format(self.__card_size),
            "Diamonds 4": "Cards/deck_01/{}/Diamond_4.png".format(self.__card_size),
            "Diamonds 5": "Cards/deck_01/{}/Diamond_5.png".format(self.__card_size),
            "Diamonds 6": "Cards/deck_01/{}/Diamond_6.png".format(self.__card_size),
            "Diamonds 7": "Cards/deck_01/{}/Diamond_7.png".format(self.__card_size),
            "Diamonds 8": "Cards/deck_01/{}/Diamond_8.png".format(self.__card_size),
            "Diamonds 9": "Cards/deck_01/{}/Diamond_9.png".format(self.__card_size),
            "Diamonds 10": "Cards/deck_01/{}/Diamond_10.png".format(self.__card_size),
            "Diamonds Jack": "Cards/deck_01/{}/Diamond_11.png".format(self.__card_size),
            "Diamonds Queen": "Cards/deck_01/{}/Diamond_12.png".format(self.__card_size),
            "Diamonds King": "Cards/deck_01/{}/Diamond_13.png".format(self.__card_size),
            "Hearts Ace": "Cards/deck_01/{}/Hearts_1.png".format(self.__card_size),
            "Hearts 2": "Cards/deck_01/{}/Hearts_2.png".format(self.__card_size),
            "Hearts 3": "Cards/deck_01/{}/Hearts_3.png".format(self.__card_size),
            "Hearts 4": "Cards/deck_01/{}/Hearts_4.png".format(self.__card_size),
            "Hearts 5": "Cards/deck_01/{}/Hearts_5.png".format(self.__card_size),
            "Hearts 6": "Cards/deck_01/{}/Hearts_6.png".format(self.__card_size),
            "Hearts 7": "Cards/deck_01/{}/Hearts_7.png".format(self.__card_size),
            "Hearts 8": "Cards/deck_01/{}/Hearts_8.png".format(self.__card_size),
            "Hearts 9": "Cards/deck_01/{}/Hearts_9.png".format(self.__card_size),
            "Hearts 10": "Cards/deck_01/{}/Hearts_10.png".format(self.__card_size),
            "Hearts Jack": "Cards/deck_01/{}/Hearts_11.png".format(self.__card_size),
            "Hearts Queen": "Cards/deck_01/{}/Hearts_12.png".format(self.__card_size),
            "Hearts King": "Cards/deck_01/{}/Hearts_13.png".format(self.__card_size),
            "Spades Ace": "Cards/deck_01/{}/Spades_1.png".format(self.__card_size),
            "Spades 2": "Cards/deck_01/{}/Spades_2.png".format(self.__card_size),
            "Spades 3": "Cards/deck_01/{}/Spades_3.png".format(self.__card_size),
            "Spades 4": "Cards/deck_01/{}/Spades_4.png".format(self.__card_size),
            "Spades 5": "Cards/deck_01/{}/Spades_5.png".format(self.__card_size),
            "Spades 6": "Cards/deck_01/{}/Spades_6.png".format(self.__card_size),
            "Spades 7": "Cards/deck_01/{}/Spades_7.png".format(self.__card_size),
            "Spades 8": "Cards/deck_01/{}/Spades_8.png".format(self.__card_size),
            "Spades 9": "Cards/deck_01/{}/Spades_9.png".format(self.__card_size),
            "Spades 10": "Cards/deck_01/{}/Spades_10.png".format(self.__card_size),
            "Spades Jack": "Cards/deck_01/{}/Spades_11.png".format(self.__card_size),
            "Spades Queen": "Cards/deck_01/{}/Spades_12.png".format(self.__card_size),
            "Spades King": "Cards/deck_01/{}/Spades_13.png".format(self.__card_size)
            }
        return deck

    def __deck_02(self):
        deck = {
            "Clubs Ace": "Cards/deck_02/{}/AC.png".format(self.__card_size),
            "Clubs 2": "Cards/deck_02/{}/2C.png".format(self.__card_size),
            "Clubs 3": "Cards/deck_02/{}/3C.png".format(self.__card_size),
            "Clubs 4": "Cards/deck_02/{}/4C.png".format(self.__card_size),
            "Clubs 5": "Cards/deck_02/{}/5C.png".format(self.__card_size),
            "Clubs 6": "Cards/deck_02/{}/6C.png".format(self.__card_size),
            "Clubs 7": "Cards/deck_02/{}/7C.png".format(self.__card_size),
            "Clubs 8": "Cards/deck_02/{}/8C.png".format(self.__card_size),
            "Clubs 9": "Cards/deck_02/{}/9C.png".format(self.__card_size),
            "Clubs 10": "Cards/deck_02/{}/10C.png".format(self.__card_size),
            "Clubs Jack": "Cards/deck_02/{}/JC.png".format(self.__card_size),
            "Clubs Queen": "Cards/deck_02/{}/QC.png".format(self.__card_size),
            "Clubs King": "Cards/deck_02/{}/KC.png".format(self.__card_size),
            "Diamonds Ace": "Cards/deck_02/{}/AD.png".format(self.__card_size),
            "Diamonds 2": "Cards/deck_02/{}/2D.png".format(self.__card_size),
            "Diamonds 3": "Cards/deck_02/{}/3D.png".format(self.__card_size),
            "Diamonds 4": "Cards/deck_02/{}/4D.png".format(self.__card_size),
            "Diamonds 5": "Cards/deck_02/{}/5D.png".format(self.__card_size),
            "Diamonds 6": "Cards/deck_02/{}/6D.png".format(self.__card_size),
            "Diamonds 7": "Cards/deck_02/{}/7D.png".format(self.__card_size),
            "Diamonds 8": "Cards/deck_02/{}/8D.png".format(self.__card_size),
            "Diamonds 9": "Cards/deck_02/{}/9D.png".format(self.__card_size),
            "Diamonds 10": "Cards/deck_02/{}/10D.png".format(self.__card_size),
            "Diamonds Jack": "Cards/deck_02/{}/JD.png".format(self.__card_size),
            "Diamonds Queen": "Cards/deck_02/{}/QD.png".format(self.__card_size),
            "Diamonds King": "Cards/deck_02/{}/KD.png".format(self.__card_size),
            "Spades Ace": "Cards/deck_02/{}/AS.png".format(self.__card_size),
            "Spades 2": "Cards/deck_02/{}/2S.png".format(self.__card_size),
            "Spades 3": "Cards/deck_02/{}/3S.png".format(self.__card_size),
            "Spades 4": "Cards/deck_02/{}/4S.png".format(self.__card_size),
            "Spades 5": "Cards/deck_02/{}/5S.png".format(self.__card_size),
            "Spades 6": "Cards/deck_02/{}/6S.png".format(self.__card_size),
            "Spades 7": "Cards/deck_02/{}/7S.png".format(self.__card_size),
            "Spades 8": "Cards/deck_02/{}/8S.png".format(self.__card_size),
            "Spades 9": "Cards/deck_02/{}/9S.png".format(self.__card_size),
            "Spades 10": "Cards/deck_02/{}/10S.png".format(self.__card_size),
            "Spades Jack": "Cards/deck_02/{}/JS.png".format(self.__card_size),
            "Spades Queen": "Cards/deck_02/{}/QS.png".format(self.__card_size),
            "Spades King": "Cards/deck_02/{}/KS.png".format(self.__card_size),
            "Hearts Ace": "Cards/deck_02/{}/AH.png".format(self.__card_size),
            "Hearts 2": "Cards/deck_02/{}/2H.png".format(self.__card_size),
            "Hearts 3": "Cards/deck_02/{}/3H.png".format(self.__card_size),
            "Hearts 4": "Cards/deck_02/{}/4H.png".format(self.__card_size),
            "Hearts 5": "Cards/deck_02/{}/5H.png".format(self.__card_size),
            "Hearts 6": "Cards/deck_02/{}/6H.png".format(self.__card_size),
            "Hearts 7": "Cards/deck_02/{}/7H.png".format(self.__card_size),
            "Hearts 8": "Cards/deck_02/{}/8H.png".format(self.__card_size),
            "Hearts 9": "Cards/deck_02/{}/9H.png".format(self.__card_size),
            "Hearts 10": "Cards/deck_02/{}/10H.png".format(self.__card_size),
            "Hearts Jack": "Cards/deck_02/{}/JH.png".format(self.__card_size),
            "Hearts Queen": "Cards/deck_02/{}/QH.png".format(self.__card_size),
            "Hearts King": "Cards/deck_02/{}/KH.png".format(self.__card_size)
            }
        return deck

    def __deck_03(self):
        deck = {
            "Clubs Ace": "Cards/deck_03/{}/ace_of_clubs.png".format(self.__card_size),
            "Clubs 2": "Cards/deck_03/{}/2_of_clubs.png".format(self.__card_size),
            "Clubs 3": "Cards/deck_03/{}/3_of_clubs.png".format(self.__card_size),
            "Clubs 4": "Cards/deck_03/{}/4_of_clubs.png".format(self.__card_size),
            "Clubs 5": "Cards/deck_03/{}/5_of_clubs.png".format(self.__card_size),
            "Clubs 6": "Cards/deck_03/{}/6_of_clubs.png".format(self.__card_size),
            "Clubs 7": "Cards/deck_03/{}/7_of_clubs.png".format(self.__card_size),
            "Clubs 8": "Cards/deck_03/{}/8_of_clubs.png".format(self.__card_size),
            "Clubs 9": "Cards/deck_03/{}/9_of_clubs.png".format(self.__card_size),
            "Clubs 10": "Cards/deck_03/{}/10_of_clubs.png".format(self.__card_size),
            "Clubs Jack": "Cards/deck_03/{}/jack_of_clubs.png".format(self.__card_size),
            "Clubs Queen": "Cards/deck_03/{}/queen_of_clubs.png".format(self.__card_size),
            "Clubs King": "Cards/deck_03/{}/king_of_clubs.png".format(self.__card_size),
            "Diamonds Ace": "Cards/deck_03/{}/ace_of_diamonds.png".format(self.__card_size),
            "Diamonds 2": "Cards/deck_03/{}/2_of_diamonds.png".format(self.__card_size),
            "Diamonds 3": "Cards/deck_03/{}/3_of_diamonds.png".format(self.__card_size),
            "Diamonds 4": "Cards/deck_03/{}/4_of_diamonds.png".format(self.__card_size),
            "Diamonds 5": "Cards/deck_03/{}/5_of_diamonds.png".format(self.__card_size),
            "Diamonds 6": "Cards/deck_03/{}/6_of_diamonds.png".format(self.__card_size),
            "Diamonds 7": "Cards/deck_03/{}/7_of_diamonds.png".format(self.__card_size),
            "Diamonds 8": "Cards/deck_03/{}/8_of_diamonds.png".format(self.__card_size),
            "Diamonds 9": "Cards/deck_03/{}/9_of_diamonds.png".format(self.__card_size),
            "Diamonds 10": "Cards/deck_03/{}/10_of_diamonds.png".format(self.__card_size),
            "Diamonds Jack": "Cards/deck_03/{}/jack_of_diamonds.png".format(self.__card_size),
            "Diamonds Queen": "Cards/deck_03/{}/queen_of_diamonds.png".format(self.__card_size),
            "Diamonds King": "Cards/deck_03/{}/king_of_diamonds.png".format(self.__card_size),
            "Spades Ace": "Cards/deck_03/{}/ace_of_spades.png".format(self.__card_size),
            "Spades 2": "Cards/deck_03/{}/2_of_spades.png".format(self.__card_size),
            "Spades 3": "Cards/deck_03/{}/3_of_spades.png".format(self.__card_size),
            "Spades 4": "Cards/deck_03/{}/4_of_spades.png".format(self.__card_size),
            "Spades 5": "Cards/deck_03/{}/5_of_spades.png".format(self.__card_size),
            "Spades 6": "Cards/deck_03/{}/6_of_spades.png".format(self.__card_size),
            "Spades 7": "Cards/deck_03/{}/7_of_spades.png".format(self.__card_size),
            "Spades 8": "Cards/deck_03/{}/8_of_spades.png".format(self.__card_size),
            "Spades 9": "Cards/deck_03/{}/9_of_spades.png".format(self.__card_size),
            "Spades 10": "Cards/deck_03/{}/10_of_spades.png".format(self.__card_size),
            "Spades Jack": "Cards/deck_03/{}/jack_of_spades.png".format(self.__card_size),
            "Spades Queen": "Cards/deck_03/{}/queen_of_spades.png".format(self.__card_size),
            "Spades King": "Cards/deck_03/{}/king_of_spades.png".format(self.__card_size),
            "Hearts Ace": "Cards/deck_03/{}/ace_of_hearts.png".format(self.__card_size),
            "Hearts 2": "Cards/deck_03/{}/2_of_hearts.png".format(self.__card_size),
            "Hearts 3": "Cards/deck_03/{}/3_of_hearts.png".format(self.__card_size),
            "Hearts 4": "Cards/deck_03/{}/4_of_hearts.png".format(self.__card_size),
            "Hearts 5": "Cards/deck_03/{}/5_of_hearts.png".format(self.__card_size),
            "Hearts 6": "Cards/deck_03/{}/6_of_hearts.png".format(self.__card_size),
            "Hearts 7": "Cards/deck_03/{}/7_of_hearts.png".format(self.__card_size),
            "Hearts 8": "Cards/deck_03/{}/8_of_hearts.png".format(self.__card_size),
            "Hearts 9": "Cards/deck_03/{}/9_of_hearts.png".format(self.__card_size),
            "Hearts 10": "Cards/deck_03/{}/10_of_hearts.png".format(self.__card_size),
            "Hearts Jack": "Cards/deck_03/{}/jack_of_hearts.png".format(self.__card_size),
            "Hearts Queen": "Cards/deck_03/{}/queen_of_hearts.png".format(self.__card_size),
            "Hearts King": "Cards/deck_03/{}/king_of_hearts.png".format(self.__card_size)
        }
        return deck

        
class Player:
    def __init__(self, name='Jack',payout=0,bet=0,deck=1):
        self.name = name
        self.payout = payout
        self.bet = bet
        self.score = 0
        self.deck = deck
        self.num_cards = 0
        self.has_ace = False

        # Deal initial cards
        draw = random.randint(0,51)
        self.update_score(draw)
        self.discard_pile = [draw]
        card = GENERAL_DECK[draw]

        self.hand = PlayerHand(card,deck,name)
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
        if (score > 21):
            return True
        else:
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
                self.has_ace = True
            else:
                self.score += 1
        else:
            self.score += CARD_VALUES[draw]
