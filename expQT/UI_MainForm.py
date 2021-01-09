# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainForm.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(515, 361)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_fullname = QtWidgets.QLabel(self.widget)
        self.label_fullname.setObjectName("label_fullname")
        self.horizontalLayout.addWidget(self.label_fullname)
        self.lineEdit_fullname = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_fullname.setObjectName("lineEdit_fullname")
        self.horizontalLayout.addWidget(self.lineEdit_fullname)
        self.pushButton_search_fullname = QtWidgets.QPushButton(self.widget)
        self.pushButton_search_fullname.setObjectName("pushButton_search_fullname")
        self.horizontalLayout.addWidget(self.pushButton_search_fullname)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.tableView = QtWidgets.QTableView(self.widget)
        self.tableView.setObjectName("tableView")
        self.gridLayout_2.addWidget(self.tableView, 1, 0, 1, 1)
        self.pushButton_quit = QtWidgets.QPushButton(self.widget)
        self.pushButton_quit.setObjectName("pushButton_quit")
        self.gridLayout_2.addWidget(self.pushButton_quit, 2, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.lineEdit_fullname, self.pushButton_search_fullname)
        MainWindow.setTabOrder(self.pushButton_search_fullname, self.tableView)
        MainWindow.setTabOrder(self.tableView, self.pushButton_quit)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Test QTableView search"))
        self.label_fullname.setText(_translate("MainWindow", "Ф.И.О."))
        self.pushButton_search_fullname.setText(_translate("MainWindow", "Поиск"))
        self.pushButton_quit.setText(_translate("MainWindow", "Выход"))