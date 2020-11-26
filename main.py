import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from PyQt5.QtWidgets import QLCDNumber, QLabel

from random import randint
import os


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Зопоминайка слов")
        self.setCentralWidget(Translater())
        self.setGeometry(300, 300, 300, 300)


class Translater(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        cotalog = "\moduls"
        expansion = ".txt"

    def get_moduls(cotalog="moduls/", expansion=".txt", clear_expansion=True):
        # Каталог из которого будем брать файлы
        directory = cotalog

        # Получаем список файлов в переменную files
        files = os.listdir(directory)
        files = filter(lambda x: x.endswith(expansion), files)
        if clear_expansion:
            moduls = [name[:-len(expansion)] for name in files]
        else:
            moduls = list(files)
        return moduls

    def get_dict(modul, cotalog="moduls/", expansion=".txt"):
        namef = cotalog + modul + expansion
        try:
            f = open(namef)
        except:
            return False
        text = f.read().replace(" ", "").split("\n")
        words = {}
        i_st = 0
        while i_st < len(text):
            st = text[i_st]
            if st == "":
                i_st += 1
                words[text[i_st]] = text[i_st + 1]
                i_st += 2
        return words

    def new_dictation(words, count_words=None, modul=None):
        if count_words is None:
            count_words = len(words)
        misspelled words

    def initUI(self):
        self.setGeometry(300, 300, 300, 300)

        self.btn = QPushButton('Кнопка', self)
        # Подстроим размер кнопки под надпись на ней
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(100, 150)
        # Обратите внимание: функцию не надо вызывать :)
        self.btn.clicked.connect(self.inc_click)

        self.label = QLabel(self)
        # Текст задается также, как и для кнопки
        self.label.setText("Количество нажатий на кнопку")
        self.label.move(80, 30)

        self.LCD_count = QLCDNumber(self)
        self.LCD_count.move(110, 80)

        self.count = 0

    def inc_click(self):
        self.count += 1
        # В QLCDNumber для отображения данных используется метод display()
        self.LCD_count.display(self.count)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    # Translater().show()
    sys.exit(app.exec())
