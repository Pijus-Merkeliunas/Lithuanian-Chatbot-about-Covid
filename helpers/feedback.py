import re

def not_spam(question):
    regex = "^[a-ząčęėįšųūž]{2,} [a-ząčęėįšųūž]{2,}"
    repeating = r"\b(\w+)(?:[\s+]\1(?=[ ]|$)){1}"
    if not re.search(regex, question) or re.search(repeating, question):
        return False

    return True
