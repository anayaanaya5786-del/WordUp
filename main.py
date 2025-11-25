# main.py
from kivymd.app import MDApp
from kivymd.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.core.window import Window
import os
import sqlite3

Window.size = (360, 740)

class Root(ScreenManager):
    pass

class WordUpApp(MDApp):
    current_user = None
    current_user_name = "Друг"
    db_path = "data/database.db"
    current_lang = "en-ru"

    languages = {
        "en-ru": {"name": "English → Русский", "flag": "GB", "color": "#4CAF50"},
        "ru-hy": {"name": "Русский → Армянский", "flag": "AM", "color": "#9C27B0"}
    }

    def build(self):
        self.title = "WordUp"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"

        os.makedirs("data", exist_ok=True)
        os.makedirs("assets", exist_ok=True)

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT UNIQUE, password TEXT, name TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS progress
                     (user_id INTEGER, lang TEXT, streak INTEGER DEFAULT 0, learned INTEGER DEFAULT 0,
                      PRIMARY KEY (user_id, lang))''')
        c.execute("INSERT OR IGNORE INTO users (email, password, name) VALUES ('anush@gmail.com', '1234', 'Ануш')")
        conn.commit()
        conn.close()

        Builder.load_file("kv/style.kv")

        # Подключаем все экраны
        from screens.login import LoginScreen
        from screens.register import RegisterScreen
        from screens.home import HomeScreen
        from screens.dictionary import DictionaryScreen
        from screens.cards import CardsScreen
        from screens.ai_cards import AICardsScreen

        sm = Root()

        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(DictionaryScreen(name="dictionary"))
        sm.add_widget(CardsScreen(name="cards"))
        sm.add_widget(AICardsScreen(name="ai_cards"))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(RegisterScreen(name="register"))

        from screens.profile import ProfileScreen
        sm.add_widget(ProfileScreen(name="profile"))

        from screens.admin import AdminScreen
        sm.add_widget(AdminScreen(name="admin"))

        return sm

    def login_success(self, user_id, name, email):
        self.current_user = int(user_id)
        self.current_user_name = name or "Друг"
        self.user_email = email  # ← СОХРАНЯЕМ EMAIL!
        self.root.current = "home"
        self.update_welcome_and_profile()

    def update_welcome_and_profile(self):
        home = self.root.get_screen("home")
        if hasattr(home.ids, "welcome"):
            home.ids.welcome.text = f"Привет, {self.current_user_name}!"
        self.update_progress_display()

    def set_language(self, lang):
        self.current_lang = lang
        self.update_progress_display()

    def update_progress_display(self):
        home = self.root.get_screen("home")
        lang_name = self.languages[self.current_lang]["name"]
        home.ids.lang_label.text = f"[color=#000000]Изучаешь:[/color] [b]{lang_name}[/b]"
        home.ids.streak_label.text = self.get_streak_text()

    def get_streak_text(self):
        if not self.current_user:
            return "Стрик: 0 дней • Выучено: 0 слов"
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT streak, learned FROM progress WHERE user_id=? AND lang=?",
                  (self.current_user, self.current_lang))
        row = c.fetchone()
        if not row:
            c.execute("INSERT INTO progress (user_id, lang) VALUES (?, ?)", (self.current_user, self.current_lang))
            conn.commit()
            conn.close()
            return "Стрик: 0 дней • Выучено: 0 слов"
        conn.close()
        return f"Стрик: {row[0]} дней • Выучено: {row[1]} слов"

    def increase_learned(self):
        if not self.current_user:
            return
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("UPDATE progress SET learned = learned + 1 WHERE user_id=? AND lang=?",
                  (self.current_user, self.current_lang))
        conn.commit()
        conn.close()
        self.update_progress_display()

if __name__ == "__main__":
    WordUpApp().run()