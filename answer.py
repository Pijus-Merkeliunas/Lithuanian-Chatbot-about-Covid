import requests
import bs4
import math
import re
import time
from threading import Thread
from queue import Queue
from src.helpers.search_patterns import decompose
from src.helpers.soundex import *


def check_for_specific_word_patterns(word): # Iš duomenų bazės paima regex šablonus ir pagal juos taiso specialius žodžius (kurie "spaCy" bibliotekos nėra atpažinti) kaip "korona"
    for key, value in Variables().regex_patterns.items():
        if re.search(key, word):
            return value



def synonyms(word): # Iš svetainės paima visus duoto žodžio sinonimus
    cap = word.capitalize()
    result = requests.get(
        "https://www.lietuviuzodynas.lt/sinonimai/{}".format(cap))
    soup = bs4.BeautifulSoup(result.text, "lxml")
    try:
        synonym = (soup.select('#main-box div.box-content')
                   [0].next_element.strip())
    except IndexError:
        synonym = 'Nieko nerasta.'

    fixed_list = []
    if synonym != 'Nieko nerasta.':
        synonym_list = synonym.split(', ')
        for s in synonym_list:
            fixed_list.append(s)

    return fixed_list

def check_for_typos(incorrect_word):

    if (Variables().debugTypoTimes):
        print("\nTypos funkcijos veikimo laikas žodžiui {}:\n".format(incorrect_word))
        start = time.perf_counter()

    corrected = []
    adjusted_question_keywords = []

    if len(incorrect_word) < 2: # Netaiso žodžių kurie turi mažiau nei dvi raides
        return corrected

    for keyword in Variables().unique_words:                # Randa raktažodžius iš duomenų bazės, kurių ilgis skiriasi nuo taisomo žodžio viena raide ir dirbą su jais
        if abs(len(keyword) - len(incorrect_word)) <= 1:
            adjusted_question_keywords.append(keyword)
    if len(adjusted_question_keywords) > 0:
        word_with_lt_letters = insert_all_lithuanian(
            incorrect_word, Variables().unique_words)
        for word in word_with_lt_letters:
            corrected.append(word)

        if len(word_with_lt_letters) == 0:
            lt_abc = ["a", "ą", "b", "c", "č", "d", "e", "ę", "ė", "f", "g", "h", "i", "į", "y", "j", "k", "l", "m",
                      "n", "o", "p", "r", "s", "š", "t", "u", "ų", "ū", "v", "z", "ž", ""]
            current_letter = 0
            while current_letter < len(incorrect_word) + 1: # +1 raidė, kad pridėti raidę ir žodžio gale
                t = 0
                while t < len(lt_abc):
                    doc_a = Variables().nlp(                # Iš taisomo žodžio yra pakeičiama raidė ir pridėdama raidė (pvz. jeigu taiso žodį "dėvėtas" pirmame ciklo rate bus ądėvėtas ir ąvėtas)
                        incorrect_word[:current_letter] + lt_abc[t] + incorrect_word[current_letter:] + " " +
                        incorrect_word[:current_letter] + lt_abc[t] + incorrect_word[current_letter + 1:])
                    for word in doc_a:
                        for keyword in adjusted_question_keywords:   # Tikrina ar yra toks pataisytas žodis duomenų bazėje
                            if Variables().debug_typo:
                                print(word.lemma_, " == ", keyword)
                            if word.lemma_ == keyword and word.lemma_ not in corrected:
                                corrected.append(word.lemma_)
                            if word.text == keyword and word.text not in corrected:
                                corrected.append(word.text)
                    t += 1
                current_letter += 1

        if (Variables().debugTypoTimes):
            finish = time.perf_counter()
            print(round((finish - start), 5))
            print("\nIštaisytas į žodį: {}".format(corrected))
        return corrected


def insert_all_lithuanian(word, keywords_to_check): # Ištaiso žodžius kuriuose reikia pakeisti raides į jų lietuviškus atitikmenis (pvz. "devetas" į "dėvėtas")
    lt_letters = {
        "a": 'ą',
        'c': 'č',
        'e': 'ę',
        'i': 'į',
        's': 'š',
        'u': 'ų',
        'z': 'ž'
    }

    e_u = {
        'e': 'ė',
        'u': 'ū'
    }

    words = [word]
    for i in range(len(word)):
        if len(words) < 12 * 12 * 12: # Gali viename žodyje ištaisyti 11 klaidų jei raidės turi du variantus (pvz a, ą), 7 jei tris (pvz e ę ė)
            if word[i] in lt_letters:
                if word[i] in e_u:
                    for j in range(len(words)):
                        words.append(words[j][:i] + e_u[word[i]] + words[j][i + 1:])
                for j in range(len(words)):
                    if words[j][i] != 'ė' and words[j][i] != 'ū' and words[j][i] not in words:
                        words.append(
                            words[j][:i] + lt_letters[word[i]] + words[j][i + 1:])

    checked_with_keywords = []
    for corrected_word in words:     # Patikrina taisomą žodį su raktažodžiais iš duomenų bazės
        if corrected_word in keywords_to_check:
            checked_with_keywords.append(corrected_word)

    return checked_with_keywords

