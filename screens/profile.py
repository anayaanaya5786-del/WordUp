# screens/profile.py — email всегда актуальный!
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.clock import Clock

class ProfileScreen(MDScreen):
    def on_enter(self):
        # Обновляем каждый раз при входе
        Clock.schedule_once(self.update_email, 0.1)

    def update_email(self, dt):
        app = MDApp.get_running_app()
        email = getattr(app, "user_email", None)
        if email:
            self.ids.user_email.text = email
        else:
            self.ids.user_email.text = "anush@gmail.com"

    def logout(self):
        app = MDApp.get_running_app()
        app.current_user = None
        app.current_user_name = "Друг"
        app.user_email = None
        app.root.current = "login"