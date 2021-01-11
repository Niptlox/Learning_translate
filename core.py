from random import randint, sample, choice, shuffle
import DateBase as db

# максимальный размер списка для дальнецйшего подбора слов в ответы
MAX_WORDS_LIST = 100
TEST_ENDLESS_LOOP = "ENDLESS_LOOP"
TEST_COUNT_LOOP = "COUNT_LOOP"
TEST_CONTROL = "CONTROL"
LEARN_COF = 1
LEARN_MAX = 5
LEARN_MIN = -5


class Test():
    def __init__(self, base, groupID, langID, typeTest=TEST_ENDLESS_LOOP, countAnswers=None, selections=3):
        self.base, self.groupID, self.langID = base, groupID, langID
        self.typeTest = typeTest
        self.selections = selections
        self.words = self.base.getWordsOfGroup(groupID)
        print(self.words)
        # self.errors = {self.words[langID][transKey][0]: 0 for transKey in self.words[langID].keys()}
        self.errors = {transKey: 0 for transKey in self.words[langID].keys()}
        self.traslateLangID = [k for k in self.words.keys() if k != langID][0]
        self.keys = list(self.errors.keys())
        print(self.errors)
        self.countWords = len(self.errors)
        # если количество вопросов == None, то по умолчанию это количество слов
        self.countAnswers = countAnswers if countAnswers is not None else self.countWords
        self.wordsList = sample(self.keys, min(self.countAnswers, self.countWords))
        self.nowCAnswers = 0  # количество отвеченых вопросов
        self.trueCAnswers = 0  # количество правильно отвеченых вопросов
        self.i = 0
        self.lastWord = None
        self.selections = selections

    def question(self):
        # индекс для слова
        iWord = randint(0, self.selections - 1)
        if self.typeTest == TEST_ENDLESS_LOOP:
            # создаем массив с ошибками и рандомным шумом и кличами translate групп
            wordsList = [[er + randint(-1, 3), k] for k, er in self.errors.items()]
            # сортируем массив для получения слов с наибольшими ошибками
            wordsList.sort(reverse=True)
            # выбираем из них топ который быдем использовать а также убираем покозатель ошибки
            words = list(map(lambda x: x[1], wordsList[0:self.selections]))
        if self.typeTest == TEST_CONTROL:
            if self.nowCAnswers == self.countWords:
                return
            # выбираем рандомный список ответов
            words = sample(self.keys, self.selections)
            print(list(self.words.keys()))
            # получаем ключ от правильной пары
            keyWord = self.wordsList.pop(0)
            # вставлеяем по индексу правильный ответ
            if keyWord not in words:
                words[iWord] = keyWord
            else:
                iWord = words.index(keyWord)
        # print(self.words)
        # номер translte группы слова
        self.questionTranslate = words[iWord]
        print("words", words)
        # берем id и текст от правильного слово из ответов
        word = self.words[self.langID][self.questionTranslate]
        self.questionWord = word
        # берем id и текст слов списка для выбора ответа
        # print(words)
        translateWords = [self.words[self.traslateLangID][keyWord] for keyWord in words]
        self.answerWord = translateWords[iWord]
        return word, iWord, translateWords

    def getCountWords(self):
        return self.countWords

    def answer(self, word):
        self.nowCAnswers += 1
        if self.typeTest in (TEST_ENDLESS_LOOP, TEST_CONTROL):
            # qID, qWord = self.questionWord
            learn_cof = LEARN_COF
            learn_max = LEARN_MAX
            learn_min = LEARN_MIN
            # получаем ошибку для изменения коофицента ошибки у слова
            erWord = self.errors[self.questionTranslate]
            print("self.errors:", self.errors)
            # print("erWord", erWord)
            out = self.answerWord[1] == word
            if out:
                erWord = max(erWord - learn_cof, learn_min)
                self.trueCAnswers += 1
            else:
                erWord = min(erWord + learn_cof * 1.5, learn_max)
            self.errors[self.questionTranslate] = erWord
            return out

    def result(self):
        nca = self.nowCAnswers
        trueCof = (self.trueCAnswers / nca) if nca != 0 else 0
        return trueCof, self.trueCAnswers, self.nowCAnswers


class Learning_translate():
    def __init__(self):
        self.base = db.DateBase("Learning_translate.sqlite")

    def newLesson(self, groupID, languageID):
        # words = self.base.getWordsOfGroup(groupID)
        self.test = Test(self.base, groupID, languageID)


if __name__ == '__main__':
    base = db.DateBase("Learning_translate.sqlite")
    groups = base.getGroups()
    for group in groups:
        print(f'{group["ID"]}. Группа: {group["Name"]}  Количество слов: {group["CountWords"]}')
        langs = group['Languages']
        print(f"Языки:", "; ".join([f"{x[0]}. {x[1]}" for x in langs]))
        print()
    groupID = int(input("Номер группы:"))
    langID = int(input("Номер языка:"))

    test = Test(base, groupID, langID, typeTest=TEST_CONTROL)
    test = Test(base, groupID, langID, typeTest=TEST_ENDLESS_LOOP)

    while True:
        out = test.question()
        if out is None:
            break
        word, iTrans, trans = out
        print("Переведите:", word[1])
        for i in range(len(trans)):
            print(i + 1, trans[i][1])

        numAnswer = int(input("Введите номер перевода:"))
        if numAnswer == 0:
            break
        answer = trans[numAnswer-1][1]
        out = test.answer(answer)
        print("Вы ответили верно" if out else f"Вы ответили не верно. Верный ответ {trans[iTrans][1]}")
        print()
    result = test.result()
    print("Результат", round(result[0] * 100, 2), "баллов;", result[1], "/", result[2], "слов")
