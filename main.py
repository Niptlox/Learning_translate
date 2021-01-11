import DateBase as db
import sys
import core
import wordsExplorer as WE

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, \
    QStackedLayout, QHBoxLayout, \
    QVBoxLayout, QTableWidget, \
    QTableWidgetItem, QListWidget, QComboBox, \
    QPlainTextEdit, QLineEdit, QFileDialog, QMessageBox, QDialog, QRadioButton

from PyQt5.QtWidgets import QLCDNumber, QLabel


BASESIZETABLE = (400, 300)


class MainWindow(QWidget):
    def __init__(self, base):
        super().__init__()
        self.base = base
        self.initUI()

    def initUI(self):
        self.setStyleSheet("font: 14px;")
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
                                              funcGroup=self.viewGroup,
                                              funcBack=self.visibleMain)

        self.groupWidget = GroupWidget(self.base,
                                              funcStartTest=self.startTest,
                                              funcBack=self.startLearn)

        self.testWidget = TestWidget(self.base, funcFinish=self.viewResult)
        self.resultWidget = ResultWidget(self.base, funcBack=self.viewGroup)


        # self.stackedLayout.addWidget(tw)
        self.stackedLayout.addWidget(self.mainWidget)
        self.stackedLayout.setCurrentIndex(0)
        self.stackedLayout.addWidget(self.groupsWidget)

        self.stackedLayout.addWidget(self.groupWidget)
        self.stackedLayout.addWidget(self.testWidget)
        self.stackedLayout.addWidget(self.resultWidget)

    def viewGroup(self, groupID=None):
        print("groupID", groupID)
        self.groupID = groupID if groupID is not None else self.groupID
        print("self.groupID", self.groupID)
        self.stackedLayout.setCurrentIndex(2)
        self.groupWidget.updateG(self.groupID)

    def startTest(self, groupID, groupName, langID, typeTest):
        self.stackedLayout.setCurrentIndex(3)
        self.testWidget.startTest(groupID, groupName, langID, typeTest)
        self.testWidget.newQestion()

    def viewResult(self, cof, words, maxCWords):
        self.resultWidget.setResult(cof * 100, words, maxCWords)
        self.stackedLayout.setCurrentIndex(4)
        print("viewResult", cof)

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
        butStart = QPushButton("Выбрать тест")
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


class GroupWidget(QWidget):
    def __init__(self, base, funcStartTest=None, funcBack=None):
        super().__init__()
        self.base = base
        self.funcBack = funcBack
        self.funcStartTest = funcStartTest
        # self.funcStartTrain = funcStartTrain
        self.initUI()

    def initUI(self):
        main_box = QVBoxLayout()
        self.setLayout(main_box)
        main_box.addStretch(1)
        self.name_label =QLabel("Группа: ")
        main_box.addWidget(self.name_label)
        self.count_label =QLabel("Количество слов: ")
        main_box.addWidget(self.count_label)
        self.langs_label =QLabel("Языки: ")
        main_box.addWidget(self.langs_label)
        self.langsComboBox = QComboBox()
        self.langsComboBox.setMaximumWidth(350)
        main_box.addWidget(self.langsComboBox)

        butStart = QPushButton("Начать тестирование")
        butStart.clicked.connect(lambda :self.startTest(core.TEST_CONTROL))
        butStart.setMaximumWidth(350)
        butStart.setMinimumHeight(25)
        main_box.addWidget(butStart)

        butStartTrain = QPushButton("Начать тренировкку")
        butStartTrain.clicked.connect(lambda :self.startTest(core.TEST_ENDLESS_LOOP))
        butStartTrain.setMaximumWidth(350)
        butStartTrain.setMinimumHeight(25)
        main_box.addWidget(butStartTrain)

        butExplor = QPushButton("Список слов")
        butExplor.clicked.connect(self.viewWords)
        butExplor.setMaximumWidth(350)
        butExplor.setMinimumHeight(25)
        main_box.addWidget(butExplor)
        main_box.addStretch(1)

        self.butLayout = butLayout = QHBoxLayout()
        main_box.addLayout(butLayout)

        self.butBack = QPushButton("Назад к группам")
        self.butLayout.addStretch()
        self.butBack.clicked.connect(self.funcBack)
        self.butBack.setMinimumWidth(130)
        butLayout.addWidget(self.butBack)

    def startTest(self, typeTest=core.TEST_ENDLESS_LOOP):
        lang = self.langsComboBox.currentText()
        print(lang)
        langID = self.langsD[lang]
        self.funcStartTest(self.groupID, self.groupName, langID, typeTest)


    def updateG(self, groupID):
        self.groupID = groupID
        group = self.base.getGroup(groupID)
        print("group", group)
        name = group["Name"]
        self.groupName = name
        count = str(group["CountWords"])
        self.langs = group["Languages"]
        self.langsD = {langN: idL for idL, langN in group["Languages"]}
        langs = "; ".join(map(lambda x: x[1], self.langs))
        self.langsComboBox.clear()
        self.langsComboBox.addItems(list(map(lambda x: x[1], group["Languages"])))
        self.name_label.setText("Группа: " + name)
        self.count_label.setText("Количество слов: " + count)
        self.langs_label.setText("Языки: " + langs)

    def viewWords(self):
        # print("self.groupID")
        tableWords = WordsGroupWidget(self.base, self.groupID, self.groupName)
        tableWords.show()


