import DateBase as db
import sys
import core
import wordsExplorer as WE

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, \
    QStackedLayout, QHBoxLayout, \
    QVBoxLayout, QTableWidget, \
    QTableWidgetItem, QListWidget, \
    QPlainTextEdit, QLineEdit, QFileDialog, QMessageBox

from PyQt5.QtWidgets import QLCDNumber, QLabel


BASESIZETABLE = (400, 300)


class MainWindow(QWidget):
    def __init__(self, base):
        super().__init__()
        self.base = base
        self.initUI()

    def initUI(self):
        # self.setStyleSheet(ROUNDED_STYLE_SHEET1)
        self.main_box = QVBoxLayout()
        self.setLayout(self.main_box)
        self._size = (500, 500)
        # self.setGeometry(500, 500, *self._size)
        self.setWindowTitle("Leanitr")
        self.stackedLayout = QStackedLayout()
        self.main_box.addLayout(self.stackedLayout)
        self.explorerGroupsDialog = WE.ExplorerWords(self.base)
        self.addGroupDialog = WE.AddGroupWidget(self.base)
        self.mainWidget = MainWidget(self.base, funcAddGroup=self.addGroup, funcExplor=self.explorerGroups,
                                     funcStart=self.startLearn)
        self.groupsWidget = TableGroupsWidget(self.base,
                                              funcGroup=print,
                                              funcBack=self.visibleMain)

        # self.stackedLayout.addWidget(tw)
        self.stackedLayout.addWidget(self.mainWidget)
        self.stackedLayout.setCurrentIndex(0)
        self.stackedLayout.addWidget(self.groupsWidget)

    def startLearn(self):
        self.stackedLayout.setCurrentIndex(1)
        self.groupsWidget.updateTable()

    def addGroup(self):
        self.addGroupDialog.show()

    def explorerGroups(self):
        print("explorerGroups")
        self.explorerGroupsDialog.show()

    def visibleMain(self):
        self.stackedLayout.setCurrentIndex(0)


class MainWidget(QWidget):
    def __init__(self, base, funcExplor=None, funcAddGroup=None, funcStart=None):
        super().__init__()
        self.base = base
        self.funcStart = funcStart
        self.funcExplor = funcExplor
        self.funcAddGroup = funcAddGroup
        self.initUI()

    def initUI(self):
        main_box = QVBoxLayout()
        self.setLayout(main_box)
        main_box.addStretch(1)
        main_box.addWidget(QLabel("    ПРИВЕТ"))
        main_box.addStretch(1)
        butStart = QPushButton("Начать тест")
        butStart.clicked.connect(self.funcStart)
        butStart.setMaximumWidth(350)
        butStart.setMinimumHeight(35)
        main_box.addWidget(butStart)

        butExplor = QPushButton("Обозреватель групп")
        butExplor.clicked.connect(self.funcExplor)
        butExplor.setMaximumWidth(350)
        butExplor.setMinimumHeight(35)
        main_box.addWidget(butExplor)

        butAdd = QPushButton("Добавить группу")
        butAdd.clicked.connect(self.funcAddGroup)
        butAdd.setMaximumWidth(350)
        butAdd.setMinimumHeight(35)
        main_box.addWidget(butAdd)
        main_box.addStretch(3)


class TableGroupsWidget(QWidget):
    def __init__(self, base, funcGroup=None, funcBack=None):
        super().__init__()
        self.base = base
        self.funcVisibleGroup = funcGroup
        self.funcBack = funcBack
        self.initUI()

    def initUI(self):
        main_box = QVBoxLayout()
        # (self, base, size=(500, 300), maxHeight = None, wordID = True, groupID = None,
        #                                                                          typeView = TVIEWGROUP, cellClicked = None, cellDoubleClicked = None)
        self.table = WE.TableMy(self.base, BASESIZETABLE, typeView=WE.TVIEWGROUPS, cellClicked=self.activCell,
                                cellDoubleClicked=self.funcVisibleGroup)

        main_box.addWidget(self.table)
        self.butLayout = butLayout = QHBoxLayout()
        # butLayout.addStretch()
        main_box.addLayout(butLayout)

        self.butBack = butBack = QPushButton("В меню")
        butBack.clicked.connect(self.funcBack)
        butBack.setMinimumWidth(130)
        butLayout.addWidget(butBack)

        butLayout.addStretch()

        self.butVisible = butVisible = QPushButton("Выбрать")
        butVisible.clicked.connect(lambda: self.funcVisibleGroup(self.rowA))
        butVisible.setMinimumWidth(100)
        butLayout.addWidget(butVisible)

        self.updateTable()
        self.setLayout(main_box)
        self.enabledTable(False)

    def updateTable(self):
        self.enabledTable(False)
        self.table.updateTable()
        return self.table

    def enabledTable(self, p1):
        self.butVisible.setEnabled(p1)

    def activCell(self, row):
        print("activCell:", row)
        self.rowA = row
        self.enabledTable(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    base = db.DateBase("Learning_translate.sqlite")
    window = MainWindow(base)
    window.show()
    sys.exit(app.exec())
