from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
import sqlite3

class StatsScreen(MDScreen):
    def on_enter(self):
        app = MDApp.get_running_app()
        conn = sqlite3.connect(app.db_path)
        c = conn.cursor()
        c.execute("SELECT streak, learned FROM progress WHERE user_id=?", (app.current_user,))
        stats = c.fetchone() or (0, 0)
        conn.close()
        self.ids.stats_label.text = f"Стрик: {stats[0]} дней\nВыучено: {stats[1]} слов\nКатегория: {app.selected_category}"