def computeTF(wordDict, bagOfWords):
    tfDict = {}
    bagOfWordsCount = len(bagOfWords)
    for word, count in wordDict.items():
        tfDict[word] = count / float(bagOfWordsCount)
    return tfDict

def computeIDF(documents):
    N = len(documents)

    idfDict = dict.fromkeys(documents[0].keys(), 0)

    for document in documents:
        for word, val in document.items():
            if val > 0:
                idfDict[word] += 1

    for word, val in idfDict.items():
        idfDict[word] = math.log(N / float(val))

    return idfDict


def computeTFIDF(tfBagOfWords, idfs):
    tfidf = {}
    for word, val in tfBagOfWords.items():
        tfidf[word] = val * idfs[word]

    return tfidf


def tf_idf(keywords, questions): # Prilygina duodamus raktažodžius su raktažodžias esančiais duomenų bazėje ir bando rasti panašius, juos įdėda į raktažodžius
    keywords = set(keywords)
    all_question_keywords = []
    keys = []
    for question in questions:
        all_question_keywords = all_question_keywords + question.keywords
    both_keywords = keywords.union(set(all_question_keywords))

    numOfWordsA = dict.fromkeys(both_keywords, 0)
    for word in keywords:
        numOfWordsA[word] += 1

    numOfWordsB = dict.fromkeys(both_keywords, 0)
    for word in all_question_keywords:
        numOfWordsB[word] += 1

    tfb = computeTF(numOfWordsB, all_question_keywords)

    idfs = computeIDF([numOfWordsA, numOfWordsB])

    tfidfB = computeTFIDF(tfb, idfs)

    for key, value in tfidfB.items():
        if value <= 0.004: # 0.004 yra riba, ir jei žodžiai ją viršija, jie yra įdedami į raktažodžius
            keys.append(key)
    return keys

def ThreadingForTypo(keywords, q): # Leidžia padaryti, kad veiktų keli check_for_typos algoritmai vienu metu
    while True:
        incorrect_word = q.get()
        result = check_for_typos(incorrect_word)
        if type(result) == list:
            for word in result:
                keywords.append(word)
        q.task_done()


