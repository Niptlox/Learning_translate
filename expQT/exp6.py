import sys

from PyQt5.QtSql import *
from PyQt5.QtWidgets import *


P_LANGS = "Languages"
NULL = "NULL"
BASE_WORDS = "Words"
BASE_GROUPS = "Groups"
BASE_WORDS_OF_GROUPS = "WordsGroup"
BASE_LANGUAGES = "Languages"

groupID = 4

st_exec = f"""SELECT {BASE_WORDS}.ID,
                       {BASE_WORDS}.Word,
                       {BASE_LANGUAGES}.ID,
                       {BASE_WORDS}.TranslateID

                  FROM {BASE_WORDS_OF_GROUPS}
                       LEFT JOIN
                       {BASE_WORDS} ON {BASE_WORDS_OF_GROUPS}.WordID = {BASE_WORDS}.ID
                       LEFT JOIN
                       {BASE_LANGUAGES} ON {BASE_WORDS}.LanguageID = {BASE_LANGUAGES}.ID
                       WHERE {BASE_WORDS_OF_GROUPS}.GroupID = {groupID}"""


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Зададим тип базы данных
        db = QSqlDatabase.addDatabase('QSQLITE')
        # Укажем имя базы данных
        db.setDatabaseName('C:\\George\\Programming\\Python\\Projects\\PyQT\\Learning_translate\\Learning_translate.sqlite')
        # И откроем подключение
        db.open()

        # QTableView - виджет для отображения данных из базы
        view = QTableView(self)
        # Создадим объект QSqlTableModel,
        # зададим таблицу, с которой он будет работать,
        #  и выберем все данные
        model = QSqlTableModel(self, db)
        model.setTable('words')
        model.select()

        # Для отображения данных на виджете
        # свяжем его и нашу модель данных
        view.setModel(model)
        view.move(10, 10)
        view.resize(617, 315)

        self.setGeometry(300, 100, 650, 450)
        self.setWindowTitle('Пример работы с QtSql')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())