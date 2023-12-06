import threading
import time
from src.answer import look_for_answer
from src.database import connect_to_database
from src.singleton_variables import Variables
from src.helpers.feedback import not_spam
from src.helpers.config import check_for_config

thread_database = threading.Thread(target=connect_to_database)   # Sukurią threadą duombazės nuskaitymui
thread_database.start()                                          # Pradeda duombazės prijungimą atskirai nuo pagrindinio programos veikimo

print("Jei norite pamatyti papildomas funkcijas rašykite !pagalba")
active = True
previous_input = None
previous_question = None
previous_answer = None
previous_answer_rating = 0
previous_keywords = None


while active:
    answer_start_number = 1
    print('\nJūs: ', end='')
    inp = input().lower()
    thread_database.join()        # Vartotojui įvedus klausimą sulaukia kol įkels duombazę
    if inp == "!k" or inp == "!kitas":
        if previous_answer is None:                                        # Jei prieš tai nebuvo užduotas klausimas arba į jį neturėjo atsakymo
            print('\nChatbot-19: Jūs dar neuždavėte klausimo.')
        elif len(previous_answer) <= 1:                                    # Jei turėjo tik vieną atsakymą
            print('\nChatbot-19: Atsiprašome, kito atsakymo neturime...')
            previous_answer_rating += 1
        else:                                                              # Jei turi daugiau atsakymų
            for nr in range(answer_start_number, len(answers)):
                previous_answer_rating += 1
                for i, answer in enumerate(list(answers.values())[nr][1]):
                    print("\nChatbot-19:", answer)
                    if i + 1 < len(list(answers.values())[0][1]):
                        time.sleep(3)
                if Variables().rating:
                    print("\nChatbot-19: Reitingas:",
                          list(answers.values())[0][nr])
                if nr < len(answers):
                    print('\nChatbot-19: Ar jus tenkina gautas atsakymas? (T/N)')
                    print('\nJūs: ', end='')
                    ats = input().lower()
                    if ats == 't' or ats == '!t' or ats == 'taip':
                        break
                    else:
                        if nr == len(answers)-1:
                            print('\nChatbot-19: Atsiprašome, kito atsakymo neturime...')
                            previous_answer_rating = 0

    elif inp.startswith('!'):       # Jei naudojama kažkuri iš pagalbinių funkcijų
        check_for_config(inp)
    else:
        thread_feedback = None
        if previous_input and previous_answer_rating != 0 and previous_input != inp:  # Jei rado atsakymą į klausimą
            thread_feedback = threading.Thread(target=connect_to_database, args=(     # Sukuria atskira threadą jo įkėlimui į duombazę
                [previous_input, previous_answer_rating, previous_answer],))
            thread_feedback.start()
        elif previous_input and previous_answer_rating == 0 and not_spam(previous_input) and previous_input != inp:  # Jei atsakymo nerado ir klausimas nebuvom spam'as
            thread_feedback = threading.Thread(target=connect_to_database, args=(                                    # Įkelią klausima į duombazę be grąžinto atsakymo
                [previous_input, previous_answer_rating],))
            thread_feedback.start()

        answers = look_for_answer(inp)  # Ieško atsakymo į klausimą
        previous_answer = answers
        previous_answer_rating = 0
        if len(answers) > 0:     # Jei randa atsakymą
            previous_question = list(answers.keys())[0]
            previous_input = inp
            previous_keywords = ' '.join(word for word in list(answers.values())[0][2])
            previous_answer_rating += 1
            if Variables().searchThreshold:                # Jei įjungtas chatbot'as neišmeta atsakymo jei jis netenkina minimalių sutampamumo kriterijų
                if Variables().searchType != 3 and list(answers.values())[0][0] > 0.3:    # Jei sutampa mažiau nei 30% raktažodžių
                    if Variables().searchType == 2:
                        list(answers.values())[0][0] += 0.1
                    for i, answer in enumerate(list(answers.values())[0][1]):
                        print("\nChatbot-19:", answer)
                        if i+1 < len(list(answers.values())[0][1]):
                            time.sleep(3)
                elif Variables().searchType == 3 and list(answers.values())[0][0] >= 1.5:   # Jei sutampančių raktažodžių vertė nesiekia 1,5
                    for i, answer in enumerate(list(answers.values())[0][1]):
                        print("\nChatbot-19:", answer)
                        if i+1 < len(list(answers.values())[0][1]):
                            time.sleep(3)
                else:
                    print('\nChatbot-19: Atsiprašau, nežinau atsakymo į jūsų užduotą klausimą.')
                    answer_start_number -= 1
            else:
                for i, answer in enumerate(list(answers.values())[0][1]):
                    print("\nChatbot-19:", answer)
                    if i + 1 < len(list(answers.values())[0][1]):  # Jei atsakymas į klausimą susideda iš kelių dalių kurios išspausdinamos atskirai
                        time.sleep(3)
            if Variables().rating:
                print("\nChatbot-19: Reitingas:", list(answers.values())[0][0])

        else:
            previous_question = ' '
            previous_input = inp
            previous_keywords = ' '
            previous_answer = []
            print('\nChatbot-19: Atsiprašau, nežinau atsakymo į jūsų užduotą klausimą.')