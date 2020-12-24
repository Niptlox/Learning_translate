import sys
from PyQt5 import QtCore
import PyQt5.QtWidgets as QtGui

ROUNDED_STYLE_SHEET1 = """QPushButton {
     background-color: green;
     color: white;
     border-style: outset;
     border-width: 4px;
     border-radius: 15px;
     border-color: blue;
     font: bold 10px;
     min-width: 10em;
     padding: 8px;
 }
"""

class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()


    def initUI(self):
        self.title = QtGui.QLabel("business management")
        self.title.setStyleSheet("font: bold 30ft AGENTORANGE")
        self.table = QtGui.QTableWidget()

        self.table.setColumnCount(6)


        self.table.setHorizontalHeaderLabels(QtCore.QString("#;Item description;Qty;Rate(Rs:);Subtotal;Delete").split(";"))
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
        self.table.verticalHeader()

        self.table.setColumnWidth(1,150)
        self.table.setColumnWidth(6,10)
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table.setRowCount(2)

        self.table.setMinimumHeight(20)
        self.hbox = QtGui.QHBoxLayout()
        self.hbox.addWidget(self.table)


        self.btn1 = QtGui.QPushButton(self)
        self.btn1.resize(200,100)
        self.btn1.setStyleSheet(ROUNDED_STYLE_SHEET1)
        self.btn1.setText("connect")
        self.lineedit = QtGui.QLineEdit()


        self.btn2 = QtGui.QPushButton("back",self)

        self.btn3 = QtGui.QPushButton("resetform", self)
        self.btn4 = QtGui.QPushButton("play",self)
        self.grid = QtGui.QGridLayout()
        self.grid.addWidget(QtGui.QLabel("Invoice Serial Number -39 "), 0,0)
        self.grid.addWidget(QtGui.QLineEdit(), 0,1)
        self.grid.addWidget(self.btn1,0,2)
        self.grid.addWidget(self.table,1,0,1,2)
        self.grid.addWidget(self.btn2,2,0)
        self.grid.addWidget(self.btn3,2,1)
        self.grid.addWidget(self.btn4,2,4)

        self.setLayout(self.grid)

        self.setWindowTitle("business management")
        self.setGeometry(200,300,900,600)
        self.show()

def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()