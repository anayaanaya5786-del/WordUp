# screens/dictionary.py
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import TwoLineListItem
from kivymd.app import MDApp

class DictionaryScreen(MDScreen):
    words = {
        "en-ru": [
            ("Hello", "Привет"), ("Love", "Любовь"), ("Friend", "Друг"),
            ("Family", "Семья"), ("House", "Дом"), ("Water", "Вода"),
            ("Book", "Книга"), ("Sun", "Солнце"), ("Cat", "Кот"),
            ("Dog", "Собака"), ("Happy", "Счастливый"), ("School", "Школа"),
        ],
        "ru-hy": [
            ("Привет", "Բարև"), ("Любовь", "Սեր"), ("Друг", "Ընկեր"),
            ("Семья", "Ընտանիք"), ("Дом", "Տուն"), ("Вода", "Ջուր"),
        ]
    }

    def on_enter(self):
        self.load_words()

    def load_words(self):
        app = MDApp.get_running_app()
        lang = app.current_lang
        words = self.words.get(lang, [])
        self.ids.word_list.clear_widgets()
        for word, trans in words:
            item = TwoLineListItem(text=f"[b]{word}[/b]", secondary_text=trans)
            item.markup = True
            self.ids.word_list.add_widget(item)

    def search(self, text):
        if not text.strip():
            self.load_words()
            return
        app = MDApp.get_running_app()
        lang = app.current_lang
        words = self.words.get(lang, [])
        self.ids.word_list.clear_widgets()
        for word, trans in words:
            if text.lower() in word.lower() or text.lower() in trans.lower():
                item = TwoLineListItem(text=f"[b]{word}[/b]", secondary_text=trans)
                item.markup = True
                self.ids.word_list.add_widget(item)