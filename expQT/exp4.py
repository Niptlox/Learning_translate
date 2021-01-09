from PyQt5 import QtWidgets


class App(QtWidgets.QWidget):

    def __init__(self):
        super(App, self).__init__()
        self.data = [1, 2, 3, 4, 5]

        self.table = QtWidgets.QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(['V1', 'V2', 'V3', 'V4', 'V5'])
        n = 6
        self.table.setRowCount(n)
        self.IDsWords = [None] * n
        for i_g in range(n):
            p1, p2 = 5 - i_g, i_g % 3
            self.IDsWords[i_g] = p1
            self.tableTranslate.insertRow(i_g)
            labels = (p1, p2)
            for i_c in range(len(labels)):
                item = QTableWidgetItem(labels[i_c])
                self.tableTranslate.setItem(i_g, i_c, item)
                print("label Trans", labels[i_c])


        self.table.setMouseTracking(True)

        # ------------------------------------------------------------
        # Этот сигнал испускается при каждом щелчке ячейки в таблице.
        self.table.cellClicked[int, int].connect(self.clickedRowColumn)

        # Этот сигнал испускается, когда ячейка, указанная в строке и столбце, активирована
        self.table.cellActivated[int, int].connect(self.activatedRowColumn)

        # Этот сигнал излучается всякий раз, когда данные элемента в ячейке изменяются.
        self.table.cellChanged[int, int].connect(self.changedRowColumn)

        # Этот сигнал испускается, когда курсор мыши входит в ячейку. 
        self.table.cellEntered[int, int].connect(self.enteredRowColumn)
        # -------------------------------------------------------------

        self.lbl = QtWidgets.QLabel()
        self.btn_add = QtWidgets.QPushButton('Добавить строку')

        self.btn_add.clicked.connect(self.add_row)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.lbl)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.btn_add)
        self.setLayout(self.layout)

    def activatedRowColumn(self, r, c):
        self.lbl.setText("Активная: строка->`{}`, столбец->`{}`, ячейка->`<b> {} : {}</b> `".format(r, c, r, c, ))

    def changedRowColumn(self, r, c):
        self.lbl.setText("Изменились данные ячейки->`<b> {} : {}<b>`".format(r, c, ))

    def clickedRowColumn(self, r, c):
        self.lbl.setText("<b>Вы кликнули ячейку->`<i style='color:blue'> {} : {} </i>`</b>".format(r, c, ))

    def enteredRowColumn(self, r, c):
        self.lbl.setText("<b>Курсор мыши в ячейкe->`<i style='color:red'> {} : {} </i>`</b>".format(r, c, ))

    def add_row(self):
        rowPosition = self.table.rowCount()
        self.table.insertRow(rowPosition)
        for i in range(5):
            self.table.setItem(rowPosition,
                               i,
                               QtWidgets.QTableWidgetItem(str(self.data[i])))


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    ex = App()
    ex.show()
    app.exec_()

    # def allGroupsUI(self):
    #     headerLabels = ['Группа', 'Количество слов', 'Языки']
    #     main_box = QVBoxLayout()
    #     groupList = QListWidget()
    #     groupList.addItem("\t".join(headerLabels))
    #     groups = self.base.getGroups()
    #     n = len(groups)
    #     for i_g in range(n):
    #         group = groups[i_g]
    #         langs = group['Languages']
    #         labels = (group["Name"], str(group["CountWords"]) + "\t", "; ".join(map(lambda x: x[1], langs)))
    #         st = "\t".join(labels)
    #         groupList.addItem(st)
    #     return groupList
