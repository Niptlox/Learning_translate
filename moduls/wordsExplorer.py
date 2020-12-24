import DateBase as db

import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, \
    QStackedLayout, QHBoxLayout, \
    QVBoxLayout, QTableWidget, \
    QTableWidgetItem, QListWidget, QPlainTextEdit

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


def createTable(size, headerLabels, widthColumns, lastStretch=True, maximumHeight=None):
    # size = (400, 300)
    w, h = size
    n = len(headerLabels)
    print("len(headerLabels)", (headerLabels))
    table = QTableWidget(0, n)
    table.setHorizontalHeaderLabels(headerLabels)
    # table.setMaximumSize(*size)
    # table.setFixedSize(*size)

    table.setMinimumSize(*size)
    if maximumHeight:
        table.setMaximumHeight(maximumHeight)
    for i in range(n):
        w_c = widthColumns[i]
        if w_c is not None:
            table.setColumnWidth(i, w_c if w_c > 1 else w_c * w)
    table.setSelectionBehavior(QAbstractItemView.SelectRows)
    table.setSelectionMode(QAbstractItemView.SingleSelection)
    table.setEditTriggers(QAbstractItemView.NoEditTriggers)
    table.horizontalHeader().setStretchLastSection(lastStretch)
    table.verticalHeader().hide()
    table.horizontalHeader().setSectionResizeMode(n - 1, QHeaderView.ResizeToContents)
    # table.verticalHeader()
    return table


class ExplorerWords(QWidget):
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
        self.setWindowTitle("Браузер слов")
        self.stackedLayout = QStackedLayout()
        self.groupsWidget = TableGroupsWidget(self.base, funcVisibleGroup=self.visibleGroup)
        self.wordsWidget = TableWordsWidget(self.base,
                                            funcVisibleWord=self.visibleWord,
                                            funcBack=self.visibleGroups)

        self.wordVWidget = ViewWordWidget(self.base,
                                          funcEditWord=lambda x: print("EditWord " + str(x)),
                                          funcBack=lambda: self.visibleGroups(self.groupID))

        self.stackedLayout.addWidget(self.groupsWidget)
        self.stackedLayout.setCurrentIndex(0)
        self.stackedLayout.addWidget(self.wordsWidget)
        self.stackedLayout.addWidget(self.wordVWidget)
        self.main_box.addLayout(self.stackedLayout)

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
        self.wordVWidget.setWord(wordID)
        self.stackedLayout.setCurrentIndex(2)


class TableGroupsWidget(QWidget):
    def __init__(self, base, funcVisibleGroup=None):
        super().__init__()
        self.base = base
        self.funcVisibleGroup = lambda: funcVisibleGroup(self.IDsGroup[self.table.currentRow()])
        self.initUI()

    def initUI(self):
        main_box = QVBoxLayout()
        self.table = self.createTable()

        self.table.cellClicked.connect(self.activCell)
        self.table.cellDoubleClicked.connect(self.funcVisibleGroup)

        main_box.addWidget(self.table)
        self.butLayout = butLayout = QHBoxLayout()
        butLayout.addStretch()
        main_box.addLayout(butLayout)
        self.butVisible = butVisible = QPushButton("Просмотр")
        # butVisible.setEnabled(False)
        butVisible.clicked.connect(self.funcVisibleGroup)
        butVisible.setMinimumWidth(130)

        butLayout.addWidget(butVisible)

        self.fillTable()
        self.setLayout(main_box)

    def createTable(self):
        size = (400, 300)
        w, h = size
        self.headerLabels = ['Группа', 'Количество пар', 'Языки']
        table = createTable(size, self.headerLabels, [w * 0.25, w * 0.37, None], lastStretch=True)
        return table

    def fillTable(self):
        self.butVisible.setEnabled(False)
        table = self.table
        table.clear()
        groups = self.base.getGroups()
        n = len(groups)
        print("len(groups)", n)
        table.setRowCount(n)
        table.setHorizontalHeaderLabels(self.headerLabels)
        self.IDsGroup = []
        for i_g in range(n):
            group = groups[i_g]
            self.IDsGroup.append(group["ID"])
            # table.insertRow(i_g)
            langs = group['Languages']
            print(f'{group["ID"]}. Группа: {group["Name"]}  Количество слов: {group["CountWords"]} \n Языки: {langs}')
            labels = (group["Name"], str(group["CountWords"]), "; ".join(map(lambda x: x[1], langs)))
            for i_c in range(3):
                item = QTableWidgetItem(labels[i_c])
                table.setItem(i_g, i_c, item)
        return table

    def activCell(self, row, coumn):
        print("activCell:", row, coumn)
        self.butVisible.setEnabled(True)