def look_for_answer(users_input):
    q = Queue()
    three_answers = dict()
    loop = 0
    questions = Variables().questions
    users_input = decompose(users_input)
    current_answer = []
    for question in questions:                    # Patikrina ar vartotojo užduotas klausimas yra identiškas klausimui duomenų bazėje
        if question.question == users_input:
            loop = loop + 1
            if Variables().searchType != 3:
                three_answers.update({question.question: [1, question.answer, "All words matched"]}) # Jeigu toks pats reitingas yra nustatomas kaip 1
            else:
                three_answers.update({question.question: [100, question.answer, "All words matched"]}) # Kadangi 4 searchType naudoja kitą reitingų sistemą todėl jam yra nustatomas 100
            current_answer.append(question.answer)
            if Variables().debug:
                print("Keywords: ", "All words matched")
                print("Full question: ", question.question)
                print("Question keywords: ", question.keywords)
                print("Matching keywords: ", 1)
                print()
            break
           
    keywords = []
    nlp = Variables().nlp
    unique_words = set(users_input.split())

    if len(unique_words) > 1:
        doc_q = nlp(" ".join(unique_words))
    else:
        doc_q = nlp("".join(unique_words))

    for chunk in doc_q:
        changed = check_for_specific_word_patterns(chunk.text)
        if changed:
            keywords.append(changed)

        if Variables().synonyms:
            if chunk.lemma_ != "korona":                    # Netikrinam koronos, nes tą daro check_for_specific_words
                for synonym in synonyms(chunk.lemma_):
                    keywords.append(synonym.lower())
                keywords.append(chunk.lemma_)

        if not Variables().multi_typo and Variables().typo and Variables().typo_select == 0: # Šito reikia jei vartotojas nori naudoti "typo" be "threading"
            for corrected_words in check_for_typos(chunk.text):
                keywords.append(corrected_words)

        if Variables().typo and Variables().typo_select == 1:
            typos_with_soundex(keywords, chunk.text, Variables().soundex_codes)

    if Variables().multi_typo:
        for i in range(5):                                                   # Maksimalus vienu metu paleistų "typo" algoritmų skaičius 5
            t = Thread(target=ThreadingForTypo, args=(keywords, q,))
            t.daemon = True
            t.start()

        for word in [chunk.text for chunk in doc_q]:
            q.put(word)
        q.join()

    if Variables().tf_idf:
        keywords = tf_idf(keywords, questions)
    keywords = set(keywords)
    question_with_most_similarities = dict()

    for question in questions: # Šitas ciklas susumuoja rastus vartotojo raktažodžius klausime, jei pasirinktas 4 ieškojimo būdas tai yra susumuojami taškai
        sum = 0
        matching_keywords = []
        for i in keywords:
            if i in question.keywords:
                matching_keywords.append(i)
                sum += question.keywords[i]
        matching_keywords_points = sum

        user_matching_keywords = len(matching_keywords)
        question_keywords = len(question.keywords)
        if user_matching_keywords > 0 and question.question not in three_answers.keys():
            question_with_most_similarities[question.question] = user_matching_keywords, question_keywords, matching_keywords, question.answer, matching_keywords_points

    if len(question_with_most_similarities) == 0: # Jei nėra jokių galimų atsakymų baigia ieškojimą
        return three_answers

    else:
        while loop < 3:
            max = 0
            max_quest = None
            rating = None
            question_temp = None
            keywords_temp = None
            for key, value in question_with_most_similarities.items():
                if value[3] not in current_answer:
                    if value[0] > max and Variables().searchType == 0: # Pirmas ieškojimo algoritmas, kuris randą klausimą turintį daugiausiai sutampančių raktažodžių
                        max = value[0]
                        max_quest = value[3]
                        rating = value[0] / value[1]
                        question_temp = key
                        keywords_temp = value[2]

                    elif value[0] / value[1] > max and Variables().searchType == 1: # Antras ieškojimo algoritmas, kuris randą geriausia rastų raktažodžių / visų klausimų raktažodžių santykį
                        max = value[0] / value[1]
                        absolute_max = value[1]
                        max_quest = value[3]
                        rating = max
                        question_temp = key
                        keywords_temp = value[2]
                    elif value[0] / value[1] == max and value[1] > absolute_max and Variables().searchType == 1: # jeigu yra du tokie patys santykiai duoda prioritetą tam, kurio klausimas esantis duomenų bazėje turi daugiau raktažodžių
                        max = value[0] / value[1]
                        absolute_max = value[1]
                        max_quest = value[3]
                        rating = max
                        question_temp = key
                        keywords_temp = value[2]

                    elif (value[0] + 1) / (value[1] + 2) > max and value[0] != 0 and Variables().searchType == 2: # Trečias ieškojimo algoritmas, kuris pagal šitą santykį - rasti raktažodžiai + 1 / visi klausimo raktažodžiai + 2, randą geriausia atsakymą
                        max = (value[0] + 1) / (value[1] + 2)
                        max_quest = value[3]
                        rating = max
                        absolute_max = value[1]
                        question_temp = key
                        keywords_temp = value[2]
                    elif (value[0] + 1) / (value[1] + 2) == max and value[1] > absolute_max and Variables().searchType == 2: # tas pats kaip ir antram ieškojimo būde
                        max = (value[0] + 1) / (value[1] + 2)
                        absolute_max = value[1]
                        max_quest = value[3]
                        rating = max
                        question_temp = key
                        keywords_temp = value[2]

                    elif value[4] > max and value[0] != 0 and Variables().searchType == 3: # Randa kurio atsakymo reitingas didžiausias
                        max = value[4]
                        max_quest = value[3]
                        rating = value[4]
                        absolute_max = value[1]
                        question_temp = key
                        keywords_temp = value[2]
                    elif value[4] == max and value[1] < absolute_max and Variables().searchType == 3: # jeigu yra du tokie patys santykiai duoda prioritetą tam, kurio klausimas esantis duomenų bazėje turi mažiau raktažodžių
                        max = value[4]
                        absolute_max = value[1]
                        max_quest = value[3]
                        rating = value[4]
                        question_temp = key
                        keywords_temp = value[2]

            if max > 0:
                three_answers.update({question_temp: [round(rating, 2), max_quest, keywords_temp]})
                current_answer.append(max_quest)
                del question_with_most_similarities[question_temp]
            else:
                break
            if Variables().debug:
                print("Keywords: ", keywords)
                for question in questions:
                    if question.answer == max_quest:
                        print("Full question: ", question.question)
                        print("Question keywords: ", question.keywords)
                        print("Matching keywords: ", max)
                        print()
            loop = loop + 1

        return three_answers