# screens/cards.py
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.animation import Animation
from kivy.core.window import Window
import random

class CardsScreen(MDScreen):
    # Твои слова
    words = [
        ("Hello", "Привет"),
        ("Cat", "Кот"),
        ("Love", "Любовь"),
        ("Water", "Вода"),
        ("Book", "Книга"),
        ("Friend", "Друг"),
        ("Good", "Хороший"),
        ("House", "Дом"),
        ("Sun", "Солнце"),
        ("Happy", "Счастливый"),
    ]

    def on_enter(self):
        self.show_new_card()

    def show_new_card(self):
        self.current_word, self.translation = random.choice(self.words)
        self.ids.word_label.text = self.current_word
        # Возвращаем карточку в центр
        self.ids.card.pos_hint = {"center_x": .5, "center_y": .5}

    def swipe_left(self, *args):
        # Не знаю — улетает влево
        anim = Animation(x=-Window.width*2, duration=0.4)
        anim.bind(on_complete=lambda *x: self.show_new_card())
        anim.start(self.ids.card)

    def swipe_right(self, *args):
        # Знаю — улетает вправо + зелёная галочка
        app = MDApp.get_running_app()
        app.increase_learned()
        self.ids.word_label.text = f"{self.current_word}\n[size=60][color=#00C853]✓[/color][/size]\n{self.translation}"
        anim = Animation(x=Window.width*2, duration=0.4)
        anim.bind(on_complete=lambda *x: self.show_new_card())
        anim.start(self.ids.card)