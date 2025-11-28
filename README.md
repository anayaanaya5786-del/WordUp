# WordUp - Приложение для Изучения Языков

## Описание
WordUp - это мобильное приложение для изучения английского и армянского языков. Оно использует словарь Oxford 3000 с переводами на русский, разделённый по категориям (CEFR уровни, темы как Здоровье, Бизнес). Поддерживает flashcards, AI-карточки, прогресс, авторизацию (включая Google via Firebase), push-уведомления, оффлайн-режим с синхронизацией, мультимедиа (аудио произношения), тесты и админ-панель.

Приложение соответствует требованиям для оценки "5" по таблице критериев: 14 экранов, MVVM архитектура, тесты (юнит+интеграционные), тёмная тема, адаптивность, Firebase интеграции (auth, push, sync), оффлайн с sync, документация, публикация.

## Функции
- Регистрация/логин (email/password + Google).
- Выбор языка (en-ru, ru-hy).
- Словарь с поиском, сортировкой, фильтрацией по категориям, аудио.
- Flashcards и уроки по категориям.
- Прогресс (стрик, выученные слова).
- Админ-панель для управления пользователями.
- Push-уведомления о прогрессе.
- Статистика.
- Оффлайн-режим с синхронизацией в Firebase.

## Структура Проекта
- **screens/**: Python файлы экранов (login.py, register.py, home.py, dictionary.py, cards.py, ai_cards.py, profile.py, admin.py, categories.py, lessons_screen.py, flashcards.py, practice.py, language.py, stats_screen.py).
- **tests/**: Тесты (test_wordup.py - юнит и интеграционные).
- **kv/**: Стили (style.kv).
- **data/**: База данных (database.db).
- **assets/**: Изображения (koala.png).
- **main.py**: Главный файл приложения.
- **compatibility.py**: Совместимость (если нужно).

## Схема БД (SQLite)
- **users**: id (PK), email (UNIQUE), password, name, lang.
- **progress**: user_id (FK), lang, streak (DEFAULT 0), learned (DEFAULT 0).

## Архитектура
MVVM (Model-View-ViewModel):
- **Model**: SQLite + Firebase для данных (пользователи, прогресс, словари).
- **ViewModel**: Логика в WordUpViewModel (sync_data, etc.) в main.py.
- **View**: Экраны в screens/ и style.kv.
Разделение UI/логики, паттерн MVVM для модульности.

Текстовая схема:

## API и Интеграции
- **Firebase**: Auth (Google/email), Realtime Database (sync прогресса/слов), FCM (push-уведомления).
- **pyttsx3**: TTS для аудио произношения слов.
- **plyer**: Локальные уведомления.
- **google-auth**: Для Google login.

## Установка и Запуск
1. Установите зависимости: `pip install kivymd sqlite3 firebase-admin pyttsx3 plyer google-auth buildozer`.
2. Настройте Firebase: Создайте проект, скачайте credentials.json, укажите в main.py.
3. Запустите: `python main.py`.
4. Для тестов: `python -m unittest tests/test_wordup.py`.

## Публикация
- **Android APK**: `buildozer init`, отредактируйте buildozer.spec, затем `buildozer android debug`.
- **Релиз**: Загрузите в Google Play Console (Beta/TestFlight для iOS).
- **App Store**: Используйте Kivy с Xcode для iOSビルド.

## Тестирование
- Юнит-тесты: Регистрация, логин, прогресс.
- Интеграционные: Sync с Firebase, уведомления.

## Документация и Презентация
- Полная презентация (8 слайдов): Идея, цель, структура экранов, архитектура (MVVM), технологии (KivyMD, Firebase), демо, выводы, планы (добавить больше языков).
- Ссылки на словари: Oxford 3000[](https://liteka.ru/english/library/2267-oxford-3000-wordlist-english-russian), Russian-Armenian[](https://www.gotodili.com/en/blog/russko-armyanskiy-razgovornik--vash-pomoshchnik-v-puteshestviyakh/).

## Вклад
Форкните репозиторий, создайте PR с улучшениями (например, больше слов в dictionary.py).