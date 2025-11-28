from compatibility import MDRoundFlatButton
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp

class LessonsScreen(MDScreen):
    current_category = "Oxford 3000 & 5000"

    def on_enter(self):
        box = self.ids.lessons_box
        box.clear_widgets()

        lessons = {
            "Oxford 3000 & 5000": ["A1 Words", "A2 Verbs", "B1 Idiom"],
            "Здоровье": ["Body Parts", "Diseases", "Medicine"],
            # Добавьте для армянского
        }.get(self.current_category, [])

        for l in lessons:
            btn = MDRoundFlatButton(text=l, size_hint_y=None, height=80)
            btn.bind(on_release=lambda x, lesson=l: self.open_flashcards(lesson))
            box.add_widget(btn)

    def open_flashcards(self, lesson):
        app = MDApp.get_running_app()
        flashcards_screen = app.root.get_screen('flashcards')
        flashcards_screen.load_lesson(self.current_category, lesson)
        app.root.current = 'flashcards'