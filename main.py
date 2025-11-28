# main.py
from kivymd.app import MDApp
from kivymd.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.core.window import Window
import os
import sqlite3
from firebase_admin import credentials, initialize_app, db as firebase_db
import firebase_admin
from google.oauth2 import service_account
from plyer import notification  # Для локальных уведомлений

Window.size = (360, 740)

class Root(ScreenManager):
    pass

class WordUpViewModel:
    def __init__(self, app):
        self.app = app

    def sync_data(self):
        local_conn = sqlite3.connect(self.app.db_path)
        local_c = local_conn.cursor()
        local_c.execute("SELECT * FROM users")
        local_users = local_c.fetchall()
        firebase_ref = firebase_db.reference('users')
        for user in local_users:
            firebase_ref.child(str(user[0])).set({'email': user[1], 'name': user[3]})
        # Sync progress similarly

class WordUpApp(MDApp):
    current_user = None
    current_user_name = "Друг"
    db_path = "data/database.db"
    current_lang = "en-ru"
    firebase_app = None
    view_model = None
    selected_category = None
    user_email = None

    languages = {
        "en-ru": {"name": "English → Русский", "flag": "GB", "color": "#4CAF50"},
        "ru-hy": {"name": "Русский → Армянский", "flag": "AM", "color": "#9C27B0"}
    }

    def build(self):
        self.title = "WordUp"
        self.theme_cls.theme_style = "Dark"  # Тёмная тема
        self.theme_cls.primary_palette = "Green"

        # Firebase
        if not firebase_admin._apps:
            cred = credentials.Certificate('path/to/firebase-credentials.json')
            self.firebase_app = initialize_app(cred, options={'databaseURL': 'https://your-project.firebaseio.com'})

        self.view_model = WordUpViewModel(self)

        os.makedirs("data", exist_ok=True)
        os.makedirs("assets", exist_ok=True)

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT UNIQUE, password TEXT, name TEXT, lang TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS progress
                     (user_id INTEGER, lang TEXT, streak INTEGER DEFAULT 0, learned INTEGER DEFAULT 0,
                      PRIMARY KEY (user_id, lang))''')
        c.execute("INSERT OR IGNORE INTO users (email, password, name) VALUES ('anush@gmail.com', '1234', 'Ануш')")
        conn.commit()
        conn.close()

        Builder.load_file("kv/style.kv")

        # Экраны
        from screens.login import LoginScreen
        from screens.register import RegisterScreen
        from screens.home import HomeScreen
        from screens.dictionary import DictionaryScreen
        from screens.cards import CardsScreen
        from screens.ai_cards import AICardsScreen
        from screens.profile import ProfileScreen
        from screens.admin import AdminScreen
        from screens.categories import CategoriesScreen
        from screens.lessons_screen import LessonsScreen
        from screens.flashcards import FlashcardsScreen
        from screens.practice import PracticeScreen
        from screens.language import LanguageScreen
        from screens.stats_screen import StatsScreen

        sm = Root()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(DictionaryScreen(name="dictionary"))
        sm.add_widget(CardsScreen(name="cards"))
        sm.add_widget(AICardsScreen(name="ai_cards"))
        sm.add_widget(ProfileScreen(name="profile"))
        sm.add_widget(AdminScreen(name="admin"))
        sm.add_widget(CategoriesScreen(name="categories"))
        sm.add_widget(LessonsScreen(name="lessons"))
        sm.add_widget(FlashcardsScreen(name="flashcards"))
        sm.add_widget(PracticeScreen(name="practice"))
        sm.add_widget(LanguageScreen(name="language"))
        sm.add_widget(StatsScreen(name="stats"))

        self.view_model.sync_data()  # Sync
        return sm

    def login_success(self, user_id, name, email):
        self.current_user = int(user_id)
        self.current_user_name = name or "Друг"
        self.user_email = email
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
        c.execute("SELECT streak, learned FROM progress WHERE user_id=? AND lang=?", (self.current_user, self.current_lang))
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
        c.execute("UPDATE progress SET learned = learned + 1 WHERE user_id=? AND lang=?", (self.current_user, self.current_lang))
        conn.commit()
        conn.close()
        self.update_progress_display()
        self.send_push_notification("Вы выучили новое слово!")
        self.view_model.sync_data()

    def send_push_notification(self, message):
        notification.notify(title="WordUp", message=message)
        # Firebase push: add FCM logic with device tokens

if __name__ == "__main__":
    WordUpApp().run()