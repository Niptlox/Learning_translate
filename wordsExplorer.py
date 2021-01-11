import DateBase as db
import os
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, \
    QStackedLayout, QHBoxLayout, \
    QVBoxLayout, QTableWidget, \
    QTableWidgetItem, QListWidget, \
    QPlainTextEdit, QLineEdit, QFileDialog, QMessageBox, QDialog

from PyQt5.QtWidgets import QAbstractItemView, QHeaderView

from PyQt5.QtWidgets import QLCDNumber, QLabel

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
 }"""

# types viewing
TVIEWGROUP = 0
TVIEWGROUPS = 3
TVIEWWORD = 1
TVIEWWORDS = 2

HIDEINDEX = True

BASESIZETABLE = (430, 330)


def createTable(size, headerLabels, widthColumns, lastStretch=True, maximumHeight=None, hideFColumn=False,
                tableWidget=None):
    # size = (400, 300)
    w, h = size
    n = len(headerLabels)
    print("len(headerLabels)", (headerLabels))

    table = QTableWidget(0, n) if tableWidget is None else tableWidget
    table.setColumnCount(n)
    table.setHorizontalHeaderLabels(headerLabels)
    if hideFColumn:
        table.hideColumn(0)
    if maximumHeight:
        table.setMaximumHeight(maximumHeight)
    # table.setMaximumSize(*size)
    # table.setFixedSize(*size)

    table.setMinimumSize(*size)

    for i in range(n):
        w_c = widthColumns[i]
        if w_c is not None:
            table.setColumnWidth(i, w_c if w_c > 1 else w_c * w)
    print(3)
    table.setSelectionBehavior(QAbstractItemView.SelectRows)
    table.setSelectionMode(QAbstractItemView.SingleSelection)
    table.setEditTriggers(QAbstractItemView.NoEditTriggers)
    table.horizontalHeader().setStretchLastSection(lastStretch)
    table.verticalHeader().hide()
    # table.horizontalHeader().setSectionResizeMode(n - 1, QHeaderView.ResizeToContents)
    # table.verticalHeader()
    return table


class ExplorerWords(QDialog):
    def __init__(self, base):
        super().__init__()
        self.base = base
        self.initUI()

    def initUI(self):
        self.setModal(True)
        # self.setStyleSheet(ROUNDED_STYLE_SHEET1)
        self.main_box = QVBoxLayout()
        self.setLayout(self.main_box)
        self._size = (500, 500)
        # self.setGeometry(500, 500, *self._size)
        self.setWindowTitle("Обозреватель групп")
        self.stackedLayout = QStackedLayout()
        self.main_box.addLayout(self.stackedLayout)

        self.groupsWidget = TableGroupsWidget(self.base,
                                              funcVisibleGroup=self.visibleGroup,
                                              funcAddGroup=self.visibleAddGroup)
        self.wordsWidget = TableWordsWidget(self.base,
                                            funcVisibleWord=self.visibleWord,
                                            funcBack=self.visibleGroups,
                                            funcAddWord=lambda x: print("addWord", x))

        self.wordVWidget = ViewWordWidget(self.base,
                                          funcEditWord=lambda x: print("EditWord " + str(x)),
                                          funcBack=lambda: self.visibleGroup(self.groupID))
        self.addGroupWidget = AddGroupWidget(self.base, funcUpdate=self.groupsWidget.table.updateTable)

        # tw = TableWords(base, groupID=4, typeView=TVIEWGROUP)
        # tw = TableWords(base, wordID=4, typeView=TVIEWWORD)
        # tw = TableMy(base, typeView=TVIEWWORDS)
        # tw = TableMy(self.base, typeView=TVIEWGROUPS)
        # tw.updateTable()

        # self.stackedLayout.addWidget(tw)
        self.stackedLayout.addWidget(self.groupsWidget)
        self.stackedLayout.setCurrentIndex(0)
        self.stackedLayout.addWidget(self.wordsWidget)
        self.stackedLayout.addWidget(self.wordVWidget)
        # self.stackedLayout.addWidget(self.addGroupWidget)


    def visibleAddGroup(self):
        self.addGroupWidget.show()

    def visibleGroup(self, groupID):
        self.groupID = groupID
        print("visibleGroup:", groupID)
        self.wordsWidget.fillTable(groupID)
        self.stackedLayout.setCurrentIndex(1)

    def visibleGroups(self):
        self.groupsWidget.fillTable()
        self.stackedLayout.setCurrentIndex(0)

    def visibleWord(self, wordID):
        print("VWord", wordID)
        # self.wordVWidget.funcBack =
        self.wordVWidget.setWord(wordID)
        self.stackedLayout.setCurrentIndex(2)


class TableGroupsWidget(QWidget):
    def __init__(self, base, funcVisibleGroup=None, funcAddGroup=None):
        super().__init__()
        self.base = base
        self.funcVisibleGroup = funcVisibleGroup
        self.funcAddGroup = funcAddGroup
        self.initUI()

    def initUI(self):
        main_box = QVBoxLayout()
        # (self, base, size=(500, 300), maxHeight = None, wordID = True, groupID = None,
        #                                                                          typeView = TVIEWGROUP, cellClicked = None, cellDoubleClicked = None)
        self.table = TableMy(self.base, BASESIZETABLE, typeView=TVIEWGROUPS, cellClicked=self.activCell,
                             cellDoubleClicked=self.funcVisibleGroup)

        main_box.addWidget(self.table)
        self.butLayout = butLayout = QHBoxLayout()
        # butLayout.addStretch()
        main_box.addLayout(butLayout)

        self.butAdd = butAdd = QPushButton("Добавить группу")
        butAdd.clicked.connect(self.funcAddGroup)
        butAdd.setMinimumWidth(110)
        butLayout.addWidget(butAdd)
        butLayout.addStretch()

        self.butDel = butDel = QPushButton("Удалить группу")
        butDel.clicked.connect(self.delGroup)
        butDel.setMinimumWidth(110)
        butLayout.addWidget(butDel)

        self.butVisible = butVisible = QPushButton("Просмотр")
        butVisible.clicked.connect(lambda: self.funcVisibleGroup(self.rowA))
        butVisible.setMinimumWidth(100)
        butLayout.addWidget(butVisible)

        self.fillTable()
        self.setLayout(main_box)
        self.enabledTable(False)

    def createTable(self):
        size = (400, 300)
        w, h = size
        self.headerLabels = ['Группа', 'Количество пар', 'Языки']
        table = createTable(size, self.headerLabels, [w * 0.25, w * 0.37, None], lastStretch=True)
        return table

    def fillTable(self):
        self.enabledTable(False)
        self.table.updateTable()
        return self.table

    def enabledTable(self, p1):
        self.butVisible.setEnabled(p1)
        self.butDel.setEnabled(p1)

    def activCell(self, row):
        print("activCell:", row)
        self.rowA = row
        self.enabledTable(True)

    def delGroup(self):
        buttonReply = QMessageBox.question(self, 'Удаление', "Удалить группу?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            print("delGroup:", self.rowA)
            self.base.delGroup(self.rowA)
            self.fillTable()
        else:
            print('No clicked.')



class TableWordsWidget(QWidget):
    def __init__(self, base, funcVisibleWord=None, funcBack=None, funcAddWord=None):
        super().__init__()
        self.base = base
        # funcVisibleWord = print
        self.funcVisibleWord = funcVisibleWord
        self.funcBack = funcBack
        self.funcAddWord = lambda: funcAddWord(self.groupID)
        # self.groupID = groupID
        self.initUI()

    def initUI(self):
        main_box = QVBoxLayout()
        self.setLayout(main_box)


        title_box = QHBoxLayout()
        main_box.addLayout(title_box)
        label = QLabel(f"Группа ")
        label.setMaximumWidth(40)
        title_box.addWidget(label)
        self.title_label = QLabel(f" ")
        title_box.addWidget(self.title_label)

        # (self, base, size=(500, 300), maxHeight = None, wordID = True, groupID = None,
        #                                                                          typeView = TVIEWGROUP, cellClicked = None, cellDoubleClicked = None)
        self.table = TableMy(self.base, BASESIZETABLE, typeView=TVIEWGROUP, cellClicked=self.activCell,
                             cellDoubleClicked=self.funcVisibleWord)

        main_box.addWidget(self.table)
        self.butLayout = butLayout = QHBoxLayout()
        main_box.addLayout(butLayout)

        self.butBack = butBack = QPushButton("Назад к группам")
        butBack.clicked.connect(self.funcBack)
        butBack.setMinimumWidth(130)
        butLayout.addWidget(butBack)

        butLayout.addStretch()

        # self.butAdd = butAdd = QPushButton("Добавить")
        # butAdd.clicked.connect(self.funcAddWord)
        # butAdd.setMinimumWidth(100)
        # butLayout.addWidget(butAdd)

        self.butVisible = butVisible = QPushButton("Просмотр")
        butVisible.setEnabled(False)
        butVisible.clicked.connect(lambda: self.funcVisibleWord(self.rowA))
        butVisible.setMinimumWidth(100)
        butLayout.addWidget(butVisible)


    def fillTable(self, groupID=None):
        self.groupName = self.base.getNameGroup(groupID)
        print(self.groupName)
        self.title_label.setText(self.groupName)
        self.butVisible.setEnabled(False)
        self.table.groupID = groupID
        self.table.updateTable()
        return self.table

    def activCell(self, row):
        print("activCell:", row)
        self.rowA = row
        self.butVisible.setEnabled(True)


class ViewWordWidget(QWidget):
    def __init__(self, base, funcBack=None, funcEditWord=None):
        super().__init__()
        self.base = base
        self.funcEditWord = funcEditWord
        self.funcBack = funcBack
        # self.groupID = groupID
        self.initUI()

    def initUI(self):
        main_box = QVBoxLayout()
        self.setLayout(main_box)

        main_box.addWidget(QLabel(f"Просмотр слова"))

        self.labelWord = QLabel()
        main_box.addWidget(self.labelWord)
        self.labelLang = QLabel()
        main_box.addWidget(self.labelLang)

        self.textDiscript = QPlainTextEdit()
        self.textDiscript.setMaximumHeight(50)
        main_box.addWidget(self.textDiscript)

        size = (400, 300)
        w, h = size

        # main_box.addWidget(QLabel("Перевод"))
        sizeT = (400, 80)
        # (self, base, size=(500, 300), maxHeight = None, wordID = True, groupID = None,
        #                                                                          typeView = TVIEWGROUP, cellClicked = None, cellDoubleClicked = None)
        self.tableTranslate = TableMy(self.base, sizeT, maxHeight=130, typeView=TVIEWWORD,
                                      cellDoubleClicked=self.setWord)

        main_box.addWidget(self.tableTranslate)
        # self.setWord lambda r, c: print(self.IDsWords[c]) self.table.item(self.table.currentRow(), 0
        # self.IDsWords[self.table.item(self.table.currentRow(), 0).text()]

        main_box.addWidget(QLabel("Группы"))
        sizeT = (400, 80)
        self.tableGroups = createTable(sizeT, [""], [None], maximumHeight=80)
        self.tableGroups.horizontalHeader().hide()
        main_box.addWidget(self.tableGroups)

        # self.table.cellClicked.connect(self.activCell)
        # self.table.cellDoubleClicked.connect(self.funcVisibleWord)
        main_box.addStretch()

        self.butLayout = butLayout = QHBoxLayout()
        main_box.addLayout(butLayout)

        self.butBack = QPushButton("Назад")
        self.butBack.clicked.connect(self.funcBack)
        self.butBack.setMinimumWidth(130)
        butLayout.addWidget(self.butBack)
        self.butLayout.addStretch()


        # self.butEdit = QPushButton("Изменить")
        # self.butEdit.clicked.connect(self.editWord)
        # self.butEdit.setMinimumWidth(130)
        # butLayout.addWidget(self.butEdit)
        main_box.addStretch()

    def setWord(self, idWord):
        self.wordID = idWord
        print(1)
        Word = self.base.getWord(idWord)
        print(Word)
        idWord, word, lang, translateID, descript = Word
        langID, lang = lang
        self.labelWord.setText("Слово:\t" + word)
        self.labelLang.setText("Язык:\t" + lang)

        self.textDiscript.setPlainText(descript if descript != db.NULL else "Описание:")
        self.textDiscript.setEnabled(False)
        self.tableGroups.setRowCount(0)
        # self.tableGroups.setHorizontalHeaderLabels(["Группа", "Zpsrb"])
        groups = self.base.getGroupsWord(idWord)
        for i_g in range(len(groups)):
            groupID, group = groups[i_g]
            self.tableGroups.insertRow(i_g)
            labels = (group,)
            for i_c in range(len(labels)):
                item = QTableWidgetItem(labels[i_c])
                self.tableGroups.setItem(i_g, i_c, item)

        self.tableTranslate.wordID = idWord
        self.tableTranslate.updateTable()

    def editWord(self):
        print("wordID", self.wordID)
        try:
            self.funcEditWord(self.wordID)
        except:
            print(self.wordID)


class TableMy(QTableWidget):
    def __init__(self, base, size=(500, 300), maxHeight=None, wordID=True, groupID=None,
                 typeView=TVIEWGROUP, cellClicked=None, cellDoubleClicked=None):
        super().__init__()
        self.base = base
        self.typeView = typeView
        self._size = size
        headerLabels = ["ID"]
        widthColumns = [0]
        if typeView == TVIEWWORD:
            self.wordID = wordID
            headerLabels += ["Слово", "Язык"]
            widthColumns += [0.5, None]
        elif typeView == TVIEWGROUP:
            self.groupID = groupID
            headerLabels += ["Слово", "Язык", "Перевод"]
            widthColumns += [0.45, 0.23, None]
        elif typeView == TVIEWWORDS:
            headerLabels += ["Слово", "Язык", "Описание"]
            widthColumns += [0.35, 0.23, None]
        elif typeView == TVIEWGROUPS:
            headerLabels += ['Группа', 'Количество пар', 'Языки']
            widthColumns += [0.32, 0.28, None]

        self.headerLabels = headerLabels
        print("size, headerLabels, widthColumns", size, headerLabels, widthColumns)
        createTable(size, headerLabels, widthColumns, lastStretch=True, maximumHeight=maxHeight, hideFColumn=HIDEINDEX,
                    tableWidget=self)
        self.setCellClicked(cellClicked)
        self.setCellDoubleClicked(cellDoubleClicked)
        print(1)

    def setCellClicked(self, func):
        if func:
            self.cellClicked.connect(lambda r, c: func(self.item(r, 0).text()))

    def setCellDoubleClicked(self, func):
        if func:
            self.cellDoubleClicked.connect(lambda r, c: func(self.item(r, 0).text()))

    def updateTable(self):
        self.clear()
        self.setRowCount(0)
        self.setHorizontalHeaderLabels(self.headerLabels)
        if self.typeView == TVIEWGROUP:
            wordsTR = self.base.getWordsOfGroupSTR(self.groupID)
            # [('74', 'plate', 'Английский', 'тарелка'), ...]
            rows = [(str(ws[i][0]), ws[i][1], ws[i][3], ws[-(i + 1)][1]) for grID, ws in wordsTR.items() for i in
                    range(2)]
        if self.typeView == TVIEWGROUPS:
            groups = self.base.getGroups()
            print(groups)
            # [('74', 'plate', 'Английский', 'тарелка'), ...]
            rows = [(str(group["ID"]), group["Name"], str(group["CountWords"]),
                     "; ".join(map(lambda x: x[1], group["Languages"]))) for group in groups]

        elif self.typeView == TVIEWWORD:
            wordsTR = self.base.getTranslatesWord(self.wordID)
            # [('74', 'plate', 'Английский'), ...]
            rows = [(str(w[0]), w[1], w[3]) for w in wordsTR]
        elif self.typeView == TVIEWWORDS:
            wordsTR = self.base.getAllWords()
            # [('74', 'plate', 'Английский', 'описание'), ...]
            rows = [(str(w[0]), w[1], w[3], w[5]) for w in wordsTR]
        print("rows", rows)
        n = len(rows)
        print("n:", n)
        for i in range(n):
            self.insertRow(i)
            aRow = rows[i]
            print(aRow)
            for j in range(len(aRow)):
                item = QTableWidgetItem(aRow[j])
                self.setItem(i, j, item)

        return self


class AddGroupWidget(QDialog):
    def __init__(self, base, funcUpdate=None):
        super().__init__()
        self.base = base
        self.funcUpdate = funcUpdate
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Создание группы')
        self.setModal(True)
        main_box = QVBoxLayout()
        self.setLayout(main_box)

        main_box.addWidget(QLabel(f"Добавление группы слов из файла"))
        helpText = """Пример файла:
