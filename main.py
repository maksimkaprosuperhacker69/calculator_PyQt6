# КАЛЬКУЛЯТОР НА PYTHON

# imports
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMainWindow, QGridLayout

from test import *


class MainWindow(QMainWindow):   # Главное окно
    def __init__(self):
        super().__init__()

        self.init_UI()  # Конструктор

        self.init_window_settings()    # Размеры окна

        self.show()      # Показ окна

    def init_UI(self):
        self.widget = QWidget()  # Main widget
        self.Grid_layout = QGridLayout()  # Сетка

        self.Grid_layout.setContentsMargins(0, 0, 0, 0) # Отступы
        self.Grid_layout.setSpacing(0)                  # Отступы
        self.Grid_layout.setVerticalSpacing(0)          # Отступы

        self.label = QLabel('0')     # Значение по умолчанию "0"
        self.label.setFont(QFont('Arial', 60))
        self.label.setMaximumWidth(235)
        self.Grid_layout.addWidget(                                            # Табло с цифрами
            self.label, 0, 0, 1, 4, alignment = Qt.AlignmentFlag.AlignRight)   # Табло с цифрами

        self.list_act = []

        # Список кнопок
        func_list = [
            self.AC, self.reverse, self.percent, self.act_func,
            self.number, self.number, self.number, self.act_func, self.number, self.number,
            self.number, self.act_func, self.number, self.number, self.number, self.act_func, self.number, self.decimal,
            self.equal
        ]
        e = 0 # хз че это
        button_number = -1 # Счетчик кнопок


# Создание кнопок со стилями
        for row, row_labels in enumerate(button_labels):
            for column, label in enumerate(row_labels):
                button_number = button_number + 1
                button = QPushButton(label)
                button.setContentsMargins(0, 0, 0, 0)
                button.setStyleSheet(style)
                if label in num_func_list:
                    if label == 'X':
                        button.clicked.connect(lambda _, button_number=button_number, label=label: func_list[button_number]('*'))
                    else:
                        button.clicked.connect(lambda _, button_number=button_number, label=label: func_list[button_number](label))
                else:
                    button.clicked.connect(func_list[button_number])
                    if label in org_list:
                        button.setStyleSheet(f"{style.replace('background-color:grey;', 'background-color:orange;')}")
                button.setFixedSize(60, 50)
                if label in ['0', ',']:
                    button.setStyleSheet(style)
                if label == '=':
                    button.setStyleSheet(f"{style.replace('background-color:grey;', 'background-color:orange;')}")
                if label == '0':
                    self.Grid_layout.addWidget(button, row + 1, column, 1, 2)
                    button.setFixedSize(120, 50)
                    e = 1
                else:
                    self.Grid_layout.addWidget(button, row + 1, column + e)

        self.widget.setLayout(self.Grid_layout) # Установка главной сетки
        self.setCentralWidget(self.widget)  # Установка главного виджета


    # Изменение размера текста для корректного отображения
    def size_num(self):
        if len(self.label.text()) == 8:
            self.label.setFont(QFont('Arial', 52))
        if len(self.label.text()) == 9:
            self.label.setFont(QFont('Arial', 47))
        if len(self.label.text()) == 10:
            self.label.setFont(QFont('Arial', 40))
        if len(self.label.text()) == 11:
            self.label.setFont(QFont('Arial', 34))
        if len(self.label.text()) < 8:
            self.label.setFont(QFont('Arial', 60))
        if len(self.label.text()) > 11:
            text = self.label.text()
            num_str = text
            mantissa_length = len(num_str) - 1
            # Конвертирование числа в формат мантиссы и экспоненты
            mantissa = num_str[0] + "." + num_str[1:num_str.find('.')]
            exponent = str(mantissa_length)
            self.label.setText(str(round(float(mantissa), 8)) + "e" + exponent)
            self.size_num()

    #Функция для создания списка с операций
    def action(self, num, act):
        if self.list_act == []:
            self.list_act.append(num)
            self.list_act.append(act)
            self.size_num()


    # Функция очистки
    def AC(self):
        self.label.setText('0')
        self.list_act = []
        self.size_num()

    # Функция для работы кнопок чисел
    def number(self, label):
        if self.label.text() != '0':
            self.label.setText(self.label.text() + label)
        else:
            self.label.setText(label)
        self.size_num()


    # Функция для добавления дробной части
    def decimal(self):
        if '.' not in self.label.text():
            self.label.setText(str(self.label.text() + '.'))
        self.size_num()

    # Функция для обратного числа
    def reverse(self):
        self.label.setText(str(float(self.label.text()) * -1))
        self.size_num()


    # Функция для перевода в проценты
    def percent(self):
        self.label.setText(str(float(self.label.text()) / 100))
        self.size_num()


    # Функция для операций
    def act_func(self, func):
        try:
            self.action(float(self.label.text()), f'{func}')
        except:
            text = self.label.text()
            num = int(text[0:text.find('e')]) * (10 ** int(text[text.find('e') + 1:]))
            self.action(float(num, f'{func}'))
        self.label.setText('0')
        self.size_num()



    # Функция для кнопки 'равно'
    def equal(self):
        if self.list_act and self.list_act[0]!=0:
            try:
                self.label.setText(
                    str(eval(f"{self.list_act[0]}{self.list_act[1]}{self.label.text()}")))
            except ZeroDivisionError:
                self.label.setText('error')
            self.list_act = []
        else:
            self.list_act=[]
        self.size_num()


    # Функция для установки размера окна
    def init_window_settings(self):
        self.setFixedSize(240, 330)

# Функция main( Точка входа )
def main():
    app = QApplication([])
    main_win = MainWindow()
    app.exec()


main()
