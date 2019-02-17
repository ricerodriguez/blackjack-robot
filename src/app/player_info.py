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
    def __init__(self, card, deck=2, player='Jack'):
        which_deck = {
            1: self.__deck_01,
            2: self.__deck_02,
            3: self.__deck_03
        }
        get_deck = which_deck.get(deck,lambda:__deck_01)
        get_deck()
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
        if (len(self.pillows) == 2):
            angles = [45, 315]
        elif (len(self.pillows) == 3):
            angles = [60, 0, 300]
        elif (len(self.pillows) == 4):
            angles = [45, 15, 345, 315]
        elif (len(self.pillows) == 5):
            angles = [60, 30, 0, 330, 300]
        elif (len(self.pillows) == 6):
            angles = [90, 60, 30, 330, 300, 270]
        else:
            rotate = False


        # offset = [
        #          [0,]]
        # working_canvas = Image.new('RGBA',self.pillows[i].size,(0,0,0,0))
        for i,img in enumerate(self.pillows):
            if (rotate):
                working = self.pillows[i]
                rotated = working.rotate(angles[i],expand=True)
                half_w = int((canvas.size[0]-rotated.size[0])/2)
                half_h = int((canvas.size[1]-rotated.size[1])/2)
                # rotated.show()
                canvas.paste(rotated,(half_w, half_h),rotated)
                canvas.show()
                # pixdata = rotated.load()
                # for y in range(rotated.size[1]):
                #     for x in range(rotated.size[0]):
                #         if pixdata[x, y] == (51, 255, 51, 255):
                #             pixdata[x, y] = (0, 0, 0, 0)


            else: 
                working = self.pillows[i]
                canvas.paste(working,(half_w, half_h))
                       
            # if (len(self.pillows) > 1):
            #     angle = angle + incrementer
            #     working_img = self.pillows[i]
            #     rotated = working_img.rotate(angle,expand=True)
            #     canvas.paste(working_img,(half_w, half_h),working_img)
            #     pixdata = working_img.load()
            #     for y in range(working_img.size[1]):
            #         for x in range(working_img.size[0]):
            #             if pixdata[x, y] == (51, 255, 51, 255):
            #                 pixdata[x, y] = (0, 0, 0, 0)
            #     # canvas.show()
            #     # self.hand_pic.paste(working_img,(half_w, half_h),working_img)
            #     # Image.composite(self.hand_pic,
            # else:
            #     working_img = self.pillows[i]
            #     canvas.paste(working_img,(half_w, half_h),working_img)
            #     pixdata = working_img.load()
            #     for y in range(working_img.size[1]):
            #         for x in range(working_img.size[0]):
            #             if pixdata[x, y] == (51, 255, 51, 255):
            #                 pixdata[x, y] = (0, 0, 0, 0)
        pixdata = canvas.load()
        for x in range(canvas.size[0]):
            for y in range(canvas.size[1]):
                if pixdata[x, y] == (51, 255, 51, 255):
                    pixdata[x, y] = (0, 0, 0, 0)
        canvas.show()
        self.hand_pic = canvas
        self.hand_pic.save('{}_hand.gif'.format(self.player_name),'GIF',transparency=0)
        # self.hand_pic.show()
                    
    def get_count(self):
        return len(self.hand)

    def get_hand(self):
        return self.hand

    def get_deck(self):
        return self.deck

    def __deck_01(self):
        self.deck = {
            "Clubs Ace": "Cards/deck_01/Clubs_1.png",
            "Clubs 2": "Cards/deck_01/Clubs_2.png",
            "Clubs 3": "Cards/deck_01/Clubs_3.png",
            "Clubs 4": "Cards/deck_01/Clubs_4.png",
            "Clubs 5": "Cards/deck_01/Clubs_5.png",
            "Clubs 6": "Cards/deck_01/Clubs_6.png",
            "Clubs 7": "Cards/deck_01/Clubs_7.png",
            "Clubs 8": "Cards/deck_01/Clubs_8.png",
            "Clubs 9": "Cards/deck_01/Clubs_9.png",
            "Clubs 10": "Cards/deck_01/Clubs_10.png",
            "Clubs Jack": "Cards/deck_01/Clubs_11.png",
            "Clubs Queen": "Cards/deck_01/Clubs_12.png",
            "Clubs King": "Cards/deck_01/Clubs_13.png",
            "Diamonds Ace": "Cards/deck_01/Diamond_1.png",
            "Diamonds 2": "Cards/deck_01/Diamond_2.png",
            "Diamonds 3": "Cards/deck_01/Diamond_3.png",
            "Diamonds 4": "Cards/deck_01/Diamond_4.png",
            "Diamonds 5": "Cards/deck_01/Diamond_5.png",
            "Diamonds 6": "Cards/deck_01/Diamond_6.png",
            "Diamonds 7": "Cards/deck_01/Diamond_7.png",
            "Diamonds 8": "Cards/deck_01/Diamond_8.png",
            "Diamonds 9": "Cards/deck_01/Diamond_9.png",
            "Diamonds 10": "Cards/deck_01/Diamond_10.png",
            "Diamonds Jack": "Cards/deck_01/Diamond_11.png",
            "Diamonds Queen": "Cards/deck_01/Diamond_12.png",
            "Diamonds King": "Cards/deck_01/Diamond_13.png",
            "Hearts Ace": "Cards/deck_01/Hearts_1.png",
            "Hearts 2": "Cards/deck_01/Hearts_2.png",
            "Hearts 3": "Cards/deck_01/Hearts_3.png",
            "Hearts 4": "Cards/deck_01/Hearts_4.png",
            "Hearts 5": "Cards/deck_01/Hearts_5.png",
            "Hearts 6": "Cards/deck_01/Hearts_6.png",
            "Hearts 7": "Cards/deck_01/Hearts_7.png",
            "Hearts 8": "Cards/deck_01/Hearts_8.png",
            "Hearts 9": "Cards/deck_01/Hearts_9.png",
            "Hearts 10": "Cards/deck_01/Hearts_10.png",
            "Hearts Jack": "Cards/deck_01/Hearts_11.png",
            "Hearts Queen": "Cards/deck_01/Hearts_12.png",
            "Hearts King": "Cards/deck_01/Hearts_13.png",
            "Spades Ace": "Cards/deck_01/Spades_1.png",
            "Spades 2": "Cards/deck_01/Spades_2.png",
            "Spades 3": "Cards/deck_01/Spades_3.png",
            "Spades 4": "Cards/deck_01/Spades_4.png",
            "Spades 5": "Cards/deck_01/Spades_5.png",
            "Spades 6": "Cards/deck_01/Spades_6.png",
            "Spades 7": "Cards/deck_01/Spades_7.png",
            "Spades 8": "Cards/deck_01/Spades_8.png",
            "Spades 9": "Cards/deck_01/Spades_9.png",
            "Spades 10": "Cards/deck_01/Spades_10.png",
            "Spades Jack": "Cards/deck_01/Spades_11.png",
            "Spades Queen": "Cards/deck_01/Spades_12.png",
            "Spades King": "Cards/deck_01/Spades_13.png"
            }

    def __deck_02(self):
        self.deck = {
            "Clubs Ace": "Cards/deck_02/AC.png",
            "Clubs 2": "Cards/deck_02/2C.png",
            "Clubs 3": "Cards/deck_02/3C.png",
            "Clubs 4": "Cards/deck_02/4C.png",
            "Clubs 5": "Cards/deck_02/5C.png",
            "Clubs 6": "Cards/deck_02/6C.png",
            "Clubs 7": "Cards/deck_02/7C.png",
            "Clubs 8": "Cards/deck_02/8C.png",
            "Clubs 9": "Cards/deck_02/9C.png",
            "Clubs 10": "Cards/deck_02/10C.png",
            "Clubs Jack": "Cards/deck_02/JC.png",
            "Clubs Queen": "Cards/deck_02/QC.png",
            "Clubs King": "Cards/deck_02/KC.png",
            "Diamonds Ace": "Cards/deck_02/AD.png",
            "Diamonds 2": "Cards/deck_02/2D.png",
            "Diamonds 3": "Cards/deck_02/3D.png",
            "Diamonds 4": "Cards/deck_02/4D.png",
            "Diamonds 5": "Cards/deck_02/5D.png",
            "Diamonds 6": "Cards/deck_02/6D.png",
            "Diamonds 7": "Cards/deck_02/7D.png",
            "Diamonds 8": "Cards/deck_02/8D.png",
            "Diamonds 9": "Cards/deck_02/9D.png",
            "Diamonds 10": "Cards/deck_02/10D.png",
            "Diamonds Jack": "Cards/deck_02/JD.png",
            "Diamonds Queen": "Cards/deck_02/QD.png",
            "Diamonds King": "Cards/deck_02/KD.png",
            "Spades Ace": "Cards/deck_02/AS.png",
            "Spades 2": "Cards/deck_02/2S.png",
            "Spades 3": "Cards/deck_02/3S.png",
            "Spades 4": "Cards/deck_02/4S.png",
            "Spades 5": "Cards/deck_02/5S.png",
            "Spades 6": "Cards/deck_02/6S.png",
            "Spades 7": "Cards/deck_02/7S.png",
            "Spades 8": "Cards/deck_02/8S.png",
            "Spades 9": "Cards/deck_02/9S.png",
            "Spades 10": "Cards/deck_02/10S.png",
            "Spades Jack": "Cards/deck_02/JS.png",
            "Spades Queen": "Cards/deck_02/QS.png",
            "Spades King": "Cards/deck_02/KS.png",
            "Hearts Ace": "Cards/deck_02/AH.png",
            "Hearts 2": "Cards/deck_02/2H.png",
            "Hearts 3": "Cards/deck_02/3H.png",
            "Hearts 4": "Cards/deck_02/4H.png",
            "Hearts 5": "Cards/deck_02/5H.png",
            "Hearts 6": "Cards/deck_02/6H.png",
            "Hearts 7": "Cards/deck_02/7H.png",
            "Hearts 8": "Cards/deck_02/8H.png",
            "Hearts 9": "Cards/deck_02/9H.png",
            "Hearts 10": "Cards/deck_02/10H.png",
            "Hearts Jack": "Cards/deck_02/JH.png",
            "Hearts Queen": "Cards/deck_02/QH.png",
            "Hearts King": "Cards/deck_02/KH.png"
            }

    def __deck_03(self):
        self.deck = {
            "Clubs Ace": "Cards/deck_03/ace_of_clubs.png",
            "Clubs 2": "Cards/deck_03/2_of_clubs.png",
            "Clubs 3": "Cards/deck_03/3_of_clubs.png",
            "Clubs 4": "Cards/deck_03/4_of_clubs.png",
            "Clubs 5": "Cards/deck_03/5_of_clubs.png",
            "Clubs 6": "Cards/deck_03/6_of_clubs.png",
            "Clubs 7": "Cards/deck_03/7_of_clubs.png",
            "Clubs 8": "Cards/deck_03/8_of_clubs.png",
            "Clubs 9": "Cards/deck_03/9_of_clubs.png",
            "Clubs 10": "Cards/deck_03/10_of_clubs.png",
            "Clubs Jack": "Cards/deck_03/jack_of_clubs.png",
            "Clubs Queen": "Cards/deck_03/queen_of_clubs.png",
            "Clubs King": "Cards/deck_03/king_of_clubs.png",
            "Diamonds Ace": "Cards/deck_03/ace_of_diamonds.png",
            "Diamonds 2": "Cards/deck_03/2_of_diamonds.png",
            "Diamonds 3": "Cards/deck_03/3_of_diamonds.png",
            "Diamonds 4": "Cards/deck_03/4_of_diamonds.png",
            "Diamonds 5": "Cards/deck_03/5_of_diamonds.png",
            "Diamonds 6": "Cards/deck_03/6_of_diamonds.png",
            "Diamonds 7": "Cards/deck_03/7_of_diamonds.png",
            "Diamonds 8": "Cards/deck_03/8_of_diamonds.png",
            "Diamonds 9": "Cards/deck_03/9_of_diamonds.png",
            "Diamonds 10": "Cards/deck_03/10_of_diamonds.png",
            "Diamonds Jack": "Cards/deck_03/jack_of_diamonds.png",
            "Diamonds Queen": "Cards/deck_03/queen_of_diamonds.png",
            "Diamonds King": "Cards/deck_03/king_of_diamonds.png",
            "Spades Ace": "Cards/deck_03/ace_of_spades.png",
            "Spades 2": "Cards/deck_03/2_of_spades.png",
            "Spades 3": "Cards/deck_03/3_of_spades.png",
            "Spades 4": "Cards/deck_03/4_of_spades.png",
            "Spades 5": "Cards/deck_03/5_of_spades.png",
            "Spades 6": "Cards/deck_03/6_of_spades.png",
            "Spades 7": "Cards/deck_03/7_of_spades.png",
            "Spades 8": "Cards/deck_03/8_of_spades.png",
            "Spades 9": "Cards/deck_03/9_of_spades.png",
            "Spades 10": "Cards/deck_03/10_of_spades.png",
            "Spades Jack": "Cards/deck_03/jack_of_spades.png",
            "Spades Queen": "Cards/deck_03/queen_of_spades.png",
            "Spades King": "Cards/deck_03/king_of_spades.png",
            "Hearts Ace": "Cards/deck_03/ace_of_hearts.png",
            "Hearts 2": "Cards/deck_03/2_of_hearts.png",
            "Hearts 3": "Cards/deck_03/3_of_hearts.png",
            "Hearts 4": "Cards/deck_03/4_of_hearts.png",
            "Hearts 5": "Cards/deck_03/5_of_hearts.png",
            "Hearts 6": "Cards/deck_03/6_of_hearts.png",
            "Hearts 7": "Cards/deck_03/7_of_hearts.png",
            "Hearts 8": "Cards/deck_03/8_of_hearts.png",
            "Hearts 9": "Cards/deck_03/9_of_hearts.png",
            "Hearts 10": "Cards/deck_03/10_of_hearts.png",
            "Hearts Jack": "Cards/deck_03/jack_of_hearts.png",
            "Hearts Queen": "Cards/deck_03/queen_of_hearts.png",
            "Hearts King": "Cards/deck_03/king_of_hearts.png"}

        
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
