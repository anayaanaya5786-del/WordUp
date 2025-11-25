# screens/register.py
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
import sqlite3

class RegisterScreen(MDScreen):
    def register(self):
        email = self.ids.email.text.strip()
        pwd1 = self.ids.pwd1.text
        pwd2 = self.ids.pwd2.text

        if not email or not pwd1:
            self.ids.error_label.text = "Заполните все поля!"
            return
        if pwd1 != pwd2:
            self.ids.error_label.text = "Пароли не совпадают!"
            return
        if len(pwd1) < 4:
            self.ids.error_label.text = "Пароль слишком короткий"
            return

        try:
            conn = sqlite3.connect("data/database.db")
            c = conn.cursor()
            name = email.split("@")[0].capitalize()
            c.execute("INSERT INTO users (email, password, name) VALUES (?, ?, ?)", (email, pwd1, name))
            user_id = c.lastrowid
            conn.commit()
            conn.close()

            app = MDApp.get_running_app()
            app.login_success(user_id, name, email)

        except sqlite3.IntegrityError:
            self.ids.error_label.text = "Этот email уже занят!"