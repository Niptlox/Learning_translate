import sys

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QCalendar, QDate, QTime
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QApplication,
                             QLineEdit, QLabel, QBoxLayout, QGridLayout,
                             QLCDNumber, QRadioButton, QListWidget, QTimeEdit, QCalendarWidget)
from random import randint
import sys
from PyQt5.QtWidgets import (QWidget, QGridLayout,
                             QPushButton, QApplication,
                             QButtonGroup)


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        main_box = QHBoxLayout()
        self.setLayout(main_box)

        editLayout = QVBoxLayout()
        self.boxL = editLayout
        main_box.addLayout(editLayout)
        timeEdit = QTimeEdit()
        editLayout.addWidget(timeEdit)
        calendar = QCalendarWidget()
        editLayout.addWidget(calendar, stretch=1)
        editPlan = QLineEdit()
        editLayout.addWidget(editPlan)
        writePlan = QPushButton("Добавить событие")
        editLayout.addWidget(writePlan)
        writePlan.clicked.connect(
            lambda _,: self.newPlan(timeEdit.time(), calendar.selectedDate(), editPlan.text()))

        self.planList = QListWidget()
        main_box.addWidget(self.planList, stretch=1)

        self.setWindowTitle('Минипланировщик')
        self.show()

    def newPlan(self, time, date, text):
        stDateTime = date.toString("yyyy-MM-dd") + " " + time.toString("hh:mm:ss")
        stPlan = stDateTime + " - " + text
        self.planList.addItem(stPlan)
        # self.setLayout(self.boxL)
        # self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
