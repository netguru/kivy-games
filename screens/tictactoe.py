from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.event import EventDispatcher
from kivy.properties import (
    StringProperty,
    BooleanProperty,
    NumericProperty,
    BoundedNumericProperty,
)


class Tile(ButtonBehavior, Image):
    def __init__(self, name, **kwargs):
        self.name = name
        super().__init__(**kwargs)


class Player(EventDispatcher):
    active = BooleanProperty(False)
    display_score = StringProperty("0")
    name = StringProperty("")
    active_dice_image = StringProperty()
    score = NumericProperty(0)
    winner = BooleanProperty(False)

    def __init__(
        self, name, dice, dice_image, winner_dice_image, active=False, **kwargs
    ) -> None:
        super(Player, self).__init__(**kwargs)
        self.dice = dice
        self.dice_image = dice_image
        self.winner_dice_image = winner_dice_image
        self.active_dice_image = dice_image
        self.active = active
        self.name = name

    def on_winner(self, obj, value):
        if value:
            obj.score += 1


class TicTacToe(Screen):

    player1 = Player(
        name="Player 1",
        dice="X",
        dice_image="assets/images/X.png",
        winner_dice_image="assets/images/X-WIN.png",
        active=True,
    )
    player2 = Player(
        name="Player 2",
        dice="O",
        dice_image="assets/images/O.png",
        winner_dice_image="assets/images/O-WIN.png",
    )
    rows = BoundedNumericProperty(3, min=3, max=3, errorvalue=3)
    cols = BoundedNumericProperty(3, min=3, max=3, errorvalue=3)
    game_over = BooleanProperty(False)
    is_draw = BooleanProperty(False)
    winner_dice_image = StringProperty("")
    matrix = {}
    tiles = {}
    winner_matrix = []

    def on_pre_enter(self, *args):
        self._highlight_active_player()
        return super().on_pre_enter(*args)

    def on_leave(self, *args):
        self._reset()
        return super().on_leave(*args)

    def on_game_over(self, instance, value):
        if value:
            Clock.schedule_once(self._switch_to_menu, 1)

    def _switch_to_menu(self, duration):
        self.manager.transition.direction = "left"
        self.manager.transition.duration = duration
        self.manager.current = "menu"

    def _current_player(self):
        player = self.player1 if self.player1.active else self.player2
        self.player1.active, self.player2.active = (
            not self.player1.active,
            not self.player2.active,
        )
        return player

    def _reset(self):
        self.game_over = False
        self.player1.winner = False
        self.player2.winner = False
        self.matrix.clear()
        for tile in self.tiles.values():
            tile.source = ""

    def _highlight_winner(self, player):
        for tile_name in self.winner_matrix:
            self.tiles[tile_name].source = player.winner_dice_image

    def _highlight_active_player(self):
        if not self.game_over:
            if self.player1.active:
                self.player1.active_dice_image = self.player1.winner_dice_image
                self.player2.active_dice_image = self.player2.dice_image
            elif self.player2.active:
                self.player2.active_dice_image = self.player2.winner_dice_image
                self.player1.active_dice_image = self.player1.dice_image

    def _set_winner(self, player, points):
        if points == 3:
            player.winner = True
            self.game_over = True
            self.is_draw = False
            self.winner_dice_image = player.winner_dice_image
            self._highlight_winner(player)
            return True
        return False

    def _get_tile_name(self, row_index, column_index):
        return "{row}{col}".format(row=row_index, col=column_index)

    def _check_dice_points(self, row_index, column_index, x_points, o_points):
        tile_name = self._get_tile_name(row_index, column_index)
        dice = self.matrix.get(tile_name)
        if dice == self.player1.dice:
            x_points += 1
        elif dice == self.player2.dice:
            o_points += 1
        return x_points, o_points

    def _check_rows(self):
        for row_index in range(self.rows):
            x_points = o_points = 0
            for column_index in range(self.cols):
                x_points, o_points = self._check_dice_points(
                    row_index, column_index, x_points, o_points
                )
                tile_name = self._get_tile_name(row_index, column_index)
                self.winner_matrix.append(tile_name)
            if self._set_winner(self.player1, x_points) or self._set_winner(
                self.player2, o_points
            ):
                return
            else:
                self.winner_matrix.clear()

    def _check_cols(self):
        for column_index in range(self.cols):
            x_points = 0
            o_points = 0
            for row_index in range(self.rows):
                x_points, o_points = self._check_dice_points(
                    row_index, column_index, x_points, o_points
                )
                tile_name = self._get_tile_name(row_index, column_index)
                self.winner_matrix.append(tile_name)
            if self._set_winner(self.player1, x_points) or self._set_winner(
                self.player2, o_points
            ):
                return
            else:
                self.winner_matrix.clear()

    def _check_right_diagonal(self):
        start_row_index = 0
        for current_column_index in range(self.cols):
            while start_row_index < self.rows:
                x_points = o_points = 0
                row_index = start_row_index
                column_index = current_column_index
                self.winner_matrix.clear()
                while row_index >= 0 and column_index < self.cols:
                    x_points, o_points = self._check_dice_points(
                        row_index, column_index, x_points, o_points
                    )
                    tile_name = self._get_tile_name(row_index, column_index)
                    self.winner_matrix.append(tile_name)
                    if self._set_winner(self.player1, x_points) or self._set_winner(
                        self.player2, o_points
                    ):
                        return
                    row_index -= 1
                    column_index += 1
                start_row_index += 1
        else:
            self.winner_matrix.clear()

    def _check_left_diagonal(self):
        start_column_index = 0
        for current_row_index in reversed(range(self.rows)):
            while start_column_index < self.cols:
                x_points = o_points = 0
                row_index = current_row_index
                column_index = start_column_index
                self.winner_matrix.clear()
                while row_index >= 0 and column_index >= 0:
                    x_points, o_points = self._check_dice_points(
                        row_index, column_index, x_points, o_points
                    )
                    tile_name = self._get_tile_name(row_index, column_index)
                    self.winner_matrix.append(tile_name)
                    if self._set_winner(self.player1, x_points) or self._set_winner(
                        self.player2, o_points
                    ):
                        return
                    row_index -= 1
                    column_index -= 1
                if start_column_index == self.cols - 1:
                    break
                else:
                    start_column_index += 1
        else:
            self.winner_matrix.clear()

    def _check_draw(self):
        if not self.game_over and len(self.matrix) == 9:
            self.game_over = True
            self.is_draw = True

    def _check_move(self):
        self._check_rows()
        self._check_cols()
        self._check_right_diagonal()
        self._check_left_diagonal()
        self._check_draw()

    def _record_move(self, tile):
        player = self._current_player()
        tile.source = player.dice_image
        self.matrix[tile.name] = player.dice
        self.tiles[tile.name] = tile

    def reset_scores(self):
        self.player1.score = 0
        self.player2.score = 0

    def make_move(self, tile):
        if not tile.source and not self.game_over:
            self._record_move(tile)
            self._check_move()
            self._highlight_active_player()
