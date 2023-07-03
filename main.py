from random import shuffle, randint
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


###############################################################################
###############################################################################
# Здесь задаётся логика программы, её "мозг".

class Question:
    def __init__(self, question, right_answer, wrong1, wrong2, wrong3):
        self.question = question
        self.right_answer = right_answer
        self.wrong1 = wrong1  # Способ хранения вопросов и ответов.
        self.wrong2 = wrong2
        self.wrong3 = wrong3


def create_task():
    task_list = []
    question_list = []
    for i in range(20):
        num1 = randint(1, 100)
        num2 = randint(1, 100)
        operation = randint(1, 4)
        str_operation = ''
        if operation == 1:
            task = num1 + num2
            str_operation = '+'
        elif operation == 2:  # Функция создаёт задачи
            task = num1 - num2
            str_operation = '-'
        elif operation == 3:
            task = num1 * num2
            str_operation = '*'
        else:
            str_operation = ':'
            if num1 < num2:
                num1, num2 = num2, num1
            task = round(num1 / num2, 2)
        question = str(num1) + str_operation + str(num2)
        question_list.append(question)
        task_list.append(task)
    return task_list, question_list


def ask(q: Question):  # Функция расставляет вопрос и варианты ответов.
    shuffle(radio_buttons)
    radio_buttons[0].setText(q.right_answer)
    radio_buttons[1].setText(q.wrong1)
    radio_buttons[2].setText(q.wrong2)
    radio_buttons[3].setText(q.wrong3)
    ans_text1.setText(q.right_answer)
    answer.setText(q.question)


def flag_off():  # Сброс вариантов ответа.
    RadioBGroup.setExclusive(False)
    rad_but_1.setChecked(False)
    rad_but_2.setChecked(False)
    rad_but_3.setChecked(False)
    rad_but_4.setChecked(False)
    RadioBGroup.setExclusive(True)


def smena_answer():
    RadioButtonGroup.hide()
    Ans_Group.show()
    ans_button.setText('Следущий вопрос')
    flag_off()
    main_win.total += 1  # Функция меняет окно, показывает окно ответа.


def smena_qest():
    Ans_Group.hide()
    RadioButtonGroup.show()
    ans_button.setText('Ответить')
    next_qest()  # Функция меняет окно, показывает вопрос и варианты ответа.


def pereckluchenie():
    global start_flag
    if ans_button.text() != 'Ответить':
        smena_qest()
    elif start_flag:
        start_flag = False
        smena_qest()
    else:  # Функция, переключающая виды окна до/после ответа.
        smena_answer()


def check_answer():  # Функция проверяет вопрос на правильность,
    if radio_buttons[0].isChecked():  # в зависимости от ответа
        ans_text2.setText('Правильно')  # меняет окраску окна и текст.
        main_win.score += 1
        Ans_Group.setStyleSheet("background-color: lightgreen")
    else:
        ans_text2.setText('Неправильно, правилно было:')
        Ans_Group.setStyleSheet("background-color: red")
    pereckluchenie()


def next_qest():  # Функция, случайным образом выбирающая вопрос.
    if len(questions) != len(asked_questions):
        cur_questions = randint(0, len(questions) - 1)
        while True:
            if questions[cur_questions] in asked_questions:
                cur_questions = randint(0, len(questions) - 1)
            else:
                break
        asked_questions.append(questions[cur_questions])
        ask(questions[cur_questions])
    else:
        konec()


def konec():
    answer.hide()
    RadioButtonGroup.hide()  # Функция выводит конечную статистику
    Ans_Group.hide()  # после ответа на все вопросы.
    ans_button.hide()
    score_text2.setText('Вопросов всего: ' + str(main_win.total))
    score_text3.setText('Отвечуно правильно: ' + str(main_win.score))
    score_text4.setText('Рейтинг: ' + str((main_win.score / main_win.total) * 100))
    score_text1.show()
    score_text2.show()
    score_text3.show()
    score_text4.show()

###############################################################################
###############################################################################


asked_questions = list()
task_list, questions_text = create_task()  # Создание заданий
questions = []
start_flag = True

for i in range(len(task_list)):
    q = Question(
        questions_text[i],
        str(task_list[i]),
        str(task_list[i] + 1),  # Здесь формируется список вопросов
        str(task_list[i] - 1),  # и варианты ответов к ним.
        str(task_list[i] * 2))
    questions.append(q)

