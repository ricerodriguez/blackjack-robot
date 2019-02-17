from PIL import Image,ImageTk
from appJar import gui
from player_info import PlayerHand, Player
from resource_loader import ResourceLoader

app = gui('djack')

class djackGUI:
    def __init__(self, num_players=1):
        self.num_players = num_players

        # # Make a Player reference for each possible player
        # temp_p = Player()
        # temp_players = [temp_p]

        # for i in range(4):
        #     temp = Player()
        #     temp_players.append(temp)

        # # Make a Python Dictionary to map names to references
        # self.players = {
        #     'Player 1' : temp_players[0],
        #     'Player 2' : temp_players[1],
        #     'Player 3' : temp_players[2],
        #     'Player 4' : temp_players[3],
        #     'Player 5' : temp_players[4]
        # }
        
        self.start_menu()
        # self.table_layout()

    def start_menu(self):
        app.startSubWindow('New Game')
        app.setLocation('CENTER')
        app.setSticky('news')
        app.setPadding([20,20])

        # Welcome image
        app.addLabel('logo','djack',0,0,2)
        app.getLabelWidget('logo').config(font='Modern\ Sans 62')
        
        # Add scale to set number of players
        app.addLabel('nump_txt','How many players are participating in this game?',1,0,4)
        app.setFont(size=16,family='URW Gothic')

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
        app.addEntry('player_1','p',1,2)
        app.addLabel('player_2_txt','Name: ',row+2,0)
        app.addEntry('player_2','p',1,2)
        app.addLabel('player_3_txt','Name: ',row+3,0)
        app.addEntry('player_3','p',1,2)
        app.addLabel('player_4_txt','Name: ',row+4,0)
        app.addEntry('player_4','p',1,2)
        app.addLabel('player_5_txt','Name: ',row+5,0)
        app.addEntry('player_5','p',1,2)

        # Set entry defaults
        app.setEntryDefault('player_1','Jack B.')
        app.setEntryDefault('player_2','Jack B.')
        app.setEntryDefault('player_3','Jack B.')
        app.setEntryDefault('player_4','Jack B.')
        app.setEntryDefault('player_5','Jack B.')

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
        app.stopSubWindow()
        app.go(startWindow='New Game')

    def update_entries(self):
        app.openSubWindow('New Game')
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
        app.stopSubWindow()
        
    def close_start(self):
        # Make the Players list from the entries
        self.players = []
        self.players_ref = {}
        app.openSubWindow('New Game')
        num = app.getScale('nump_scale')
        for i in range(num):
            j = i+1
            entry = 'player_{}'.format(j)
            name = app.getEntry(entry)
            self.players.append(name)
            self.players_ref[name] = Player(name)
            # key = 'Player {}'.format(j)
            # self.players[name] = self.players[key]
            # del self.players[key]

        app.stopSubWindow()    
        app.destroySubWindow('New Game')
        print(self.players)
        app.show()
        self.table_layout(num)

    def table_layout(self,num):
        app.setTitle('djack')
        app.setSize('fullscreen')
        app.setLocation('CENTER')

        positions = [(0,0),(1,1),(2,2),(2,3),(1,4),(0,5)]
        
        for i in range(num):
            p_cards = ImageTk.PhotoImage(Image.open('{}_hand.gif'.format(self.players[i])))
            pos = list(positions[i])
            app.startFrame('{} Frame'.format(self.players[i]),pos[0],pos[1])
            app.addImageData('{} Hand'.format(self.players[i]),p_cards,fmt='PhotoImage')
            # app.addImage('{} Hand'.format(self.players[i]),'{}_hand.gif'.format(self.players[i]))
            
        # app.addImage('test','Cards/deck_02/2C.png')

if __name__=='__main__':
    dj = djackGUI()
    
