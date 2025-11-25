# screens/categories.py
from kivymd.uix.screen import MDScreen
from compatibility import TwoLineIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.app import MDApp

class CategoryItem(TwoLineIconListItem):
    pass

class CategoriesScreen(MDScreen):
    def on_pre_enter(self):
        self.ids.cat_list.clear_widgets()
        cats = [
            ("Oxford 3000 & 5000", "book"),
            ("Здоровье", "heart-pulse"),
            ("Базовые глаголы", "run"),
            ("Бизнес", "briefcase"),
            ("Внешность", "face-man"),
            ("Еда", "food-apple"),
            ("Идиомы", "lightbulb-on"),
            ("Маркетинг", "chart-line"),
            ("Компьютер", "laptop"),
            ("Психология", "brain"),
            ("Фразовые глаголы", "arrow-up-down"),
            ("Экономика", "currency-usd"),
            ("Экология", "leaf"),
        ]
        for name, icon in cats:
            item = CategoryItem(text=name, secondary_text="0 слов")
            item.add_widget(MDCheckbox(size_hint=(None, None), size=(50,50), pos_hint={"center_y": .5}))
            item.bind(on_release=lambda x, n=name: self.select_cat(n))
            self.ids.cat_list.add_widget(item)

    def select_cat(self, name):
        app = MDApp.get_running_app()
        app.selected_category = name
        app.root.current = "practice"