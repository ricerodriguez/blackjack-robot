from PIL import Image
from player_info import Player, PlayerHand

class ResourceLoader(PlayerHand):
    def __init__(self,PlayerHand):
        self.hand = PlayerHand.get_hand()
        self.imgs = PlayerHand.get_hand()
        self.deck = PlayerHand.get_deck()
        self.hand.sort()
        self.update_images()

    def update_images(self):
        self.hand = PlayerHand.get_hand()
        self.imgs = PlayerHand.get_hand()
        self.deck = PlayerHand.get_deck()
        self.hand.sort()
        for i,card in enumerate(self.hand):
            img_path = self.deck.get(card)
            self.imgs.insert(i,img_path)

        for i,path in enumerate(imgs):
            image = Image.open(path)
            if (i == 0):
                self.pillows = [image]
            else:
                self.pillows.append(image)

    def get_image_names(self):
        return self.imgs

    def get_images(self):
        return self.pillows
