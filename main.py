import json
from difflib import get_close_matches
from getpass import getpass
import re

# Загрузить базу знаний из файла
def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

# Сохранить базу знаний в файл
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

# Нормализовать вопрос
def normalize_question(question: str) -> str:
    question = question.lower()  # Привести к нижнему регистру
    question = re.sub(r'\W+', ' ', question)  # Удалить знаки препинания
    return question.strip()

# Найти лучший совпадающий вопрос
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    normalized_user_question = normalize_question(user_question)
    normalized_questions = [normalize_question(q) for q in questions]
    matches = get_close_matches(normalized_user_question, normalized_questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

# Получить ответ на вопрос
def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if normalize_question(q["question"]) == question:
            return q["answer"]

# Основная функция чат-бота
def chat_bot():
    knowledge_base = load_knowledge_base("knowledge_base.json")
    correct_password = "123"

    while True:
        user_input = input('You: ')
        print(f"User input: {user_input}")

        if user_input.lower() == 'quit':
            break

        best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])
        print(f"Best match: {best_match}")

        if best_match:
            answer = get_answer_for_question(best_match, knowledge_base)
            print(f'Bot: {answer}')
        else:
            print('Bot: I don\'t know the answer. Can you teach me?')
            print('Enter password to teach the bot:')
            password = input('Password: ')
            print(f"Entered password: {password}")

            if password == correct_password:
                new_answer = input('Type the answer or "skip" to skip: ')
                print(f"New answer: {new_answer}")

                if new_answer.lower() != 'skip':
                    knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                    save_knowledge_base('knowledge_base.json', knowledge_base)
                    print('Bot: Thank you! I learned a new response')
            else:
                print('Bot: Incorrect password. Cannot learn new response.')

if __name__ == '__main__':
    chat_bot()