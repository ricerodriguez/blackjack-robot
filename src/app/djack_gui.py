from PIL import Image,ImageTk
from appJar import gui
from player_info import PlayerHand, Player
import simpleaudio as beats
import numpy as np

app = gui('djack')
app.setBg('green')


class djackGUI:
    def __init__(self, num_players=1):
        self.num = num_players
        self.started = False
        self.start_menu()
        # self.table_layout(self.num)
        app.go(startWindow='New Game')

    def start_menu(self):
        app.startSubWindow('New Game')
        app.setLocation('CENTER')
        app.setSticky('news')
        app.setPadding([20,20])
        app.setFont(size=16,family='Modern Sans')

        self.music_wave = beats.WaveObject.from_wave_file('sounds/Insert-Quarter.wav')
        self.music = self.music_wave.play()
        
        # app.showSplash('djack','white','white','black',44)
        # Welcome image
        app.addLabel('logo','djack',0,0,2)
        app.getLabelWidget('logo').config(font='Modern\ Sans 62')
        
        # Add scale to set number of players
        app.setFont(size=16,family='URW Gothic')        
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
        app.setButtonSubmitFunction('start',self.close_start)

        app.registerEvent(self.play_music)
        
        app.stopSubWindow()

    def play_music(self):
        if not (self.music.is_playing()):
            self.music = self.music_wave.play()
        else:
            pass
        # if not (self.started or self.music.is_playing()):
        #     self.music = self.music_wave.play()
        # else:
        #     pass
    
    
    def update_entries(self):
        # app.openSubWindow('New Game')
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
 #        app.stopSubWindow()
# -
    def check_during(self,entry):
        data = app.getEntry(entry)
        num = app.getScale('nump_scale')
        # app.openSubWindow('New Game')
        for i in range(num):
            j = i + 1
            temp = 'player_{}'.format(j)
            check = app.getEntry(temp)
            if ((data == check) and temp != entry):
                app.setEntryInvalid(entry)
                app.setButtonState('start','disabled')
                # app.soundError()
                break
            else:
                app.setEntryValid(entry)
                app.setButtonState('start','normal')
                continue
        
    def close_start(self):
        # Make the Players list from the entries
        self.players = []
        self.players_ref = {}
        # app.openSubWindow('New Game')
        self.num = app.getScale('nump_scale')

        for i in range(self.num):
            j = i+1
            entry = 'player_{}'.format(j)
            name = app.getEntry(entry)
            self.players.append(name)
            self.players_ref[name] = Player(name)

        # app.stopSubWindow()
        beats.stop_all()
        self.started = True
        app.destroySubWindow('New Game')
        app.show()
        self.table_layout(self.num)
        
    def table_layout(self,num):
        # MAIN FUNCTION
        app.setTitle('djack')
        app.setSize('fullscreen')
        self.music_wave = beats.WaveObject.from_wave_file('sounds/Arcade-Puzzler_v001.wav')
        row = app.getRow()
        for i in range(num):
            app.addLabel('{}'.format(self.players[i]),row=row,column=i)
            im = Image.open('{}_hand.png'.format(self.players[i]))
            im.convert('RGBA')
            im = ImageTk.PhotoImage(im)
            r = row+1
            app.addImageData('{} Hand'.format(self.players[i]),im,fmt='PhotoImage',row=r,column=i)
        

if __name__=='__main__':
    dj = djackGUI()
    
