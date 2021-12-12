import os
import pickle

# Паціент
class Patient:
    def __init__(self, name, age, gender, diseases, symptoms, visit_date, medication):
        self.name = name
        self.age = age
        self.gender = gender
        self.diseases = diseases
        self.symptoms = symptoms
        self.visit_date = visit_date
        self.medication = medication

is_running = True # Якщо поміняти на False основний цикл завершиться

# Ця функція буде намагатися отримати ціле число, поки воно не буде білше нуля
def force_positive_int(msg):
    i = input(msg)
    while not i.isdigit() or int(i) <= 0:
        if int(i) <= 0: # Число не позитивне
            print("Не може бути <= 0, спробуйте ще раз")
        elif not i.isdigit(): # Взагалі не є числом
            print("Повинно бути числом, спробуйте ще раз")
        i = input()
    return int(i)

# Завантаження базової бази данних
def load_data():
    data = []
    data.append(Patient("Ігор Швайка", 30, "Чоловіча", "Туберкульоз", 
    "Кашель, висока температура", "2021/11/05", "")) # Додаємо в базу пацієнта
    data.append(Patient("Тат'яна Панченко", 21, "Жіноча", "", 
    "Втрата смаку, слабкість", "2021/11/09", ""))
    data.append(Patient("Олександр Охріменко", 44, 
    "Чоловіча", "", "Біль в серці", "", ""))
    return data

