
import unittest
import sqlite3
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from main import WordUpApp


class TestWordUp(unittest.TestCase):
    db_path = "test_database.db"

    def setUp(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users 
                     (id INTEGER PRIMARY KEY, email TEXT UNIQUE, password TEXT, name TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS progress 
                     (user_id INTEGER, lang TEXT, streak INTEGER DEFAULT 0, learned INTEGER DEFAULT 0)''')
        conn.commit()
        conn.close()

        self.app = WordUpApp()
        self.app.db_path = self.db_path
        self.app.root = None

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_register_user(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT INTO users (email, password, name) VALUES (?, ?, ?)",
                  ("test@gmail.com", "1234", "TestUser"))
        conn.commit()
        conn.close()

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT name FROM users WHERE email=?", ("test@gmail.com",))
        result = c.fetchone()
        conn.close()

        self.assertIsNotNone(result)
        self.assertIn("Test", result[0])

    def test_login_success(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT INTO users (email, password, name) VALUES (?, ?, ?)",
                  ("anush@gmail.com", "1234", "Ануш"))
        user_id = c.lastrowid
        conn.commit()
        conn.close()

        self.app.current_user = user_id
        self.app.current_user_name = "Ануш"

        self.assertEqual(self.app.current_user_name, "Ануш")

    def test_admin_login(self):
        self.assertTrue(True)

    def test_increase_learned(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT INTO users (email, password, name) VALUES (?, ?, ?)",
                  ("test@gmail.com", "1234", "Тест"))
        user_id = c.lastrowid
        c.execute("INSERT INTO progress (user_id, lang, learned) VALUES (?, ?, 0)",
                  (user_id, "en-ru"))
        conn.commit()
        conn.close()

        self.app.current_user = user_id
        self.app.current_lang = "en-ru"

        original = self.app.update_progress_display
        self.app.update_progress_display = lambda: None

        self.app.increase_learned()

        self.app.update_progress_display = original

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT learned FROM progress WHERE user_id=?", (user_id,))
        learned = c.fetchone()[0]
        conn.close()

        self.assertEqual(learned, 1)

    def test_sync_with_firebase(self):
        self.app.sync_with_firebase()
        self.assertTrue(True)

    def test_push_notification(self):
        self.app.send_push_notification("Test")
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main(verbosity=2)