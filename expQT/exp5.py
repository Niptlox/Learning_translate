#!/usr/bin/python3
# -*- coding:utf-8 -*-

import sys
import UI_MainForm as Ui_MainForm
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *


class MainForm(QMainWindow, Ui_MainForm.Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('C:\\George\\Programming\\Python\\Projects\\PyQT\\Learning_translate\\testbase.db')
        self.db.open()

        self.model = QSqlTableModel()
        self.model.setTable('main_table')
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.select()

        self.model.setHeaderData(0, Qt.Horizontal, 'Ф.И.О.')
        self.model.setHeaderData(1, Qt.Horizontal, 'Примечания')
        self.tableView.setModel(self.model)

        self.pushButton_quit.clicked.connect(qApp.quit)
        self.pushButton_search_fullname.clicked.connect(self.search_fullname)

    def search_fullname(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainForm()
    win.show()
    sys.exit(app.exec_())