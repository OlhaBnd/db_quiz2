from random import shuffle
from flask import Flask, session, redirect, url_for, render_template_string, request
from db_scripts import get_question_after, init_db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ThisIsSecretSecretSecretLife'

# Ініціалізуємо базу
init_db()

# --------------------------
# CSS-шаблон для кнопок і сторінки
# --------------------------
STYLE = """
<style>
body {
    font-family: Arial, sans-serif;
    background-color: #f0f4f8;
    text-align: center;
    padding: 50px;
}
h2 {
    color: #333;
}
button {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 15px 30px;
    margin: 10px;
    font-size: 16px;
    cursor: pointer;
    border-radius: 8px;
    transition: 0.3s;
}
button:hover {
    background-color: #45a049;
}
a.finish {
    display: inline-block;
    margin-top: 20px;
    padding: 10px 25px;
    background-color: #f44336;
    color: white;
    text-decoration: none;
    border-radius: 8px;
    transition: 0.3s;
}
a.finish:hover {
    background-color: #d32f2f;
}
.feedback {
    font-size: 20px;
    margin: 20px 0;
}
</style>
"""

# --------------------------
# Головна сторінка
# --------------------------
@app.route('/')
def index():
    session['quiz'] = 1  # або randint(1,3) для випадкової вікторини
    session['last_question'] = 0
    session['score'] = 0
    return f'{STYLE}<a href="/test"><button>Почати тест</button></a>'

# --------------------------
# Сторінка тесту
# --------------------------
@app.route('/test')
def test():
    result = get_question_after(session['last_question'], session['quiz'])

    if result is None:
        return redirect(url_for('result'))

    session['last_question'] = result[0]

    question_text = result[1]
    correct = result[2]
    wrongs = [result[3], result[4], result[5]]

    answers = wrongs + [correct]
    shuffle(answers)

    session['correct_answer'] = correct

    # HTML із стилізацією та кнопкою "Завершити тест"
    html = f'''
    {STYLE}
    <h2>{question_text}</h2>
    <form method="get" action="/answer">
        {"".join(f'<button type="submit" name="answer" value="{a}">{a}</button><br><br>' for a in answers)}
    </form>
    <a href="/result" class="finish">Завершити тест</a>
    '''
    return render_template_string(html)

# --------------------------
# Обробка відповіді
# --------------------------
@app.route('/answer')
def answer():
    user_ans = request.args.get('answer')
    correct = session.get('correct_answer')

    if user_ans == correct:
        session['score'] += 1
        feedback = f'<div class="feedback" style="color:green;">Правильно! ✅</div>'
    else:
        feedback = f'<div class="feedback" style="color:red;">Неправильно! ❌ Правильна: {correct}</div>'

    feedback += '<a href="/test"><button>Наступне питання</button></a>'
    feedback += '<br><a href="/result" class="finish">Завершити тест</a>'
    return render_template_string(STYLE + feedback)

# --------------------------
# Кінець тесту
# --------------------------
@app.route('/result')
def result():
    score = session.get('score', 0)
    html = f'''
    {STYLE}
    <h2>Тест завершено!</h2>
    <p>Ваш результат: {score} балів</p>
    <a href="/"><button>Повернутися на головну</button></a>
    '''
    return render_template_string(html)

# --------------------------
# Запуск сервера
# --------------------------
if __name__ == '__main__':
    app.run(debug=True)