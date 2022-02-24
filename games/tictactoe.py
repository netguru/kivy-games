from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty

result = {}

def current_player():
    if player1.active:
        player1.active = False
        player2.active = True
        return player1
    elif player2.active:
        player1.active = True
        player2.active = False
        return player2

class Player:
    def __init__(self, name, dice, active=False) -> None:
        self.name = name
        self.dice = dice
        self.score = ObjectProperty(None)
        self.active = active
        self.display_name = StringProperty()
        '''
        '{}{} ({})'.format(
            '*' if not active else '', name, dice)
        '''

class TicTacToe(Screen):
    
    def on_enter(self, *args):
        self._update_display_name()
        return super().on_enter(*args)
    
    def on_leave(self, *args):
        return super().on_leave(*args)
    
    def reset_scores(self):
        self.ids['player1.score'].text = '0'
        self.ids['player2.score'].text = '0'
    
    def _update_display_name(self):
        self.ids['player1.display_name'].text = '{}{} ({})'.format(
            '*' if player1.active else '', player1.name, player1.dice)
        self.ids['player2.display_name'].text = '{}{} ({})'.format(
            '*' if player2.active else '', player2.name, player2.dice)
    
    def make_move(self, tile):
        if not tile.text:
            player = current_player()
            tile.text = player.dice
            self._update_display_name()

player1 = Player(name='Player 1', dice='X', active=True)
player2 = Player(name='Player 2', dice='O')