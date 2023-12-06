import configparser
import sshtunnel
import psycopg2
import requests
import bs4
import re
from src.helpers.question import Question
from src.helpers.soundex import *


def web_scrap_answer(html, link, position, answer):
    result = requests.get(link)                         # Gauna informaciją apie puslapį ir informacijos vietą ir ją nuskaito
    soup = bs4.BeautifulSoup(result.text, "lxml")
    new_answer = answer.format(soup.select(html)[position].getText())
    return new_answer


def add_unique_word(word):
    if word not in Variables().unique_words:            # Patikrina ar žodis nėra raktažodžiuose
        Variables().unique_words.append(word)


def add_question(question, answer):
    existing = False
    for obj in Variables().questions:
        if obj.question == question:
            obj.add_answer(answer)
            existing = True

    if not existing:                                    # Priskiria kalbos dalims reitingavimo taškus
        q = Question(question.lower(), answer)
        keywords = dict()
        doc_q = Variables().nlp(question)
        for chunk in doc_q:
            if chunk.lemma_ == "liga" or chunk.lemma_ == "korona":
                string = chunk.lemma_
                keywords[string.lower()] = 1.3
            elif chunk.text == "pirmasis":
                string = chunk.text
                keywords[string.lower()] = 2
                add_unique_word(chunk.text)
            elif chunk.pos_ == "NOUN" or chunk.pos_ == "VERB":
                string = chunk.lemma_
                keywords[string.lower()] = 1.5
                add_unique_word(chunk.lemma_)
            elif chunk.pos_ == "PROPN":
                string = chunk.lemma_
                keywords[string.lower()] = 2
                add_unique_word(chunk.lemma_)
            elif chunk.pos_ == "PRON":
                string = chunk.lemma_
                keywords[string.lower()] = 1.8
                add_unique_word(chunk.lemma_)
            elif re.search("\W", chunk.text) is None and Variables().searchType == 3:
                string = chunk.lemma_
                keywords[string.lower()] = 1
                add_unique_word(chunk.lemma_)
        q.set_keywords(keywords)
        Variables().questions.append(q)


def read_database(data):
    cur = data.cursor()
    cur.execute(
        "SELECT question, answer FROM question, answer, answer_question where questionType = 0 AND questionId=qstId AND "
        "answerId=ansId AND (themeId={} OR themeId = 3);".format(Variables().theme))
    for row in cur:
        add_question(row[0], row[1])                    # Prideda kievieną klausimą iš duombazės su parinkta tema į darbinę atmintį

    cur.execute(
        "SELECT question, answer, link, html, position FROM question,answer,answer_question,source where questionType = 1 AND sourceQstId = questionId AND questionId=qstId AND "
        "answerId=ansId AND (themeId={} OR themeId = 3);".format(Variables().theme))
    for row in cur:                                     # Prideda dinaminius klausimus(kurie renka informaciją iš puslapių) iš duombazės ir ideda į darbinę atmintį
        add_question(row[0], web_scrap_answer(row[2], row[3], row[4], row[1]))

    cur.execute(
        "SELECT pattern, word FROM regex".format(Variables().theme))
    for row in cur:                                    # Prideda regex šablonus pagal kuriuos idetifikuojame žodžius kurių neatpažįsta spaCy
        Variables().regex_patterns[row[0]] = row[1]

    cur.close()


def connect_to_database(write=None, testing=False):
    config = configparser.ConfigParser()
    try:
        if (testing):
            config.read('..\..\config\dbconfig.txt')    # Nuskaito konfiguracinį failą
        else:
            config.read('config\dbconfig.txt')
        dbconfig = config['DATABASE']

        try:
            sshtunnel.SSH_TIMEOUT = 5.0
            sshtunnel.TUNNEL_TIMEOUT = 5.0
            with sshtunnel.SSHTunnelForwarder(          # Su informacija apie virtualią mašina iš konfiguracinio failo prisijungiame prie virtualios mašinos su ssh tuneliu
                    (dbconfig["IP"], int(dbconfig["Port"])),
                    ssh_username=dbconfig["User"], ssh_password=dbconfig["SERVER_PASSWORD"],
                    remote_bind_address=('localhost', 5432),
                    local_bind_address=('localhost', 9954)
            ) as server:
                server.start()                          # Priskiriame "params" kintamajam duombazės informaciją
                params = {
                    'database': dbconfig["DB_NAME"],
                    'user': dbconfig["User"],
                    'password': dbconfig["DB_PASSWORD"],
                    'host': 'localhost',
                    'port': 9954
                }
                conn = psycopg2.connect(**params)       # Su iš konfiguracinio failo surinkta informacija prisijungiame prie duomenų bazės virtualioje mašinoje
                cur = conn.cursor()
                if write is None:
                    read_database(conn)                 # Paleidžiame funkciją kuri nuskaito duombazę
                    get_soundex_codes()
                elif write[1] != 0:                     # Kai duombazė paleista visus užduotus klausimus į ją įrašome

                    cur.execute(
                        "INSERT INTO user_questions(date, input, rating, themeid) VALUES(current_timestamp,'{}',{},{});".format(
                            write[0], write[1], Variables().theme))

                    choiceNum = 1
                    for key, value in write[2].items(): # Jei į klausimą buvo atsakyta suranda jį ir ir įrašo jo id
                        cur.execute(
                            "select questionId, questionType from question where question like '{}';".format(key))
                        for row in cur:
                            qstid = row[0]
                            qstType = row[1]

                        if qstType == 1:
                            cur.execute(
                                "select ansId from answer_question where qstId = {}".format(qstid))
                        else:
                            cur.execute(
                                "select answerId from answer where answer like '{}';".format(value[1][0]))
                        for row in cur:
                            ansid = row[0]

                        cur.execute("select MAX(questionNo) from user_questions;")
                        for row in cur:
                            questionNo = row[0]

                        cur.execute("INSERT INTO choice VALUES({}, {}, {}, {});".format(
                            choiceNum, questionNo, qstid, ansid))
                        keywordNum = 1

                        for key in value[2]:
                            cur.execute("INSERT INTO keywords VALUES('{}', {}, {}, {});".format(
                                key, choiceNum, keywordNum, questionNo))
                            keywordNum += 1
                        choiceNum += 1
                    cur.execute(                        # Jei klausimas nebuvo rastas įrašo be jo
                        "select rating from user_questions where questionno={};".format(questionNo))
                    rating = cur.fetchone()
                    cur.execute("select qstid from choice where choiceNo = {} and qstno = {};".format(
                        rating[0], questionNo))
                    questionId = cur.fetchone()
                    cur.execute(
                        "select frequency from question where questionid={};".format(questionId[0]))
                    frequency = cur.fetchone()
                    cur.execute("update question set frequency={} where questionid = {}".format(
                        frequency[0] + 1, questionId[0]))
                    conn.commit()
                else:
                    cur.execute(
                        "INSERT INTO user_questions(date, input, rating, themeid) VALUES(current_timestamp,'{}',{},{});".format(
                            write[0], write[1], Variables().theme))  # 0-question 2-rating  3-atsakymas 4-keyword
                    conn.commit()
                conn.close()
                server.close()
        except:
            print(
                "Chatbot-19: Nepavyko prisijungti prie duomenų bazės, prašome įstikinti ar yra veikiantis interneto rišys.\n")
    except:
        print('Chatbot-19: Prašome pridėti konfiguracinį failą mano "config" direktorijoj')
