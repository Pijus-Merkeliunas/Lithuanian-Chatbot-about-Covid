from src.singleton_variables import Variables

def soundex(name):
    soundexcoding = [' ', ' ', ' ', ' ']
    soundexcodingindex = 1

    #           ABCDEFGHIJKLMNOPQRSTUVWXYZ
    mappings = "01230120022455012623010202" # Vertės priskirtos raidėms pagal jų tarimą.

    soundexcoding[0] = name[0].upper()

    for i in range(1, len(name)):  # generuoja kombinacija pagal kurią galima lyginti žodžių panašumą

         c = ord(name[i].upper()) - 65

         if c >= 0 and c <= 25:

             if mappings[c] != '0':

                 if mappings[c] != soundexcoding[soundexcodingindex-1]:

                     soundexcoding[soundexcodingindex] = mappings[c]
                     soundexcodingindex += 1

                 if soundexcodingindex > 3:

                     break

    if soundexcodingindex <= 3:
        while(soundexcodingindex <= 3):
            soundexcoding[soundexcodingindex] = '0'
            soundexcodingindex += 1

    return ''.join(soundexcoding)

def get_soundex_codes():
    lt_letters = {
        "ą": 'a',
        'č': 'c',
        'ę': 'e',
        'ė': 'e',
        'į': 'i',
        'š': 's',
        'ų': 'u',
        'ū': 'u',
        'ž': 'z'
    }

    codes = {}
    for word in Variables().unique_words:
        if word[0] in lt_letters.keys():
            word = lt_letters[word[0]] + word[1:]
        codes[soundex(word)] = word
    Variables().soundex_codes = codes

def typos_with_soundex(keywords, incorrect_word, keywords_to_check): # Taiso klaidas žodžiuose ieškodamas panašiai skambančių žodžių esančių mūsų duombazėje
    word_soundex = soundex(incorrect_word)
    corrected = []

    for key, value in keywords_to_check.items():
        if key == word_soundex:
            corrected.append(value)
            keywords.append(value)

    return corrected
