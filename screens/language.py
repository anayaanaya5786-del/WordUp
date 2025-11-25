# screens/language.py
from kivymd.uix.screen import MDScreen
import sqlite3
from kivymd.app import MDApp
class LanguageScreen(MDScreen):
    def choose_lang(self, lang):
        app = MDApp.get_running_app()
        if app.current_user:
            conn = sqlite3.connect("data/database.db")
            c = conn.cursor()
            c.execute("UPDATE users SET lang=? WHERE id=?", (lang, app.current_user["id"]))
            conn.commit()
            conn.close()
        self.manager.current = "home"