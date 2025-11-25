from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCardSwipe
from kivymd.uix.label import MDLabel

class FlashCard(MDCardSwipe):
    def on_swipe_complete(self, direction):
        if direction == "right":
            print("Знаю!")
        else:
            print("Не знаю :(")
        self.parent.parent.show_next()

class FlashcardsScreen(MDScreen):
    words = [("hello", "привет"), ("cat", "кошка"), ("dog", "собака"), ("water", "вода")]
    current = 0

    def on_enter(self):
        self.show_next()

    def show_next(self):
        if self.current >= len(self.words):
            self.ids.stack.add_widget(MDLabel(text="Урок завершён!", font_style="H2"))
            return

        card = FlashCard()
        card.add_widget(MDLabel(
            text=self.words[self.current][0],
            font_style="H4",
            halign="center"
        ))
        self.ids.stack.clear_widgets()
        self.ids.stack.add_widget(card)
        self.current += 1