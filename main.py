from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from screens.tictactoe import Tile


class RootScreenManager(ScreenManager):
    pass


class MainApp(App):
    title = "Tic Tac Toe"

    def build(self):
        manager = Builder.load_file("templates/screen_manager.kv")
        self._build_grid_layout(manager)
        return manager

    def _build_grid_layout(self, manager):
        for row in range(manager.ids.tictactoe.rows):
            for column in range(manager.ids.tictactoe.cols):
                manager.screens[1].ids.grid_layout.add_widget(
                    Tile("%d%d" % (row, column))
                )
        return manager


if __name__ == "__main__":
    MainApp().run()
