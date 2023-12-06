import re


def decompose(input):   # Jei įvestyje yra daugiau nei vienas sakinys - surandą pirma klausimą
    shortened_names = False
    if '.' in input and '?' in input:
        input = multiple_question_marks(input)
        contains_multiple_questions = False

        if input.count('?') > 1:
            contains_multiple_questions = True
            input = input.split('?')[0] + '?'
            print('Prašome vienu metu užduoti vieną klausimą.')
            print('Atsakome į šį Jūsų užduotą klausimą:')

        if re.search(' .\.', input):  # Atpažįsta jei įvestyje yra trumpinių (pvz G. Nausėda)
            shortened_names = True
        input = input.split('.')

        if shortened_names:                            # Jei yra trumpinių jų netraktuoja kaip atskirų sakinių
            for number, sentence in enumerate(input):
                if re.fullmatch(' .', sentence[-2:]):
                    try:
                        input[number + 1] = sentence + '.' + input[number + 1]
                    except IndexError:
                        continue

        for sentence in input:  # ieško sakinio su klaustuku
            if '?' in sentence:
                if sentence[0] == ' ':
                    sentence = sentence[1:]
                if contains_multiple_questions:
                    print(sentence + '\n')

                return sentence

    elif re.search('\?.+', input):
        print("Atsakome į šį klausimą: {}?".format(input.split('?')[0]))
        return input.split('?')[0] + '?'

    return input


def multiple_question_marks(input):  # Panaikina klaustukų perteklių sakinyje
    pattern = re.compile("\?[?]")

    if not re.search(pattern, input):
        return input

    new_input = ''
    stop = 0

    for match in re.finditer(pattern, input):
        it_start = match.start()

        if it_start < stop:
            continue

        new_input += input[stop:it_start + 1]

        for number, x in enumerate(input[it_start + 2:]):

            if x != '?':
                stop = it_start + number + 2
                break

            stop = it_start + number + 3

    new_input += input[stop:]

    return new_input
