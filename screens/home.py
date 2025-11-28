# screens/home.py
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp

class HomeScreen(MDScreen):
    def on_pre_enter(self):
        app = MDApp.get_running_app()
        name = app.current_user_name
        self.ids.welcome.text = f"Привет, {name}!"