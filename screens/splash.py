from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.clock import Clock


class SplashScreen(Screen):
    def on_enter(self, *args):
        Clock.schedule_once(self._splash_in, 2)
        return super().on_enter(*args)

    def _splash_in(self, duration):
        logo_image = Image(source="assets/images/netguru_logo.png", pos=(800, 800))
        animation = Animation(x=0, y=0, d=2, t="out_bounce")
        animation.start(logo_image)
        self.manager.ids.splash.ids.logo.add_widget(logo_image)
        Clock.schedule_once(self._splash_out, 2)

    def _splash_out(self, duration):
        self.manager.transition.direction = "left"
        self.manager.transition.duration = duration
        self.manager.current = "tictactoe"