class TableWordsWidget(QWidget):
    def __init__(self, base, funcVisibleWord=None, funcBack=None):
        super().__init__()
        self.base = base
        self.funcVisibleWord = lambda: funcVisibleWord(self.IDsWords[self.table.currentRow()])
        self.funcBack = funcBack
        # self.groupID = groupID
        self.initUI()

    def initUI(self):
        main_box = QVBoxLayout()
        main_box.addWidget(QLabel(f"Группа"))

        self.table = self.createTable()
        self.table.cellClicked.connect(self.activCell)
        self.table.cellDoubleClicked.connect(self.funcVisibleWord)

        main_box.addWidget(self.table)
        self.butLayout = butLayout = QHBoxLayout()
        main_box.addLayout(butLayout)

        self.butBack = butBack = QPushButton("Назад к группам")
        butBack.clicked.connect(self.funcBack)
        butBack.setMinimumWidth(130)
        butLayout.addWidget(butBack)

        butLayout.addStretch()

        self.butVisible = butVisible = QPushButton("Просмотр")
        butVisible.setEnabled(False)
        butVisible.clicked.connect(self.funcVisibleWord)
        butVisible.setMinimumWidth(130)
        butLayout.addWidget(butVisible)

        self.setLayout(main_box)

    def createTable(self):
        size = (400, 300)
        w, h = size
        self.headerLabels = ['Слово', 'Язык', 'Перевод']
        table = createTable(size, self.headerLabels, [w * 0.37, w * 0.25, None], lastStretch=True)
        return table

    def fillTable(self, groupID=None):
        self.butVisible.setEnabled(False)
        self.table.scrollToTop()
        table = self.table
        groupID = self.groupID if groupID is None else groupID
        table.clear()
        words = self.base.getWordsOfGroup(groupID)
        langs = self.base.getAllLanguage()
        # преводим к виду (((ид1, слово1, ид_языка1), (ид2, слово2, ид_языка2)),
        # ((ид3, слово3, ид_языка1), (ид4, слово4, ид_языка2)))
        words = list(
            zip(*map(lambda x: map(lambda y: list(y[1]) + [x[0]], sorted(x[1].items())), sorted(words.items()))))
        n = len(words) * 2
        table.setRowCount(0)
        table.setHorizontalHeaderLabels(['Слово', 'Язык', 'Перевод'])
        self.IDsWords = []
        for i_g in range(n // 2):
            # группа слов однокового перевода
            groupWord = words[i_g]
            i_w = 0
            for Word in groupWord:
                idWord, word, idLang = Word
                self.IDsWords.append(idWord)
                table.insertRow(i_g)

                # print(f'{group["ID"]}. Группа: {group["Name"]}  Количество слов: {group["CountWords"]} \n Языки: {langs}')
                labels = (word, langs[idLang][0], groupWord[(i_w + 1) % len(groupWord)][1])
                print("labels word:", labels)
                for i_c in range(len(labels)):
                    item = QTableWidgetItem(labels[i_c])
                    table.setItem(i_g, i_c, item)
                i_g += 1
                i_w += 1
        return table

    def activCell(self, row, coumn):
        print("activCell:", row, coumn)
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
        self.headerTranslate = ["Перевод", "Язык"]
        self.tableTranslate = createTable(sizeT, self.headerTranslate, [0.6, None])
        main_box.addWidget(self.tableTranslate)

        main_box.addWidget(QLabel("Группы"))
        sizeT = (400, 80)
        self.tableGroups = createTable(sizeT, [""], [None], maximumHeight=80)
        self.tableGroups.horizontalHeader().hide()
        main_box.addWidget(self.tableGroups)

        # self.table.cellClicked.connect(self.activCell)
        # self.table.cellDoubleClicked.connect(self.funcVisibleWord)

        self.butLayout = butLayout = QHBoxLayout()
        main_box.addLayout(butLayout)

        self.butBack = QPushButton("Назад")
        self.butBack.clicked.connect(self.funcBack)
        self.butBack.setMinimumWidth(130)
        butLayout.addWidget(self.butBack)

        self.butLayout.addStretch()

        self.butEdit = QPushButton("Изменить")
        self.butEdit.clicked.connect(self.editWord)
        self.butEdit.setMinimumWidth(130)
        butLayout.addWidget(self.butEdit)
        main_box.addStretch()

    def setWord(self, idWord):
        self.idWord = idWord
        print(1)
        Word = self.base.getWord(idWord)
        print(Word)
        idWord, word, lang, translateID, descript = Word
        langID, lang = lang
        self.labelWord.setText("Слово:\t" + word)
        self.labelLang.setText("Язык:\t" + lang)
        self.textDiscript.setPlainText(descript)
        self.textDiscript.setEnabled(False)
        self.tableGroups.setRowCount(0)
        self.tableGroups.setHorizontalHeaderLabels(["Группа", "Zpsrb"])
        i_g = 0
        for Group in base.getGroupsWord(idWord):
            print("Group:", Group)
            groupID, group = Group
            self.tableGroups.insertRow(i_g)
            labels = (group, )
            for i_c in range(len(labels)):
                item = QTableWidgetItem(labels[i_c])
                self.tableGroups.setItem(i_g, i_c, item)
                print("label", labels[i_c])
            i_g += 1


    def editWord(self):
        self.funcEditWord(self.wordID)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    base = db.DateBase("Learning_translate.sqlite")

    window = ExplorerWords(base)
    window.show()
    sys.exit(app.exec())
