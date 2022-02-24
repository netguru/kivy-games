from locale import currency
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

class MenuScreen(Screen):
    pass

class HomeScreen(Screen):
    pass
        
class RootScreenManager(ScreenManager):
    pass

class MainApp(App):    
    def build(self):
        return Builder.load_file('kvs/screen_manager.kv')

if __name__ == '__main__':
    MainApp().run()