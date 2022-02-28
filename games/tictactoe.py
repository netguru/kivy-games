from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty, NumericProperty
from kivy.event import EventDispatcher


class Player(EventDispatcher):
    active = BooleanProperty(False)
    display_score = StringProperty("0")
    name = StringProperty("")
    score = NumericProperty(0)

    def __init__(self, name, dice, active=False, **kwargs) -> None:
        super(Player, self).__init__(**kwargs)
        self.dice = dice
        self.active = active
        self.name = name

class TicTacToe(Screen):
    
    player1 = Player(name='Player 1', dice='X', active=True)
    player2 = Player(name='Player 2', dice='O')
    
    matrix = {'00': None, '01': None, '02': None, '10': None, '11': None, '12': None, '20': None, '21': None, '22': None}
    
    def on_pre_enter(self, *args):
        for tile_id in self.matrix.keys():
            setattr(self, 'tile_%s' % tile_id, ObjectProperty(None))
        return super().on_pre_enter(*args)
    
    def on_leave(self, *args):
        self._reset_tiles()
        return super().on_leave(*args)
    
    def _current_player(self):
        player = self.player1 if self.player1.active else self.player2
        self.player1.active = not self.player1.active
        self.player2.active = not self.player2.active
        return player
        
    def _reset_tiles(self):
        for tile in self.matrix.keys():
            self.ids['root.tile_%s' % tile].text = ''

    def _check_rows(self):
        x_points = 0
        o_points = 0
        for row in range(3):
            for col in range(3):
                dice = self.matrix['{row}{col}'.format(row=row, col=col)]
                print(dice)
                
    def _check_cols(self):
        pass
                
    def _check_diagonal(self):
        pass
    
    def _check_move(self):
        pass
    
    def _game_over():
        pass
    
    def restart(self):
        self._reset_tiles()

    def reset_scores(self):
        self.player1.score += 1
        self.player2.score += 1
        
    def make_move(self, tile):
        if not tile.text:
            player = self._current_player()
            tile.text = self.matrix[tile.name] = player.dice
            self._check_move()