[Think]  - Название группы
[Английский; Русский]  - Языки

hello
приветствую

think
думать
"""
        self.textQT = QPlainTextEdit(helpText)
        self.textQT.setReadOnly(False)
        main_box.addWidget(self.textQT)

        main_box.addStretch()
        self.resultLabel = QLabel()
        main_box.addWidget(self.resultLabel)
        but_box = QHBoxLayout()
        main_box.addLayout(but_box)
        but_back = QPushButton("ОК")
        but_back.setMinimumWidth(130)

        but_back.clicked.connect(lambda :self.hide())
        but_box.addWidget(but_back)

        but_box.addStretch()
        but_open = QPushButton("Открыть файл")
        but_open.setMinimumWidth(110)
        but_open.clicked.connect(self.openFile)
        but_box.addWidget(but_open)

        self.but_export = but_export = QPushButton("Импорт")
        self.but_export.setEnabled(False)
        but_export.setMinimumWidth(110)
        but_export.clicked.connect(self.exportToBase)
        but_box.addWidget(but_export)

    def openFile(self):
        path = os.path.abspath(os.curdir)
        fname = QFileDialog.getOpenFileName(self, 'Open file', path)[0]
        print(fname)
        if not fname:
            return
        with open(fname, "r") as f:
            self.text_file = f.read()
            self.textQT.setPlainText(self.text_file)
        self.but_export.setEnabled(True)
        self.textQT.setReadOnly(False)
        print("openFile")

    def exportToBase(self):
        text = self.textQT.toPlainText()
        print("exportToBase")
        try:
            db.addTextToBase(self.base, text)
            self.resultLabel.setText("Группа добавлена")
            if self.funcUpdate:
                self.funcUpdate()
        except Exception as ex:
            print(ex)
            self.resultLabel.setText("Ошибка! Группа не добавлена")






if __name__ == '__main__':
    app = QApplication(sys.argv)
    _base = db.DateBase("Learning_translate.sqlite")
    window = ExplorerWords(_base)
    window.show()
    sys.exit(app.exec())
