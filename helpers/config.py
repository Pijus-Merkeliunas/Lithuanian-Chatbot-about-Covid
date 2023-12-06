from src.database import *

def check_for_config(inp):

    if inp == "!pagalba":
        print("\nChatbot-19:")
        print("!klaidos - išjungia / įjungia klaidų taisymą")
        print("!išjungti - išjungia progrmą")
        print("!k arba !kitas - grąžiną kitą populiariausią atsakymą, jei egzistuoja (daugiausiai gali būti 2 papildomi atsakymai)")
        print('!debug - įjungia / išjungia "debug" rėžimą, kuris yra skirtas programos kurimui arba tobulinimui')
        print('!debug typo - įjungia / išjungia klaidų taisymų "debug" rėžimą')
        print('!debug typo time - įjungia / išjungia klaidų taisymų "debug" funkciją, kuri skaičiuoja kiek laiko dirbo typo algoritmas')
        print("!tf-idf - įjungia / išjungia tf-idf algoritmą, kuris pridedą papildomų raktažodžių ieškodamas atsakymų")
        print("!sinonimai - įjungia / išjungia sinonimus kai yra ieškoma atsakymų")
        print("!reitingas - išjungia / įjungia reitingo parodymą (reitingas yra nuo 0 iki 1.00 (1.00 yra geriausias rezultatas), jeigu 3 (su reitingu) ieškojimo rėžimas tai rezultatas neturi limito ir kuo didesnis, tuo geresnis)")
        print("!ieškojimo būdas - įvedus šitą komandą yra pakeičiamas ieškojimo būdas, paskui reikia įvesti skaičių nuo 0 iki 2 rėžimai yra\n"
              "     0 - Paprasčiausias rėžimas, kuris išrenka atsakymus tuos, kurie turi daugiausiai sutampančių raktažodžių\n"
              "     1 - Santykinis rėžimas, kuris išrenka atsakymus pagal santykį (santykis yra: rasti raktažodžiai / kiek raktažodžių yra to atsakymo klausime)\n"
              "     2 - Binominis santykinis rėžimas, kuris išrenka atsakymus pagal santykį (santykis yra: rasti raktažodžiai + 1 / kiek raktažodžių yra to atsakymo klausime + 2). Rekomenduojamas rėžimas")
        print("!klaidų keitimas - įvedus šitą komandą yra pakeičiamas klaidų taisymo būdas, paskui reikia įvesti skaičių nuo 0 iki 1 rėžimai yra:\n "
              "    0 - Vienos raidės pakeitimo rėžimas, kuris bando pakeistis angliškas raides, kaip a,c,e... į jų lietuviškas atitkmenis ą,č,ę,ė... arba įdėda / įšima raidę ir taip taiso žodį,\n pvz tranportas ištaisys į transportas. Rekomenduojamas rėžimas.\n"
              '     1 - Soundex rėžimas, kuris naudodają algoritmą pavadinimu "soundex" ir bando ištaisyti klaidas pagal žodžio tarimą')
        print("!minimumas - įjungia / išjungia reitingo minimumo reikalavimą")
        print("!keisti tema - Įvedus šią komandą reikia paskui pasirinkti temą į kuria nori pakeisti (vu/covid). Duomenų bazei reikės persikrauti tai gali užtrukti kelias sekundes, baigus perkrovimui bus pranešamą")

    elif inp == "!klaidos":
        Variables().typo = not Variables().typo
        if Variables().typo:
            print("\nChatbot-19: klaidų taisymas įjungtas")
        else:
            print("\nChatbot-19: klaidų taisymas išjungtas")

    elif inp == "!išjungti":
        exit()

    elif inp == "!minimumas":
        Variables().searchThreshold = not Variables().debug
        if Variables().searchThreshold:
            print("\nChatbot-19: threshold įjungtas")
        else:
            print("\nChatbot-19: threshold išjungtas")

    elif inp == "!debug":
        Variables().debug = not Variables().debug
        if Variables().debug:
            print("\nChatbot-19: debug įjungtas")
        else:
            print("\nChatbot-19: debug išjungtas")

    elif inp == "!debug typo":
        Variables().debug_typo = not Variables().debug_typo
        if Variables().debug_typo:
            print("\nChatbot-19: debug typo įjungtas")
        else:
            print("\nChatbot-19: debug typo išjungtas")

    elif inp == "!debug typo time":
        Variables().debugTypoTimes = not Variables().debugTypoTimes
        if Variables().debugTypoTimes:
            print("\nChatbot-19: debug typo laikas įjungtas")
        else:
            print("\nChatbot-19: debug typo laikas išjungtas")

    elif inp == "!tf-idf":
        Variables().debug_typo = not Variables().debug_typo
        if Variables().debug_typo:
            print("\nChatbot-19: tf-idf įjungtas")
        else:
            print("\nChatbot-19: tf-idf išjungtas")
    elif inp == "!sinonimai":
        Variables().synonyms = not Variables().synonyms
        if Variables().synonyms:
            print("\nChatbot-19: sinonimai įjungti")
        else:
            print("\nChatbot-19: sinonimai išjungti")
    elif inp == "!reitingas":
        Variables().rating = not Variables().rating
        if Variables().rating:
            print("\nChatbot-19: reitingas įjungtas")
        else:
            print("\nChatbot-19: reitingas išjungtas")
    elif inp == "!ieškojimo būdas":
        print("\nChatbot-19: įveskite kokį ieškojimo rėžimą norite įjungti (0-3), gali reikalauti duomenų bazės perkrovimo, kuri padarys automatiškai, bet užtruks kelias sekundes")
        print("\nJūs: ", end='')
        x = input()
        try:
            x = int(x)

            if x == 1:
                if Variables().searchType == 3:
                    Variables().searchType = x
                    Variables().questions = []
                    connect_to_database(None)
                    print(
                        "\nChatbot-19: ieškojimas pagal sutampančių raktažodžių santykį įjungtas")
                else:
                    Variables().searchType = x
                    print(
                        "\nChatbot-19: ieškojimas pagal sutampančių raktažodžių santykį įjungtas")
            elif x == 2:
                if Variables().searchType == 3:
                    Variables().searchType = x
                    Variables().questions = []
                    connect_to_database(None)
                else:
                    Variables().searchType = x
                    print(
                        "\nChatbot-19: ieškojimas pagal sutampančių raktažodžių santykį paremtas su binominia distrubucija įjungtas")
            elif x == 3:
                Variables().searchType = x
                Variables().questions = []
                connect_to_database(None)
                print("\nChatbot-19: ieškojimas pagal reitinga įjungtas")
            else:
                if Variables().searchType == 3:
                    Variables().searchType = 0
                    Variables().questions = []
                    connect_to_database(None)
                else:
                    Variables().searchType = 0
                    print(
                        "\nChatbot-19: ieškojimas pagal sutampačius raktažodžius įjungtas")
        except:
            print("\nChatbot-19: prašome įvesti skaičių (0-2)")
    elif inp == "!klaidų keitimas":
        print("\nChatbot-19: įveskite kokį ieškojimo rėžimą norit (0-1)")
        print("\nJūs: ", end='')
        x = input()
        try:
            x = int(x)
            Variables().searchType = x
            if x == 1:
                Variables().searchType = x
                print('\nChatbot-19: ieškojimas su "soundex" įjungtas')
            else:
                print("\nChatbot-19: ieškojimas pakeitus 1 raidė įjungtas")
        except:
            print("\nChatbot-19: prašome įvesti skaičių (0-1)")

    elif inp == "!keisti tema":
        print("\nChatbot-19: įveskite į kokią temą norite pakeisti (vu/covid)")
        print("\nJūs: ", end='')
        x = input().lower()
        if x == "vu":
            Variables().theme = 1
            Variables().questions = []
            connect_to_database(None)
            print('\nChatbot-19: tema "Vilniaus Universitetas" parinkta')

        elif x == "covid":
            Variables().theme = 2
            Variables().questions = []
            connect_to_database(None)
            print('\nChatbot-19: tema "Covid-19" parinkta')

        else:
            print("\nChatbot-19: prašau iš naujo bandyti įvesti temą")

    else:
        print("\nChatbot-19: Komanda nerasta")
