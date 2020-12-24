from random import randint
import os

engw = "qwertyuiopasdfghjklzxcvbnm"
rusw = "йцукенгшщзхъфывапролджэячсмитьбюё"
Now_modul = None


def moduls(cotalog="moduls/"):
    global Now_modul
    # Каталог из которого будем брать файлы
    directory = cotalog

    # Получаем список файлов в переменную files
    files = os.listdir(directory)
    files = filter(lambda x: x.endswith('.txt'), files)
    files = list(map(lambda x: x[:-4], files))
    print(*files, sep="\n")
    modul = ""
    while modul not in files:
        modul = input("Модуль:")
        if modul == "" and Now_modul != None:
            modul = Now_modul
            print("Предыдущий модуль:", modul)

    # print("sda")
    Now_modul = modul
    return modul


def openfile(namef="my.txt"):
    try:
        f = open(namef)
    except:
        return False
    text = f.read().split("\n")
    text = [st.replace("\n", "") for st in text]
    words = []
    i = -1
    nper = False
    for st in text:
        if st != "":
            if st[0] in engw:
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


def engrus1(words, owords, kolviv):
    # Не рабочий
    ochki = 0
    l = len(words)
    aw = [0] * (l)
    for i in range(kolviv):
        for io in range(l):
            aw[io] = [randint(0, 8) + owords[io][0], io]
        # print(aw)
        aw.sort()
        iw = aw[::-1][0][1]
        w = words[iw]
        # aw[iw] += 1
        # kper = len(w) - 1

        print("Переведите:", w[0])
        per = input()
        if per == w[1]:
            print("Вы перевели правильно, перевод:", w[1])
            if owords[iw][0] > -3:
                owords[iw][0] -= 1
            ochki += 1
        else:
            print("Вы перевели не правильно, перевод:", w[1])

            if owords[iw][0] < 5:
                owords[iw][0] += 2

        print()
    return ochki


def ruseng2(words, kolviv):
    ochki = 0
    l = len(words)
    aw = [0] * (l)
    for i in range(kolviv):
        for io in range(l):
            aw[io] = [randint(0, 8) + owords[io][0], io]
        # print(aw)
        aw.sort()
        iw = aw[::-1][0][1]
        w = words[iw]
        # kper = len(w) - 1

        print("Переведите:", w[1])
        iw2 = randint(0, l - 1)
        iw3 = randint(0, l - 1)
        am = [[randint(0, 100), iw, True], [randint(0, 100), iw2, False],
              [randint(0, 100), iw3, False]]

        am.sort()
        i = 1
        for m in am:
            print(i, words[m[1]][0])
            i += 1
        trv = False
        per = -1
        while trv == False or 1 > per or per > 3:
            try:
                per = int(input())
                trv = True
            except:
                trv = False

        if am[per - 1][1] == iw:
            print("Вы перевели правильно!!!")
            ##            print("Вы перевели правильно, перевод:", w[0])
            if owords[iw][0] > -3:
                owords[iw][0] -= 2
            ochki += 1
        else:
            print("Вы перевели не правильно, перевод:", w[0])

            if owords[iw][0] < 5:
                owords[iw][0] += 3
        print()
    return ochki


modul = 1
modInos = {modul: ""}
# while True:


# print(modul)
oslword = {}
while True:
    words = False
    while words == False:
        m = moduls()
        modul = "moduls/" + m + ".txt"
        words = openfile(namef=modul)
    for st in words:
        print(st[0], ":", *st[1:])
    if m in oslword:
        owords = oslword[m]
    else:
        owords = [[0, word] for word in words]
        oslword[m] = owords
    # print(oslword)
    l = len(words)
    # print(l)
    print()
    print()

    ##    tip = int(input("Введите тип: 1 - eng-rus, 2 - rus-eng :"))
    tip = 2

    kolviv = int(l * 1.5)

    if tip == 1:
        ochki = engrus1(words, owords, kolviv)
    elif tip == 2:
        ochki = ruseng2(words, kolviv)
    if kolviv > 0:
        print("Ваша оценка:", str(3 / kolviv * (ochki) + 2)[:4])
    else:
        print("СЛОВ НЕ БЫЛО")
