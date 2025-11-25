# ai/trainer.py
from transformers import pipeline
import torch

# Лёгкая модель (работает даже на телефоне!)
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
    device=0 if torch.cuda.is_available() else -1
)

def is_correct_answer(user_answer: str, correct_word: str, tolerance=0.85):
    if correct_word.lower() in user_answer or user_answer == correct_word.lower():
        return True

    result = classifier(user_answer, [correct_word, "неправильный перевод", "другое слово"])
    return result['labels'][0].lower() == correct_word.lower() and result['scores'][0] > tolerance

# Тест
# print(is_correct_answer("яблочко", "яблоко")) → True
# print(is_correct_answer("собака", "яблоко")) → False