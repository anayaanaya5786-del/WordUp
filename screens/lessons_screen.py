from compatibility import MDRoundFlatButton
from kivymd.uix.screen import MDScreen


class LessonsScreen(MDScreen):
    current_category = "Еда"

    def on_enter(self):
        box = self.ids.lessons_box
        box.clear_widgets()

        lessons = {
            "Еда": ["Фрукты", "Овощи", "Напитки"],
            "Путешествия": ["Аэропорт", "Отель", "Транспорт"],
        }[self.current_category]

        for l in lessons:
            btn = MDRoundFlatButton(text=l, size_hint_y=None, height=80)
            btn.bind(on_release=lambda x, lesson=l: self.open_flashcards(lesson))
            box.add_widget(btn)

    def open_flashcards(self, lesson):
        self.manager.get_screen('flashcards').load_lesson(self.current_category, lesson)
        self.manager.current = 'flashcards'