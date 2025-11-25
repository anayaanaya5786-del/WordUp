# screens/admin.py — КРАСИВАЯ АДМИНКА + БЕЗ ОШИБОК!
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRoundFlatButton
from kivymd.app import MDApp
from kivy.metrics import dp  # ← ЭТО НАДО ДОБАВИТЬ!
import sqlite3


class UserItem(TwoLineAvatarIconListItem):
    def __init__(self, user_id, name, email, learned, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.text = f"[b]{name or 'Без имени'}[/b]"
        self.secondary_text = f"{email} • Выучено: {learned} слов"
        self.markup = True

        # Кнопка "Удалить"
        delete_btn = MDRoundFlatButton(
            text="Удалить",
            md_bg_color=(1, 0.3, 0.3, 1),
            text_color=(1, 1, 1, 1),
            size_hint_x=None,
            width=dp(100)  # ← Теперь dp работает!
        )
        delete_btn.bind(on_release=self.delete_user)
        self.add_widget(delete_btn)

        # Кнопка "Сброс"
        reset_btn = MDRoundFlatButton(
            text="Сброс",
            md_bg_color=(1, 0.6, 0, 1),
            text_color=(1, 1, 1, 1),
            size_hint_x=None,
            width=dp(90)   # ← Теперь dp работает!
        )
        reset_btn.bind(on_release=self.reset_progress)
        self.add_widget(reset_btn)

    def delete_user(self, *args):
        conn = sqlite3.connect("data/database.db")
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE id=?", (self.user_id,))
        c.execute("DELETE FROM progress WHERE user_id=?", (self.user_id,))
        conn.commit()
        conn.close()
        MDApp.get_running_app().root.get_screen("admin").refresh_users()

    def reset_progress(self, *args):
        conn = sqlite3.connect("data/database.db")
        c = conn.cursor()
        c.execute("UPDATE progress SET learned=0, streak=0 WHERE user_id=?", (self.user_id,))
        conn.commit()
        conn.close()
        MDApp.get_running_app().root.get_screen("admin").refresh_users()


class AdminScreen(MDScreen):
    def on_enter(self):
        self.refresh_users()

    def refresh_users(self):
        self.ids.user_list.clear_widgets()

        conn = sqlite3.connect("data/database.db")
        c = conn.cursor()
        c.execute("""SELECT u.id, u.name, u.email, COALESCE(p.learned, 0)
                     FROM users u
                     LEFT JOIN progress p ON u.id = p.user_id""")
        users = c.fetchall()
        conn.close()

        if not users:
            self.ids.user_list.add_widget(MDLabel(
                text="Нет пользователей",
                halign="center",
                theme_text_color="Hint",
                font_style="H5"
            ))
            return

        for user_id, name, email, learned in users:
            item = UserItem(user_id, name, email, learned)
            self.ids.user_list.add_widget(item)