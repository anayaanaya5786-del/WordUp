# screens/dictionary.py
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import TwoLineListItem
from kivymd.app import MDApp
import pyttsx3  # Для TTS аудио

class DictionaryScreen(MDScreen):
    # Большой Oxford 3000 (пример из источников; полный - скачайте и добавьте)
    oxford_words = {
        "en-ru": {
            "A1": [  # Пример из извлечённых данных
                ("a", "а", "A1"),
                ("about", "о", "A1"),
                ("above", "выше", "A1"),
                ("abroad", "за границей", "A1"),
                ("absence", "отсутствие", "A1"),
                ("absent", "отсутствовать", "A1"),
                ("absolute", "абсолютный", "A1"),
                ("absorb", "поглощать", "A1"),
                ("abuse", "злоупотребление", "A1"),
                ("academic", "учебный", "A1"),
                ("accent", "акцент", "A1"),
                ("acceptable", "приемлемый", "A1"),
                ("access", "доступ", "A1"),
                ("accident", "несчастный случай", "A1"),
                ("abandon", "отказываться от", "A1"),
                ("a bit", "немного", "A1"),
                ("a few", "несколько", "A1"),
                ("because of", "из-за", "A1"),
                ("rely on", "рассчитывать на", "A1"),
                ("worried", "беспокоило", "A1"),
                ("crowded", "переполненный", "A1"),
                ("depressed", "угнетенный", "A1"),
                ("deserted", "пустынный", "A1"),
                ("detailed", "подробный", "A1"),
                ("determined", "определяется", "A1"),
                ("devoted", "посвященный", "A1"),
                ("disabled", "инвалид", "A1"),
                ("disappointed", "разочарованный", "A1"),
                ("disgusted", "противно", "A1"),
                ("divorced", "разведенный", "A1"),
                ("dressed", "одетый", "A1"),
                ("edge", "край", "A1"),
                ("edition", "издание", "A1"),
                ("editor", "редактор", "A1"),
                ("educate", "воспитывать", "A1"),
                ("education", "образование", "A1"),
                ("embarrassed", "смущенный", "A1"),
                ("federal", "федеральный", "A1"),
                ("feed", "кормить", "A1"),
                ("confused", "спутанный", "A1"),
                ("controlled", "управляемый", "A1"),
                ("curved", "изогнутый", "A1"),
                ("engaged", "занято", "A1"),
                ("immediate", "немедленный", "A1"),
                ("infected", "зараженный", "A1"),
                ("ingredient", "ингредиент", "A1"),
                ("injured", "пострадавший", "A1"),
                ("interested", "заинтересованный", "A1"),
                ("knitted", "вязаный", "A1"),
                ("married", "женат", "A1"),
                ("medicine", "медицина", "A1"),
                ("medium", "средний", "A1"),
                ("mixed", "смешанный", "A1"),
                ("naked", "голый", "A1"),
                ("need", "необходимость", "A1"),
                ("needle", "игла", "A1"),
                ("occupied", "занятый", "A1"),
                ("opposed to", "против", "A1"),
                # Добавьте больше из полного списка (около 3000 слов) из https://www.scribd.com/document/649166061/Oxford-3000-English-Russian или VK PDF
            ],
            "Health": [  # Пример категории
                ("doctor", "врач", "B1"),
                ("medicine", "лекарство", "B1"),
                # Добавьте
            ],
            # Другие категории: Business, Food и т.д.
        },
        "ru-hy": {  # Русский-Армянский (пример common words из источников)
            "Basic": [
                ("привет", "Բարև"),
                ("кот", "Կատու"),
                ("собака", "Շուն"),
                ("любовь", "Սեր"),
                ("дом", "Տուն"),
                ("вода", "Ջուր"),
                ("книга", "Գիրք"),
                ("солнце", "Արև"),
                ("друг", "Ընկեր"),
                ("счастливый", "Երջանիկ"),
                ("доброе утро", "Բարի առավոտ"),
                ("спасибо", "Շնորհակալություն"),
                ("да", "Այո"),
                ("нет", "Ոչ"),
                ("пожалуйста", "Խնդրեմ"),
                ("извините", "Ներողություն"),
                ("как дела", "Ինչպես ես"),
                ("хорошо", "Լավ"),
                ("плохо", "Վատ"),
                ("еда", "Ուտելիք"),
                # Добавьте больше (около 55000 из книг, см. Amazon; или Glosbe API для полного)
            ],
            "Health": [
                ("врач", "Բժիշկ"),
                ("лекарство", "Դեղ"),
                # Добавьте
            ],
        }
    }

    def on_enter(self):
        self.load_words()

    def load_words(self, category=None, sort_by="alpha"):
        app = MDApp.get_running_app()
        lang = app.current_lang
        words = self.oxford_words.get(lang, {}).get(category or "A1", [])
        if sort_by == "alpha":
            words.sort(key=lambda x: x[0])
        self.ids.word_list.clear_widgets()
        for word, trans, level in words:
            item = TwoLineListItem(text=f"[b]{word} ({level})[/b]", secondary_text=trans)
            item.markup = True
            item.bind(on_release=lambda x, w=word: self.play_audio(w))
            self.ids.word_list.add_widget(item)

    def search(self, text, category=None):
        if not text.strip():
            self.load_words(category)
            return
        app = MDApp.get_running_app()
        lang = app.current_lang
        words = self.oxford_words.get(lang, {}).get(category or "All", [])
        self.ids.word_list.clear_widgets()
        for word, trans, level in words:
            if text.lower() in word.lower() or text.lower() in trans.lower():
                item = TwoLineListItem(text=f"[b]{word} ({level})[/b]", secondary_text=trans)
                item.markup = True
                self.ids.word_list.add_widget(item)

    def play_audio(self, word):
        engine = pyttsx3.init()
        engine.say(word)
        engine.runAndWait()