class WordsGroupWidget(QDialog):
    def __init__(self, base, groupID, groupName):
        super().__init__()
        self.groupID = groupID
        self.groupName = groupName
        self.base = base
        self.funcBack = self.hide
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Список слов группы ' + self.groupName)
        self.setModal(True)
        main_box = QVBoxLayout()
        self.setLayout(main_box)
        self.table = WE.TableMy(self.base, WE.BASESIZETABLE, typeView=WE.TVIEWGROUP, groupID=self.groupID)
        self.table.updateTable()
        main_box.addWidget(self.table)

        self.butLayout = butLayout = QHBoxLayout()
        main_box.addLayout(butLayout)

        self.butLayout.addStretch()
        self.butBack = QPushButton("ОК")
        self.butBack.clicked.connect(self.funcBack)
        self.butBack.setMinimumWidth(70)
        butLayout.addWidget(self.butBack)


class TestWidget(QWidget):
    def __init__(self, base, funcFinish=None):
        super().__init__()
        self.base = base
        # self.funcBack = funcBack
        self.funcFinish = funcFinish
        self.initUI()

    def initUI(self):

        main_box = QVBoxLayout()
        self.setLayout(main_box)
        self.label = QLabel("Контрольная")
        main_box.addWidget(self.label)
        main_box.addStretch()

        word_box = QHBoxLayout()
        main_box.addLayout(word_box)
        word_box.addWidget(QLabel("Переведите:  "))
        self.wordLabel = QLabel("Word")
        word_box.addWidget(self.wordLabel)
        word_box.addStretch()
        vbox = QVBoxLayout()
        main_box.addLayout(vbox)
        self.n = 3
        self.arRadios = []
        for j in range(self.n):
            radioW = QRadioButton("")
            vbox.addWidget(radioW)
            self.arRadios.append(radioW)
            radioW.clicked.connect(lambda _, _i=j: self.answer(_i))
            print(j)
        self.outLabel = QLabel("Ответ верен")
        main_box.addWidget(self.outLabel)

        main_box.addStretch()

        self.butLayout = butLayout = QHBoxLayout()
        main_box.addLayout(butLayout)

        # self.butLayout.addStretch()
        self.butBack = QPushButton("Остановить тест")
        self.butBack.clicked.connect(self.stopTest)
        # self.butBack.setMinimumWidth(70)
        butLayout.addWidget(self.butBack)

        self.butBack = QPushButton("Далее")
        self.butBack.clicked.connect(self.further)
        # self.butBack.setMinimumWidth(70)
        butLayout.addWidget(self.butBack)

    def further(self):
        if not self.newAnswer:
            self.test.answer("_NOTANSWER_")
        self.newQestion()

    def stopTest(self):
        self.finishTest()

    def startTest(self, groupID, groupName, langID, typeTest=core.TEST_CONTROL):
        if typeTest == core.TEST_CONTROL:
            self.label.setText("Контрольная по модулю " + groupName)
        else:
            self.label.setText("Тренировка по модулю " + groupName)
        self.groupID = groupID
        self.langID = langID
        self.typeTest = typeTest
        self.groupName = groupName
        self.test = core.Test(base, groupID, langID, typeTest=typeTest)


    def newQestion(self):
        self.newAnswer=False
        out = self.test.question()
        if out is None:
            self.finishTest()
            return
        self.que = out
        word, iTrans, trans = out
        self.outLabel.setText("")
        self.wordLabel.setText(word[1])
        for i in range(self.n):
            rad = self.arRadios[i]
            rad.setText(trans[i][1])
            rad.setEnabled(True)
            rad.setAutoExclusive(False)
            rad.setChecked(False)




    def answer(self, numAnswer):
        print("numAnswer", numAnswer)
        self.newAnswer = True
        word, iTrans, trans = self.que
        answer = trans[numAnswer][1]
        out = self.test.answer(answer)
        if out:
            st = "Вы ответили верно"
        else:
            st = f"Вы ответили не верно. Верный ответ {trans[iTrans][1]}"
        self.outLabel.setText(st)
        for i in range(self.n):
            self.arRadios[i].setEnabled(False)

    def finishTest(self):
        print("r")
        result = self.test.result()
        print("result", result)
        # print("Результат", round(result[0] * 100, 2), "баллов;", result[1], "/", result[2], "слов")
        cof, w, maxw = result
        if self.test.typeTest == core.TEST_CONTROL:
            maxw = self.test.getCountWords()
            cof = w / maxw
        try:
            self.funcFinish(cof, w, maxw)
        except Exception as ex:
            print(ex)



class ResultWidget(QWidget):
    def __init__(self, base, funcBack=None):
        super().__init__()
        self.base = base
        self.funcBack = funcBack
        self.initUI()

    def initUI(self):

        main_box = QVBoxLayout()
        self.setLayout(main_box)
        main_box.addStretch()

        res_box = QHBoxLayout()
        main_box.addLayout(res_box)
        res_box.addWidget(QLabel("Результат:"))
        self.resLabel = QLabel("0 баллов")
        res_box.addWidget(self.resLabel)
        res_box.addStretch()

        self.resWLabel = QLabel("Переведено правильно: {words} из {maxWords} слов")
        main_box.addWidget(self.resWLabel)

        main_box.addStretch()

        butLayout = QHBoxLayout()
        main_box.addLayout(butLayout)

        butLayout.addStretch()
        self.butBack = QPushButton("ОК")
        self.butBack.clicked.connect(lambda: self.funcBack())
        self.butBack.setMinimumWidth(70)
        butLayout.addWidget(self.butBack)

    def setResult(self, bals, words, maxWords):
        print(bals, words, maxWords)
        self.resLabel.setText(f"{round(bals, 2)} баллов")
        self.resWLabel.setText(f"Переведено правильно: {words} из {maxWords} слов")
        print(1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    base = db.DateBase("Learning_translate.sqlite")
    window = MainWindow(base)
    window.show()
    sys.exit(app.exec())
