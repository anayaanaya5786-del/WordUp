from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCardSwipe
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from screens.dictionary import DictionaryScreen

class FlashCard(MDCardSwipe):
    def on_swipe_complete(self, direction):
        if direction == "right":
            print("Знаю!")
            MDApp.get_running_app().increase_learned()
        else:
            print("Не знаю :(")
        self.parent.parent.show_next()

class FlashcardsScreen(MDScreen):
    words = []
    current = 0

    def load_lesson(self, category, lesson):
        app = MDApp.get_running_app()
        lang = app.current_lang
        all_words = DictionaryScreen.oxford_words.get(lang, {}).get(category, [])
        self.words = [(w, t, l) for w, t, l in all_words if lesson in w]  # Фильтр
        self.current = 0
        self.show_next()

    def on_enter(self):
        if not self.words:
            self.load_lesson("A1", "All")

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