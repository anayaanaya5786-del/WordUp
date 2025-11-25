# screens/ai_cards.py
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
import random

class AICardsScreen(MDScreen):
    words = {
        "Hello": "привет",
        "Cat": "кот",
        "Dog": "собака",
        "Love": "любовь",
        "Water": "вода",
        "Book": "книга",
        "Sun": "солнце",
        "Friend": "друг",
        "Happy": "счастливый",
        "Good morning": "доброе утро",
        "Thank you": "спасибо",
        "House": "дом"
    }

    def on_enter(self):
        self.show_new_word()

    def show_new_word(self):
        self.current_eng = random.choice(list(self.words.keys()))
        self.correct = self.words[self.current_eng]
        self.ids.word_label.text = f"[b]{self.current_eng}[/b]\nКак будет по-русски?"
        self.ids.answer_field.text = ""
        self.ids.result_label.text = ""

    def check_answer(self, *args):
        user_answer = self.ids.answer_field.text.strip().lower()
        if not user_answer:
            self.ids.result_label.text = "[color=#FF9800]Напиши ответ![/color]"
            return

        if user_answer == self.correct.lower() or self.correct.lower() in user_answer:
            self.ids.result_label.text = f"[color=#00C853]Правильно! ✓[/color]\n[b]{self.correct.capitalize()}[/b]"
            MDApp.get_running_app().increase_learned()
        else:
            self.ids.result_label.text = f"[color=#F44336]Неправильно ✗[/color]\nПравильно: [b]{self.correct.capitalize()}[/b]"

        # Через 2 секунды — новое слово
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: self.show_new_word(), 2.5)