# Зберігає інформацію в файл
def save_data(data):
    with open("data.pickle", 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

# Виводить інформацію про назначені візити
def visits(data):
    if len(data) == 0: # База пуста
        print("Інформація порожня")
        return

    print("Назначені візити")
    for p in data: # Для кожного пацієнта
        if p.visit_date != "": # Якщо дата не пуста
            print(f"{p.name} - {p.visit_date}, {p.age} років")

# Виводить повну інформацію про пацієнтів
def patients(data):
    if len(data) == 0: # База пуста
        print("Інформація порожня")
        return
    
    print("Пацієнти")
    for p in data: # Для кожного пацієнта
        print(f"{p.name}")
        print(f"\tвік: {p.age}")
        print(f"\tстать: {p.gender}")
        print(f"\tдіагнози: {p.diseases}")
        print(f"\tсимптоми: {p.symptoms}")

# Реєстрація пацієнта
def register_patient(data):
    print("Реєстрація пацієнта")

    # Отримуємо данні
    name = input("Ім'я: ")
    age = int(force_positive_int("Вік: "))
    gender = input("Стать: ")
    diseases = input("Діагнози: ")
    symptoms = input("Симптоми: ")
    visit_date = ""
    medication = ""

    data.append(Patient(name, age, gender, diseases, symptoms, visit_date, medication)) # Додаємо в базу
    print(f"Створено {name} віком {age}")
    save_data(data)

#  Видаляє пацієнта з бази данних
def remove_patient(data):
    indexes = [] # Список щоб звірити що вибраний індекс не виходить за межі
    print("Виберіть пацієнта або 0 щоб вийти")
    for i, p in enumerate(data, start=1): # індекс з 1 і пацієнт
        print(f"{i}. {p.name}")
        indexes.append(i) # додаємо в список

    i = int(input())
    if i == 0: # Виходимо
        return

    if not i in indexes: # Вибраний індекс за межами, виходимо
        print("Немає пацієнта з таким індексом")
        return

    print(f"Пацієнта {data[i - 1].name} видалено")
    data.pop(i - 1) # Видаляємо пацієнта з бази
    save_data(data)

# Відміняє візит
def cancel_visit(data):
    indexes = [] # Список щоб звірити що вибраний індекс не виходить за межі
    print("Виберіть пацієнта або 0 щоб вийти")
    for i, p in enumerate(data, start=1): # індекс з 1 і пацієнт
        if p.visit_date == "": # Якщо немає візиту, пропускаємо
            continue
        print(f"{i}. {p.visit_date} {p.name}") 
        indexes.append(i) # додаємо в список

    i = int(input())
    if i == 0: # Виходимо
        return

    if not i in indexes: # Вибраний індекс за межами, виходимо
        print("Немає візиту з таким індексом")
        return

    print(f"Візит {data[i - 1].visit_date} відмінено")
    data[i - 1].visit_date = "" # Видаляємо візит
    save_data(data)

# Створити візит
def schedule_visit(data):
    indexes = [] # Список щоб звірити що вибраний індекс не виходить за межі
    print("Виберіть пацієнта або 0 щоб вийти")
    for i, p in enumerate(data, start=1):
        if p.visit_date != "":
            continue
        print(f"{i}. {p.visit_date} {p.name}") 
        indexes.append(i) # додаємо в список

    
    i = int(input()) 
    if i == 0: # Виходимо
        return

    if not i in indexes: # Вибраний індекс за межами, виходимо
        print("Немає візиту з таким індексом")
        return
        
    print("Введіть дату у форматі рррр/мм/дд")
    date = input("дата: ")
    data[i - 1].visit_date = date # Замінюємо дату
    print("Візит створено")
    save_data(data)

# Виписати ліки
def prescribe_medication(data):
    indexes = [] # Список щоб звірити що вибраний індекс не виходить за межі
    print("Виберіть пацієнта або 0 щоб вийти")
    for i, p in enumerate(data, start=1):
        print(f"{i}. {p.visit_date} {p.name}") 
        indexes.append(i) # додаємо в список

    i = int(input()) 
    if i == 0: # Виходимо
        return

    if i < 1 or i > len(data): # Вибраний індекс за межами, виходимо
        print("Немає візиту з таким індексом")
        return
        
    print("Введіть нові ліки: ")
    medication = input("->: ")
    data[i - 1].medication = medication# Замінюємо ліки
    save_data(data)

# Виводить опис до команд
def help():
    print("1. - Показує дату візитів")
    print("2. - Пацієнти повну інформацію про зареєстрованих пацієнтів")
    print("3. - Реєстрація пацієнта в базу данних")
    print("4. - Створити візит")
    print("5. - Видалити пацієнта з бази данних")
    print("6. - Відмінити візит")
    print("8. - Виводить цей текст")
    print("9. - Виводить ім'я та інші дані про розробника")
    print("0. - Завершити програму")
    
# Виводить інформацію про розробника
def about():
    print("Розроблено Д. Колібабчуком")
    print("Група Б2, потік-1")

# Вихід з програми
def exit():
    global is_running
    is_running = False
    print("Програму завершено")

# Основий цикл
def loop(data):
    print()
    i = input("Оберіть пункт в меню ->")
    print()
    if i == "1": # Показати візити
        visits(data)
    if i == "2": # Показати інформацію про пацієнтів
        patients(data)
    if i == "3": # Зареєструвати пацієнта
        register_patient(data)
    if i == "4": # Створити візит
        schedule_visit(data)
    if i == "5": # Видалення пацієнта за бази
        remove_patient(data)
    if i == "6": # Відмінити візит
        cancel_visit(data)
    if i == "7": # Виписати ліки
        prescribe_medication(data)
    if i == "8": # Показати допомогу
        help()
    if i == "9": # Показати інформацію про розробника
        about()
    if i == "0": # Вийти з программи
        exit()

def main():
    print("------------------------------")
    print("Програма  'Помічник Лікаря'")
    print("Розроблено Д. Колібабчуком")
    print("-----------------------------")
    print("1. Назначені візити")
    print("2. Пацієнти")
    print("3. Зареєструвати пацієнта")
    print("4. Створити візит")
    print("5. Видалити пацієнта з бази данних")
    print("6. Відмінити візит")
    print("7. Виписати ліки")
    print("8. Показати список команд та їх опис")
    print("9. Про програму")
    print("0. Вихід")

    data = load_data()
    while is_running:
        loop(data)

main()
