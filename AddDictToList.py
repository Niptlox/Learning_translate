import sqlite3

# engw = "qwertyuiopasdfghjklzxcvbnm"

# SELECT перечень_полей FROM имя_таблицы
#         WHERE условие
# WHERE duration IN (45, 90)
# WHERE duration BETWEEN 45 AND 60

# WHERE title LIKE 'А_к%'
# % — обозначает любое количество, в том числе нулевое, любых символов
# _ — обозначает один любой символ

# SELECT title FROM Films
#     WHERE genre=(
# SELECT id FROM genres
#     WHERE title = 'фантастика')

# INSERT INTO имя_таблицы(названия_полей*) VALUES(значения)

# UPDATE имя_таблицы
# SET название_колонки = новое_значение
# WHERE условие

# DELETE from films
# where year < 1985

# .fetchall()  все полученные элементы
# .fetchone(),  первый элемент,
# .fetchmany(n) n первых записей.

P_LANGS = "Languages"
NULL = "NULL"
BASE_WORDS = "AllWords"
BASE_GROUPS = "AllGroups"
BASE_WORDS_OF_GROUPS = "WordsOfGroups"
BASE_LANGUAGES = "Languages"


class DateBase():
    def __init__(self, name_db="Learning_translate.sqlite"):
        self.con = sqlite3.connect(name_db)
        self.name_db = name_db
        self.mainLanguageID = self.getLanguageID_Main()

    # add group words and translate
    def addDict(self, dictW, group, newGroup=True):
        groupID = self.createGroup(group) if newGroup else group
        langs = dictW.pop(P_LANGS)
        langID1 = self.getLanguageID(langs[0])
        langID2 = self.getLanguageID(langs[1])
        words = list(dictW.items())
        for word1, word2 in dictW.items():
            out = self.addWord(word1, LanguageID=langID1)
            if out:
                wordID, translateID = out
                self.addWordToGroup(wordID, langID1, groupID)
                out = self.addWord(word2, LanguageID=langID2, translateID=translateID)
                if out:
                    wordID, translateID = out
                    self.addWordToGroup(wordID, langID2, groupID)

    # add word and translate to datebase and return wordID, translateID
    def addWord(self, word, translateID=NULL, LanguageID=NULL, descript=NULL):
        LanguageID = self.mainLanguageID if LanguageID == NULL else LanguageID
        translateID = self.getNewTranslateID if translateID == NULL else translateID
        if self.wordInBase(word, LanguageID):
            return
        descript = f"'{descript}'" if descript is not NULL else descript
        wordID = self.getNewWordID()
        word = f"'{word}'"
        cur = self.con.cursor()
        cur.execute(f"""INSERT INTO {BASE_WORDS}(WordID, Word, LanguageID, TranslateID, Description)
                        VALUES{(wordID, word, translateID, LanguageID, descript)}""")
        self.con.commit()
        return wordID, translateID

    # add word to group of words or and create New Group
    def addWordToGroup(self, wordID, LanguageID, groupID):
        cur = self.con.cursor()
        cur.execute(f"""INSERT INTO {BASE_WORDS_OF_GROUPS}(GroupID, WordID, LanguageID)
                        VALUES{(groupID, wordID, LanguageID,)}""")
        self.con.commit()

    #     create new group
    def createGroup(self, group):
        groupID = self.getNewGroupID()
        print(group)
        group = f"{group}"
        cur = self.con.cursor()
        st = f"""INSERT INTO {BASE_GROUPS}(GroupID, GroupName)
                                VALUES{(groupID, group)}"""
        print(st)
        cur.execute(st)
        self.con.commit()
        return groupID

    # This word in DateBase?
    def wordInBase(self, word, LanguageID):
        cur = self.con.cursor()
        word = word.replace("'", "''")
        st = f"""SELECT Word
                 FROM {BASE_WORDS}
                 WHERE Word = '{word}' AND LanguageID = {LanguageID}"""
        print(st)
        res = cur.execute(st).fetchone()
        res = [] if res is None else res
        return list(res) != 0

    # get ID translate group of wordID
    def getTranslateIDOfWord(self, wordID):
        cur = self.con.cursor()
        st = f"""SELECT translateID
                 FROM {BASE_WORDS}
                 WHERE WordID = {wordID}"""
        res = cur.execute(st).fetchone()[0]
        return res

    # get new ID for new word
    def getNewWordID(self):
        cur = self.con.cursor()
        res = cur.execute(f"SELECT MAX(WordID) FROM {BASE_WORDS})").fetchone()[0]
        res = 1 if res is None else res + 1
        return res

    # get new ID for new group
    def getNewGroupID(self):
        cur = self.con.cursor()
        res = cur.execute(f"SELECT MAX(GroupID) FROM {BASE_GROUPS}").fetchone()[0]
        res = 1 if res is None else res + 1
        # print(res)
        return res

    # get new ID for translation group
    def getNewTranslateID(self):
        cur = self.con.cursor()
        res = cur.execute(f"SELECT MAX(TranslateID) FROM {BASE_WORDS})").fetchone()[0]
        res = 1 if res is None else res + 1
        return res

    # get ID of name language
    def getLanguageID(self, Language):
        cur = self.con.cursor()
        result = cur.execute(f"""SELECT ID FROM {BASE_LANGUAGES}
                WHERE Language = '{Language}'""").fetchone()[0]
        return result

    # get ID of main language
    def getLanguageID_Main(self):
        cur = self.con.cursor()
        result = cur.execute(
            f"""SELECT ID FROM {BASE_LANGUAGES} WHERE MainLanguage = 1""").fetchone()
        return result


rusw = "йцукенгшщзхъфывапролджэячсмитьбюё"


def openfile(namef="moduls/household.txt"):
    f = open(namef)
    text = f.read().split("\n")
    text = [st.replace("\n", "") for st in text]
    words = []
    i = -1
    nper = False
    for st in text:
        if st != "":
            if st[0].lower() not in rusw:
                # nper = False
                nper = True
                i += 1
                words.append([""])
                words[i][0] = st
                ip = 1
            elif nper:
                # print(st,i,len(words))
                words[i].append("")
                words[i][ip] = st
                ip += 1
    return words


def add_dict_to_table(file, langs=["Английский", "Русский"], group=NULL):
    ar = openfile(file)
    # [["wordEng", "wordRus"], ["wordEng2", "wordRus2"]]
    d = {}
    d.update(ar)
    print(d, ar)
    # {"wordEng": "wordRus", "wordEng2": "wordRus2"}
    d[P_LANGS] = langs
    group = file if group is NULL else group
    base = DateBase()
    base.addDict(d, group)


ar = openfile()
file = "moduls/household.txt"
name = "Household"
langs = ["Английский", "Русский"]
add_dict_to_table(file, langs, "household")
