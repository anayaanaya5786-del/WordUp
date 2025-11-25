# screens/login.py — СЕКРЕТНЫЙ ВХОД ДЛЯ АДМИНА!
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
import sqlite3

class LoginScreen(MDScreen):
    def login(self):
        email = self.ids.email.text.strip()
        password = self.ids.password.text

        # СЕКРЕТНЫЙ ВХОД АДМИНА!
        if email == "admin" and password == "wordup123":
            app = MDApp.get_running_app()
            app.root.current = "admin"
            return

        if not email or not password:
            self.ids.error_label.text = "Заполните все поля!"
            return

        conn = sqlite3.connect("data/database.db")
        c = conn.cursor()
        c.execute("SELECT id, name FROM users WHERE email=? AND password=?", (email, password))
        user = c.fetchone()
        conn.close()

        if user:
            app = MDApp.get_running_app()
            app.login_success(user[0], user[1], email)  # передаём email
        else:
            self.ids.error_label.text = "Неправильный логин или пароль"