###############################################################################
###############################################################################
# Здесь начинается создание окна программы.

app = QApplication([])
main_win = QWidget()  # Здесь создаётся окно само по себе.
main_win.setWindowTitle('Вопросник')

main_win.total = 0
main_win.score = 0

main_win.resize(400, 400)
answer = QLabel('Готовся решить тест по математике!')  # Задаётся размер окна и его шрифт.
answer.setFont(QFont('Arial', 12))

RadioButtonGroup = QGroupBox('Варианты ответов:')
RadioButtonGroup.setFont(QFont('Arial', 10))

Ans_Group = QGroupBox('Ответ')
Ans_Group.setFont(QFont('Arial', 10))  # Задаётся нижняя часть окна,
Ans_Group.hide()  # показывающая ответ.
ans_button = QPushButton('Ответить')
ans_text1 = QLabel('******')
ans_text2 = QLabel('Правильно/Неправильно')
ans_text1.setFont(QFont('Arial', 10))
ans_text2.setFont(QFont('Arial', 10))

score_text1 = QLabel('Ваш результат за тест:')
score_text2 = QLabel('')
score_text3 = QLabel('')
score_text4 = QLabel('')
score_text1.setFont(QFont('Arial', 11))
score_text2.setFont(QFont('Arial', 11))  # Здесь задаётся конечный
score_text3.setFont(QFont('Arial', 11))  # вид окна после конца теста.
score_text4.setFont(QFont('Arial', 11))
score_text1.hide()
score_text2.hide()
score_text3.hide()
score_text4.hide()

main_layout = QVBoxLayout()
up_layout = QHBoxLayout()
down_layout = QHBoxLayout()  # десь задаются "невидимые линии", на которых будут
ans_layout1 = QVBoxLayout()  # формироватся все элементы окна
ans_layout2 = QHBoxLayout()

RadioBGroup = QButtonGroup()
rad_but_1 = QRadioButton('просто')
rad_but_2 = QRadioButton('на')  # Создаётся нижняя часть окна с вариантами ответа.
rad_but_3 = QRadioButton('нажми')
rad_but_4 = QRadioButton('кнопку')
radio_buttons = [rad_but_1, rad_but_2, rad_but_3, rad_but_4]
RadioBGroup.addButton(rad_but_1)
RadioBGroup.addButton(rad_but_2)
RadioBGroup.addButton(rad_but_3)
RadioBGroup.addButton(rad_but_4)

layout_group1 = QVBoxLayout()
layout_group2 = QHBoxLayout()  # Здесь создаются "невидимыке линии"
layout_group3 = QHBoxLayout()  # для размещения вариантов ответа.
layout_group2.addWidget(rad_but_1, alignment=Qt.AlignLeft)
layout_group2.addWidget(rad_but_3, alignment=Qt.AlignRight)
layout_group3.addWidget(rad_but_2, alignment=Qt.AlignLeft)
layout_group3.addWidget(rad_but_4, alignment=Qt.AlignRight)
################################
layout_group1.addLayout(layout_group2)
layout_group1.addLayout(layout_group3)
ans_layout2.addWidget(ans_text2, alignment=Qt.AlignLeft)
ans_layout1.addLayout(ans_layout2)
ans_layout1.addWidget(ans_text1, alignment=Qt.AlignCenter)

RadioButtonGroup.setLayout(layout_group1)
Ans_Group.setLayout(ans_layout1)
# Здесь окно "собирается" воедино.
up_layout.addWidget(answer, alignment=Qt.AlignCenter)
down_layout.addWidget(ans_button, stretch=3)

main_layout.addLayout(up_layout)
main_layout.addWidget(RadioButtonGroup)
main_layout.addWidget(score_text1, alignment=Qt.AlignCenter)
main_layout.addWidget(score_text2, alignment=Qt.AlignCenter)
main_layout.addWidget(score_text3, alignment=Qt.AlignCenter)
main_layout.addWidget(score_text4, alignment=Qt.AlignCenter)
main_layout.addWidget(Ans_Group)
main_layout.addLayout(down_layout)
main_layout.setSpacing(5)

main_win.setLayout(main_layout)

ans_button.clicked.connect(check_answer)

main_win.show()  # Показ окна на экране.
app.exec()  # Данная строка не позволяет окну закрываться.
