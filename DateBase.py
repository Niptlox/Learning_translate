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
BASE_WORDS = "Words"
BASE_GROUPS = "Groups"
BASE_WORDS_OF_GROUPS = "WordsGroup"
BASE_LANGUAGES = "Languages"


class DateBase():
    def __init__(self, name_db="Learning_translate.sqlite"):
        self.con = sqlite3.connect(name_db)
        self.name_db = name_db
        self.mainLanguageID = self.getLanguageID_Main()

    # get name of db
    def getName(self):
        return self.name_db

    # add group words and translate
    def addDict(self, dictW, group, newGroup=False):
        if newGroup:
            groupID = self.createGroup(group)
        else:
            out = self.getGroupID(group)
            groupID = self.createGroup(group) if out is None else out
        langs = dictW.pop(P_LANGS)
        langID1 = self.getLanguageID(langs[0])
        langID2 = self.getLanguageID(langs[1])
        words = list(dictW.items())
        for word1, word2 in dictW.items():
            out = self.addWord(word1, LanguageID=langID1, newCommit=False)
            print(out)
            if out:
                wordID, translateID = out
                self.addWordToGroup(wordID, groupID)
                out = self.addWord(word2, LanguageID=langID2,
                                   translateID=translateID, newCommit=False)
                if out:
                    wordID, translateID = out
                    self.addWordToGroup(wordID, groupID)
        self.commit()

    # add word and translate to datebase and return wordID, translateID
    def addWord(self, word, translateID=NULL, LanguageID=NULL, descript=NULL, newCommit=True):
        LanguageID = self.mainLanguageID if LanguageID == NULL else LanguageID
        translateID = self.getNewTranslateID() if translateID == NULL else translateID
        out = self.wordInBase(word, LanguageID)
        if out:
            return out
        descript = str(descript)
        wordID = self.getNewWordID()
        cur = self.con.cursor()
        print(f"VALUES{(wordID, word, translateID, LanguageID, descript)}")
        cur.execute(f"""INSERT INTO {BASE_WORDS}(ID, Word, LanguageID, TranslateID, Description)
                        VALUES{(wordID, word, LanguageID, translateID, descript)}""")
        if newCommit:
            self.commit()
        return wordID, translateID

    # get word (ID, Word, (LanguageID, Language), TranslateID, Description)
    def getWord(self, wordID):
        cur = self.con.cursor()

        st_exec = f"""SELECT {BASE_WORDS}.ID, Word, LanguageID, TranslateID, Description, {BASE_LANGUAGES}.Language  
                      FROM {BASE_WORDS} 
                      LEFT JOIN {BASE_LANGUAGES} ON LanguageID = {BASE_LANGUAGES}.ID                              
                      WHERE {BASE_WORDS}.ID = {wordID}"""

        arW = list(cur.execute(st_exec).fetchone())
        lang = (arW[2], arW.pop(-1))
        arW[2] = lang
        return arW

    def getAllWords(self):
        cur = self.con.cursor()

        st_exec = f"""SELECT ID, 
        Word, 
        LanguageID, 
        (SELECT Language FROM {BASE_LANGUAGES} WHERE LanguageID = ID),
        TranslateID,
        Description
         FROM  {BASE_WORDS}"""
        arW = cur.execute(st_exec).fetchall()
        return arW

    # del word
    def delWord(self, wordID, delFromGroups=True, commit=True):
        cur = self.con.cursor()
        cur.execute(f"""DELETE FROM {BASE_WORDS}
                        WHERE ID = {wordID}""")
        if delFromGroups:
            cur.execute(f"""DELETE FROM {BASE_WORDS_OF_GROUPS}
                            WHERE WordID = {wordID}""")
        if commit:
            self.commit()

    # edit word
    def editWord(self, wordID, word=NULL, LanguageID=NULL, translateID=NULL, description=NULL, commit=True):
        st_exec = f"""UPDATE {BASE_WORDS} SET """
        st_exec += f"Word = '{word}' " if word is not NULL else ""
        st_exec += f"LanguageID = '{LanguageID}'" if LanguageID is not NULL else ""
        st_exec += f"TranslateID = '{translateID}'" if translateID is not NULL else ""
        st_exec += f"Description = '{description}'" if description is not NULL else ""
        st_exec += f"WHERE ID = {wordID}"
        cur = self.con.cursor()
        cur.execute(st_exec)
        if commit:
            self.commit()

    # commit conection DateBase
    def commit(self):
        self.con.commit()

    # get all groups and params
    def getGroups(self):
        st_exec = f"""SELECT {BASE_GROUPS}.ID,
                             {BASE_GROUPS}.GroupName,
                             COUNT({BASE_WORDS}.LanguageID),
                             {BASE_LANGUAGES}.Language,
                             {BASE_LANGUAGES}.ID
                          FROM {BASE_WORDS_OF_GROUPS}
                               LEFT JOIN
                               {BASE_WORDS} ON {BASE_WORDS_OF_GROUPS}.WordID = {BASE_WORDS}.ID
                               LEFT JOIN
                               {BASE_GROUPS} ON {BASE_WORDS_OF_GROUPS}.GroupID = {BASE_GROUPS}.ID
                               LEFT JOIN 
                               {BASE_LANGUAGES} ON {BASE_WORDS}.LanguageID = {BASE_LANGUAGES}.ID
                        GROUP BY {BASE_GROUPS}.ID, {BASE_WORDS}.LanguageID;"""
        cur = self.con.cursor()
        res = cur.execute(st_exec).fetchall()
        out = []
        lastID = None
        for st in res:
            groupID, groupName, countW, lang, langID = st
            if lastID == groupID:
                out[-1][P_LANGS].append((langID, lang))
            else:
                d = {"ID": groupID, "Name": groupName, "CountWords": countW, P_LANGS: [(langID, lang)]}
                out.append(d)
                lastID = groupID

        # print(out)
        return out

    # get words for groupID
    def getWordsOfGroup(self, groupID):
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
        cur = self.con.cursor()
        res = cur.execute(st_exec).fetchall()
        dictWords = {}
        for st in res:
            wordID, word, langID, translateID = st
            if langID not in dictWords:
                dictWords[langID] = {}
            dictWords[langID][translateID] = (wordID, word)
        # print(dictWords)
        return dictWords

    def getWordsOfGroupSTR(self, groupID):
        st_exec = f"""SELECT ID,
                           Word,
                           (SELECT Language FROM {BASE_LANGUAGES} WHERE LanguageID = ID),
                           LanguageID,       
                           TranslateID
                        FROM {BASE_WORDS}
                        LEFT JOIN {BASE_WORDS_OF_GROUPS} ON WordsGroup.WordID = ID
                        WHERE GroupID = {groupID};"""
        cur = self.con.cursor()
        res = cur.execute(st_exec).fetchall()
        dictWords = {}
        for st in res:
            wordID, word, lang, langID, translateID = st
            if translateID not in dictWords:
                dictWords[translateID] = []
            dictWords[translateID].append((wordID, word, langID, lang))
        # print(dictWords)
        return dictWords

    def execute(self, st_exec, commit=False):
        cur = self.con.cursor()
        res = cur.execute(st_exec)
        if commit:
            self.commit()
        return res

    # add word to group
    def addWordToGroup(self, wordID, groupID, commit=True):
        cur = self.con.cursor()
        cur.execute(f"""INSERT INTO {BASE_WORDS_OF_GROUPS}(GroupID, WordID)
                        VALUES{(groupID, wordID)}""")
        if commit:
            self.con.commit()

    # del word from group
    def delWordOfGroup(self, wordID, groupID, commit=True):
        cur = self.con.cursor()
        cur.execute(f"""DELETE FROM {BASE_WORDS_OF_GROUPS}
                        WHERE GroupID = {groupID} AND WordID = {wordID}""")
        if commit:
            self.con.commit()

    # create new group
    def createGroup(self, group):
        groupID = self.getNewGroupID()
        print(group)
        group = f"{group}"
        cur = self.con.cursor()
        st = f"""INSERT INTO {BASE_GROUPS}(ID, GroupName)
                                VALUES{(groupID, group)}"""
        print(st)
        cur.execute(st)
        self.con.commit()
        return groupID

    # get all languagesID of groupID
    def getLanguagesGroup(self, groupID):
        st = f"""SELECT
                    {BASE_WORDS}.LanguageID,
                    COUNT({BASE_WORDS}.LanguageID)
                FROM
                    {BASE_WORDS_OF_GROUPS}
                LEFT JOIN {BASE_WORDS} ON {BASE_WORDS_OF_GROUPS}.ID = {BASE_WORDS}.ID
                WHERE ID = {groupID}
                GROUP BY {BASE_WORDS}.LanguageID;"""
        cur = self.con.cursor()
        res = cur.execute(st).fetchall()
        print(res)
        return res

    # get wordID and TranslateID in Base for word and LanguageID
    def wordInBase(self, word, LanguageID):
        cur = self.con.cursor()
        word = word.replace("'", "''")
        st = f"""SELECT ID, TranslateID
                 FROM {BASE_WORDS}
                 WHERE Word = '{word}' AND LanguageID = {LanguageID}"""
        res = cur.execute(st).fetchone()
        res = [] if res is None else res
        return res

    # get ID translate group of wordID
    def getTranslateIDOfWord(self, wordID):
        cur = self.con.cursor()
        st = f"""SELECT translateID
                 FROM {BASE_WORDS}
                 WHERE ID = {wordID}"""
        res = cur.execute(st).fetchone()[0]
        return res

    # get translate word and wordID of wordID
    def getTranslateOfWordID(self, wordID, LanguagesID):
        st = f"""SELECT ID, Word
                   FROM {BASE_WORDS}
                 WHERE TranslateID = (
                                               SELECT TranslateID
                                                 FROM {BASE_WORDS}
                                                WHERE ID = {wordID} 
                                           )
                 AND 
                       LanguageID = {LanguagesID};"""
        cur = self.con.cursor()
        res = cur.execute(st).fetchone()
        return res

    # get new numID for column in table
    def getNewTableID(self, table, column="ID"):
        cur = self.con.cursor()
        res = cur.execute(f"SELECT MAX({column}) FROM {table}").fetchone()[0]
        res = 1 if res is None else res + 1
        return res

    # get new ID for new word
    def getNewWordID(self):
        return self.getNewTableID(BASE_WORDS)

    # get new ID for new group
    def getNewGroupID(self):
        return self.getNewTableID(BASE_GROUPS)

    # get new ID for translation group
    def getNewTranslateID(self):
        return self.getNewTableID(BASE_WORDS, column="TranslateID")

    # get ID of name language
    def getLanguageID(self, Language):
        cur = self.con.cursor()
        result = cur.execute(f"""SELECT ID FROM {BASE_LANGUAGES}
                WHERE Language = '{Language}'""").fetchone()[0]
        return result

    # get dict {ID: (name, is_main)} of all languages
    def getAllLanguage(self):
        cur = self.con.cursor()
        result = cur.execute(f"""SELECT ID, Language, MainLanguage FROM {BASE_LANGUAGES}""").fetchall()
        d = {r[0]: r[1:] for r in result}
        return d

    # get all groups of word
    def getGroupsWord(self, wordID):
        cur = self.con.cursor()
        result = cur.execute(f"""SELECT GroupID, GroupName  
        FROM {BASE_WORDS_OF_GROUPS}
        LEFT JOIN {BASE_GROUPS} ON GroupID = {BASE_GROUPS}.ID
        WHERE WordID = {wordID}""").fetchall()
        return result

    # get all Translates of word
    def getTranslatesWord(self, wordID):
        st = f"""SELECT ID, Word, LanguageID, (SELECT Language
                                                FROM {BASE_LANGUAGES}
                                                WHERE {BASE_LANGUAGES}.ID = LanguageID)
        FROM {BASE_WORDS}         
        WHERE TranslateID = (
                                   SELECT TranslateID
                                     FROM {BASE_WORDS}
                                    WHERE ID = {wordID} 
                               ) AND
        ID != {wordID}"""
        cur = self.con.cursor()
        res = cur.execute(st).fetchall()
        return res



    # get ID of name group
    def getGroupID(self, group):
        cur = self.con.cursor()
        result = cur.execute(f"""SELECT ID FROM {BASE_GROUPS}
                WHERE GroupName = '{group}'""").fetchone()[0]
        return result

    # get ID of main language
    def getLanguageID_Main(self):
        cur = self.con.cursor()
        result = cur.execute(
            f"""SELECT ID FROM {BASE_LANGUAGES} WHERE MainLanguage = 1""").fetchone()[0]
        return result


def addFileToBase(base, file="moduls/Bedroom.txt"):
    with open(file) as f:
        modul_name = f.readline().replace(" ", "")[1:-2]
        langs = f.readline().replace(" ", "")[1:-2].split(";")
        text = list(filter(lambda st: st != "", f.read().splitlines()))
        words = {text[i]: text[i + 1] for i in range(0, len(text), 2)}
    words[P_LANGS] = langs
    # print(words, modul_name)
    base.addDict(words, modul_name, newGroup=True)


if __name__ == '__main__':
    base = DateBase()
    print(*base.getGroups(), sep="\n\n")
    print(base.getWordsOfGroup(2))
    nameF = "moduls/think.txt"
    addFileToBase(base, nameF, newGroup=False)
    # print(base.getWord(74))
