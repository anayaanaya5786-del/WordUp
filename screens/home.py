# screens/home.py
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp

class HomeScreen(MDScreen):
    def on_pre_enter(self):
        app = MDApp.get_running_app()
        name = name = "Ануш"
        self.ids.welcome.text = f"Привет, {name}!"