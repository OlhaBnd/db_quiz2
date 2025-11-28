import sqlite3

db_name = 'quiz.sqlite'

def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

def close():
    cursor.close()
    conn.close()

def do(query, params=()):
    cursor.execute(query, params)
    conn.commit()

# ------------------------------
# Створення таблиць
# ------------------------------
def create():
    open()
    cursor.execute('PRAGMA foreign_keys=on')

    do('''CREATE TABLE IF NOT EXISTS quiz (
           id INTEGER PRIMARY KEY,
           name VARCHAR)''')

    do('''CREATE TABLE IF NOT EXISTS question (
           id INTEGER PRIMARY KEY,
           question VARCHAR,
           answer VARCHAR,
           wrong1 VARCHAR,
           wrong2 VARCHAR,
           wrong3 VARCHAR)''')

    do('''CREATE TABLE IF NOT EXISTS quiz_content (
           id INTEGER PRIMARY KEY,
           quiz_id INTEGER,
           question_id INTEGER,
           FOREIGN KEY (quiz_id) REFERENCES quiz (id),
           FOREIGN KEY (question_id) REFERENCES question (id))''')
    close()

# ------------------------------
# Додаємо питання
# ------------------------------
def add_questions():
    questions = [
        ('Скільки місяців на рік мають 28 днів?', 'Всі', 'Один', 'Жодного', 'Два'),
        ('Яким стане зелена скеля, якщо впаде в Червоне море?', 'Мокрим', 'Червоним', 'Не зміниться', 'Фіолетовим'),
        ('Якою рукою краще розмішувати чай?', 'Ложкою', 'Правою', 'Лівою', 'Любою'),
        ('Що не має довжини, глибини, ширини, висоти, а можна виміряти?', 'Час', 'Дурність', 'Море', 'Повітря'),
        ('Коли сіткою можна витягнути воду?', 'Коли вода замерзла', 'Коли немає риби', 'Коли спливла золота рибка', 'Коли сітка порвалася'),
        ('Що більше слона і нічого не важить?', 'Тінь слона', 'Повітряна куля', 'Парашут', 'Хмара')
    ]
    open()
    cursor.executemany('INSERT INTO question (question, answer, wrong1, wrong2, wrong3) VALUES (?,?,?,?,?)', questions)
    conn.commit()
    close()

# ------------------------------
# Додаємо вікторини
# ------------------------------
def add_quiz():
    quizes = [
        ('Своя гра', ),
        ('Хто хоче стати мільйонером?', ),
        ('Найрозумніший', )
    ]
    open()
    cursor.executemany('INSERT INTO quiz (name) VALUES (?)', quizes)
    conn.commit()
    close()

# ------------------------------
# Автоматично зв’язуємо питання з вікторинами
# ------------------------------
def add_links_auto():
    open()
    for quiz_id in range(1, 4):
        for question_id in range(1, 7):
            cursor.execute("INSERT INTO quiz_content (quiz_id, question_id) VALUES (?, ?)", (quiz_id, question_id))
    conn.commit()
    close()

# ------------------------------
# Отримати наступне питання після заданого id
# ------------------------------
def get_question_after(last_id=0, quiz_id=1):
    open()
    query = '''
    SELECT quiz_content.id, question.question, question.answer, question.wrong1, question.wrong2, question.wrong3
    FROM question, quiz_content
    WHERE quiz_content.question_id = question.id
      AND quiz_content.id > ? 
      AND quiz_content.quiz_id = ?
    ORDER BY quiz_content.id
    LIMIT 1
    '''
    cursor.execute(query, [last_id, quiz_id])
    result = cursor.fetchone()
    close()
    return result

# ------------------------------
# Ініціалізація бази
# ------------------------------
def init_db():
    create()
    add_questions()
    add_quiz()
    add_links_auto()
