from PIL import Image,ImageTk
from appJar import gui
from player_info import PlayerHand, Player
import simpleaudio as beats
import numpy as np
app = gui('djack')

# Music Credit: Eric Matyas, soundimage.org
# Art Credit: Andrew Tidey, https://opengameart.org/content/cards-set

class djackGUI:
    def __init__(self):
        self.started = False
        self.start_menu()
        app.go(startWindow='New Game')

    def start_menu(self):
        app.startSubWindow('New Game')
        app.setLocation('CENTER')
        app.setSticky('news')
        app.setPadding([20,20])

        self.music_wave = beats.WaveObject.from_wave_file('resources/sounds/Insert-Quarter.wav')
        self.music = self.music_wave.play()
        
        # Welcome image
        app.addLabel('logo','djack',0,0,2)
        app.getLabelWidget('logo').config(font='Quicksand\ Book 62')
        
        # Add scale to set number of players
        app.setFont(size=16,family='CaviarDreams')        
        app.addLabel('nump_txt','How many players are participating in this game?',1,0,4)

        # Update the row and change the scale settings
        row = app.getRow()
        app.addScale('nump_scale',row,0,colspan=2)
        app.setScaleRange('nump_scale',1,5)
        app.setScaleIncrement('nump_scale',1)
        app.showScaleValue('nump_scale')
        app.setScaleChangeFunction('nump_scale',self.update_entries)

        # Update row
        row = app.getRow()
        
        # Add labels and entries
        app.addLabel('players_label','Add Players:',row,0,2)
        app.addLabel('player_1_txt','Name: ',row+1,0)
        app.addValidationEntry('player_1','p',1,2)
        app.addLabel('player_2_txt','Name: ',row+2,0)
        app.addValidationEntry('player_2','p',1,2)
        app.addLabel('player_3_txt','Name: ',row+3,0)
        app.addValidationEntry('player_3','p',1,2)
        app.addLabel('player_4_txt','Name: ',row+4,0)
        app.addValidationEntry('player_4','p',1,2)
        app.addLabel('player_5_txt','Name: ',row+5,0)
        app.addValidationEntry('player_5','p',1,2)

        # Set entry defaults
        app.setEntryDefault('player_1','Jack B.')
        app.setEntryDefault('player_2','Jack B.')
        app.setEntryDefault('player_3','Jack B.')
        app.setEntryDefault('player_4','Jack B.')
        app.setEntryDefault('player_5','Jack B.')

        # Set entry checks
        app.setEntryChangeFunction('player_1',self.check_during)
        app.setEntryChangeFunction('player_2',self.check_during)
        app.setEntryChangeFunction('player_3',self.check_during)
        app.setEntryChangeFunction('player_4',self.check_during)
        app.setEntryChangeFunction('player_5',self.check_during)

        # Hide labels
        app.hideLabel('player_2_txt')
        app.hideLabel('player_3_txt')
        app.hideLabel('player_4_txt')
        app.hideLabel('player_5_txt')

        # Hide entries
        app.hideEntry('player_2')
        app.hideEntry('player_3')
        app.hideEntry('player_4')
        app.hideEntry('player_5')

        # Update row
        row = app.getRow()

        # Add start game button
        app.addNamedButton('START GAME!','start',self.close_start,row,0,2)
        app.setButtonState('start','disabled')
        # app.setButtonSubmitFunction('start',self.close_start)
        app.enableEnter(self.close_start)

        app.registerEvent(self.play_music)
        
        app.stopSubWindow()

    def play_music(self):
        if not (self.music.is_playing()):
            self.music = self.music_wave.play()
        else:
            pass
    
    
    def update_entries(self):
        for i in range(5):
            j = i+1
            entry = 'player_{}'.format(j)
            label = 'player_{}_txt'.format(j)
            app.hideLabel(label)
            app.hideEntry(entry)

        num = app.getScale('nump_scale')
        for j in range(num):
            k = j+1
            entry = 'player_{}'.format(k)
            label = 'player_{}_txt'.format(k)
            app.showLabel(label)
            app.showEntry(entry)

    def check_during(self,entry):
        data = app.getEntry(entry)
        num = app.getScale('nump_scale')
        for i in range(num):
            j = i + 1
            temp = 'player_{}'.format(j)
            check = app.getEntry(temp)
            if ((data == check) and temp != entry):
                app.setEntryInvalid(entry)
                app.setButtonState('start','disabled')
                break
            else:
                app.setEntryValid(entry)
                app.setButtonState('start','normal')
                continue
        
    def close_start(self):
        # Make the Players list from the entries
        self.players = []
        self.players_ref = {}
        num = app.getScale('nump_scale')

        for i in range(num):
            j = i+1
            entry = 'player_{}'.format(j)
            name = app.getEntry(entry)
            self.players.append(name)
            self.players_ref[name] = Player(name)

        beats.stop_all()
        self.started = True
        app.destroySubWindow('New Game')
        app.show()
        self.num = num
        self.table_layout(num)

    # MAIN FUNCTION
    def table_layout(self,num):
        # Set up the look
        app.setTitle('djack')
        app.setSize('fullscreen')
        app.setBg('firebrick3')

        # Lay down some fresh beats
        self.music_wave = beats.WaveObject.from_wave_file('resources/sounds/Arcade-Puzzler_v001.wav')
        row = app.getRow()

        dealer_deck = Image.open('resources/deck_01/large/Back_Blue_1.png')
        dealer_deck.convert('RGBA')
        dealer_deck = ImageTk.PhotoImage(dealer_deck)

        dealer_col = int(num/2)
        app.addImageData('dealer deck',dealer_deck,fmt='PhotoImage',row=row,column=dealer_col)

        row = app.getRow()

        # Make images for each command
        im_hit = Image.open('resources/commands/hit_me.png')
        im_hit.convert('RGBA')
        im_hit = ImageTk.PhotoImage(im_hit)

        im_stand = Image.open('resources/commands/stand.png')
        im_stand.convert('RGBA')
        im_stand = ImageTk.PhotoImage(im_stand)
        
        for i in range(num):
            # app.setStretch('none')
            app.addImageData('{} speech'.format(self.players[i]), im_hit,fmt='PhotoImage',row=row,column=i)
            app.hideImage('{} speech'.format(self.players[i]))
            r = row + 1
            player = self.players_ref.get(self.players[i])
            label = '{0}\nScore: {1}'.format(self.players[i],player.score)
            app.addLabel('{}'.format(self.players[i]),label,row=r,column=i)
            app.setLabelSticky('{}'.format(self.players[i]),'s')
            # im = Image.open('{}_hand.png'.format(self.players[i]))
            im = Image.open('resources/deck_01/example_hand.png')
            im.convert('RGBA')
            im = ImageTk.PhotoImage(im)
            r += 1
            app.setSticky('n')
            app.addImageData('{} Hand'.format(self.players[i]),im,fmt='PhotoImage',row=r,column=i)
            im = Image.open('{}_hand.png'.format(self.players[i]))
            im.convert('RGBA')
            im = ImageTk.PhotoImage(im)
            app.reloadImageData('{} Hand'.format(self.players[i]),im,fmt='PhotoImage')
            r += 1
            app.addNamedButton('Hit me!','{} hit'.format(self.players[i]),self.hit,row=r,column=i)
            r += 1
            app.addNamedButton('Rematch?','{} rematch'.format(self.players[i]),self.rematch,row=r,column=i)
            app.hideButton('{} rematch'.format(self.players[i]))

    def rematch(self,cmd):
        name = cmd.replace(' rematch','')
        player = self.players_ref.get(name)
        player.rematch(name)
        im = Image.open('{}_hand.png'.format(name))
        im.convert('RGBA')
        im = ImageTk.PhotoImage(im)
        app.reloadImageData('{} Hand'.format(name),im,fmt='PhotoImage')
        label = '{0}\nScore: {1}'.format(name,player.score)
        app.setLabel('{}'.format(name),label)
        app.enableButton('{} hit'.format(name))
        app.hideButton('{} rematch'.format(name))
        
        # self.table_layout(self.num)

    def hit(self,cmd):
        name = cmd.replace(' hit','')
        player = self.players_ref.get(name)
        player.hit()
        im = Image.open('{}_hand.png'.format(name))
        im.convert('RGBA')
        im = ImageTk.PhotoImage(im)
        app.reloadImageData('{} Hand'.format(name),im,fmt='PhotoImage')
        player = self.players_ref.get(name)
        label = '{0}\nScore: {1}'.format(name,player.score)
        app.setLabel('{}'.format(name),label)

        if player.busted():
            app.setLabel('{}'.format(name), '{}\nBUSTED'.format(name))
            app.disableButton('{} hit'.format(name))
            app.showButton('{} rematch'.format(name))

if __name__=='__main__':
    dj = djackGUI()
    
