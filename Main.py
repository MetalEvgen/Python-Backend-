import random
import sqlite3
from getpass import getpass
import textwrap
from idlelib.run import exit_now
from os import close
#Импорт библиотек для проекта
#_________________________________________________________________________
# => Блок функций. Функции запускаются из меню посредством стартовой команды

def all_books(): # => Функция отображения всех книг библиотеки
    BD2 = sqlite3.connect("Biblioteka.db")
    cursor = BD2.cursor()
    cursor.execute('''
    SELECT * FROM biblio''')
    resultat = cursor.fetchall()
    for book in resultat:
        print(f" * {book[2]} - {book[1]} - {book[6]}")
    BD2.close()

def repeat_or_back(): # => Функция повтора загрузки
    while True:
        try:
            x = int(input(" 1 - Повторить загрузку книг\n"" 2 - Возврат в главное
меню\n"))
        except ValueError:
            print("Неверная команда")
            continue
        if x == 1:
            add_book()
        elif x == 2:
            main()


def passbackup(): # => Функция восстановления пароля
    print("Забыли пароль?\n Введите <Логин учетной записи> и <Кодовое слово>: ")
    l = input("Логин: ")
    cw = getpass("Кодовое слово: ")
    BD = sqlite3.connect("Users.db")
    cursor = BD.cursor()
    cursor.execute('''
    SELECT PASSWORD FROM users WHERE NAME = ? AND CODEWORD = ?
    ''', (l, cw))
    result = cursor.fetchone()
    if result:
        print(f"Учетная запись проверена. Пароль: {result[0]}")
        login()
    else:
        print("Кодовое слово не верное")
        while True:
            try:
                x = int(input(" 1 - Повторить восстановление пароля\n 2 - Выход в главное
меню:\n "))
            except ValueError:
                print("Введите значения 1 - 2")
                continue
            if x == 1:
                print("----------------------")
                passbackup()
            elif x == 2:
                print("----------------------")
                login()
        BD.close()
        
def back_or_not(): # => Функция повтора или выхода в главное меню
    while True:
        try:
            x = int(input(" 1 - Повторить поиск книги\n"" 2 - Возврат в главное меню "))
        except ValueError:
            print("Неверная команда")
            continue
        if x == 1:
            search_book()
        elif x == 2:
            main()
            break


def Database_books(): # => Создание базы данных Книги
    BD2 = sqlite3.connect("Biblioteka.db")
    cursor = BD2.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS biblio(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    AUTHOR TEXT,
    NAME TEXT,
    YEAR TEXT,
    PREVIEW TEXT,
    file BLOB
    )
    ''')
    BD2.commit()
    BD2.close()
    
def Database(): # => Cоздание базы данных Учетные записи
    BD = sqlite3.connect("Users.db")
    cursor = BD.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME TEXT,
    PASSWORD TEXT,
    CODEWORD TEXT,
    )
    ''')
    BD.commit()
    BD.close()


def random_book(): # => Функция показа рандомизации для отображения книг дня
    BD2 = sqlite3.connect("Biblioteka.db")
    cursor = BD2.cursor()
    cursor.execute("SELECT NAME, AUTHOR, GENRE, PREVIEW FROM biblio
                    ORDER BY RANDOM() LIMIT 1")
    bk = cursor.fetchone()
    print(f" * Название: {bk[0]}")
    print(f" * Автор: {bk[1]}")
    print(f" * Жанр: {bk[2]}")
    print("---------------------------------")
    while True:
        try:
            y = int(input("Хотите прочитать описание?\n 1 - Открыть\n 2 - Нет\n "))
        except ValueError:
            print("Неверная команда")
            continue
        if y == 1:
            print("Открываю описание книги ^_^")
            print("---------------------------")
            text = textwrap.fill(f"{bk[3]}",width =50)
            print(text)
            break
        elif y == 2:
            print("---------------------------")
            print("Переход в главное меню")
            print("---------------------------")
            break
        else:
            print("Неверная команда")
            break
BD2.close()


def add_book(): # => Функция добавления книг в библиотеку.
    BD2 = sqlite3.connect("Biblioteka.db")
    cursor = BD2.cursor()
    author_book = input("Автор: ").strip()
    name_book = input("Название: ").strip()
    year = input("Год выпуска: ").strip()
    genre = input("Жанр: ").strip()
    cursor.execute('''
    SELECT 1 FROM biblio WHERE AUTHOR = ? AND NAME = ? AND YEAR = ? AND GENRE = ?
    ''', (author_book, name_book, year, genre))
    result = cursor.fetchone()
    if result:
        print("Данная книга уже есть в каталоге библиотеки")
        print(result)
        BD2.close()
        repeat_or_back()
    else:
        cursor.execute('''
        INSERT INTO biblio (AUTHOR, NAME, YEAR, GENRE)
        VALUES ( ?, ?, ?, ?)
        ''', (author_book, name_book, year, genre))
        BD2.commit()
        BD2.close()
        print("Книга успешно добавлена в библиотеку!")
        repeat_or_back()
        
def search_book(): # => Функция поиска книг с полем ввода
    BD2 = sqlite3.connect("Biblioteka.db")
    cursor = BD2.cursor()
    s = input("Поиск книги по атрибутам: ")
    cursor.execute('''
    SELECT * FROM biblio
    WHERE AUTHOR LIKE (?) OR NAME LIKE (?) OR YEAR LIKE(?)
    ''', (f"%{s}%",f"%{s}%",f"%{s}%"))
    resultat = cursor.fetchall()
    if resultat:
        print("Результат поиска: ")
        for book in resultat:
            print("-----------------------")
            print(f" * Автор: {book[1]}")
            print(f" * Название: {book[2]}")
        back_or_not()
    else:
        print("Книга не найдена")
        back_or_not()
    BD2.close()


def text_load(): # => Функция вывода текста при загрузке приложения
    txt = ["=> Учение свет! <=",
           "=> Учиться, учиться и еще раз учиться! <=",
           "=> Загрузка программы... <=",
           "=> Терпение и труд все перетрут! <= ",
            ]
    print(random.choice(txt))
text_load()

# => Отображение приветственного сообщения с названием программы
print("
print("
print("
print("
  Выпускная квалификационная работа")
       Студент 4 курса Балашов Е.Р.")
                 Группа ООБИ-22091с")
Московский Технологический Институт")
print("------------------------------------------------------------------------")
print("     Вас приветствует Информационная Система", "< Книжная Библиотека >  ")
print("------------------------------------------------------------------------")
def start(): # => Запуск подключения к базе данных Учетные записи
    try:
        # Подключение к базе данных
        BD = sqlite3.connect("Users.db")
        cursor = BD.cursor()
        # Получение данных от пользователя
        log = input("Введите логин: ").strip()
        pas = getpass("Введите пароль: ").strip()
        # Выполнение запроса
        cursor.execute('''
            SELECT PASSWORD
            FROM users
            WHERE NAME = ?
        ''', (log,))  # Здесь нужен запятая для создания кортежа
        resultat = cursor.fetchone()
        if resultat:
            # Правильное получение значения из результата
            stored_password = resultat[0]
            if stored_password == pas:
                print("Успешная авторизация!")
main() else:
                print("Ошибка: неверный пароль!")
                passbackup()
        else:
            print("Пользователь не найден!")
            reg = int(input("Нет учетной записи?\n 1 - Регистрация пользователя\n 2 -
Возврат в главное меню\n "))
            if reg == 1:
                add_user()
            elif reg == 2:
                login()
            else:
                print(">Нераспознанная команда<")
                login()
    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        # Гарантированное закрытие соединения
        if BD:
            BD.close()
    return False
55

 def add_user(): # => Функция регистрации пользователя в базе данных "Учетные записи"
    BD = sqlite3.connect("Users.db")
    cursor = BD.cursor()
    log = input("Введите логин: ")
    def dubl():
        cursor.execute('''
        SELECT * FROM users WHERE NAME = ?''', (log,))
        result = cursor.fetchall()
        if result:
            print("Логин недоступен")
            print("Попробуйте снова ^_^")
            add_user()
        else:
            print("Успех! Логин свободен!")
            pas = getpass("Введите пароль пользователя: ").strip()
            code_word = getpass("Введите кодовое слово для восстановления пароля: \n")
            cursor.execute('''
            INSERT INTO users (NAME,PASSWORD,CODEWORD)
            VALUES (?,?,?)
            ''', (log, pas, code_word))
            BD.commit()
            BD.close()
            print("Успешная регистрация пользователя!")
dubl()
def login(): # => Функция выбора Вход или Регистрации
    while True:
        try:
            x = int(input(" 1 - Вход в программу\n 2 - Регистрация пользователя\n" ))
        except ValueError:
            print("Неверная команда")
            continue
        if x == 1:
            start()
            break
        elif x == 2:
            add_user()
            login()
            break
56

 # => Основной блок программы. Здесь происходит выбор блоков для выполнения функций
def main(): # => Функция основного блока выбора модулей
    Database_books()
    print("--------------------------------------------------------------------")
    print("                    Добро пожаловать в систему!                     ")
    print("--------------------------------------------------------------------")
    print("               Подборка интересной книги на сегодня:                ")
    random_book()
    def menu():
        while True:
            print("---------------------------")
            print("Доступные разделы:\n 1 - Каталог книг \n 2 - Поиск книг\n 3 - Загрузка
книг\n 4 - Выход из программы\n " )

try:
    block = int(input("Выберите раздел: "))
except ValueError:
    print("Ошибка! Введите чисто от 1 до 4")
    continue
if block == 1:
    print("1 - Каталог")
    all_books()
elif block == 2:
    print("2 - Поиск книг в библиотеке")
    search_book()
elif block == 3:
    print("3 - Загрузка книг")
    add_book()
elif block == 4:
    print(" 4 - Закрытие программы\n Возвращайтесь к нам снова ^_^")
    break
else:
    print("Некорректная команда")
    
    menu()
    
login()
