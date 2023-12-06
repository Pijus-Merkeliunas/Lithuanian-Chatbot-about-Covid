import spacy


class Variables(object):
    class __Variables:
        def __init__(self):
            self.questions = []
            self.unique_words = []
            self.soundex_codes = {}
            self.regex_patterns = {}
            self.nlp = spacy.load("lt_core_news_md")
            self.typo = True
            self.debug = False
            self.debug_typo = False
            self.synonyms = True
            self.theme = 2 # 1 vu, 2 covid
            self.multi_typo = True
            self.searchType = 3 # 0 basic, 1 with ratio, 2 with +1/+2 ratio, 3 with rating
            self.typo_select = 0 # 0 basic, 1 soundex
            self.tf_idf = False
            self.rating = False
            self.debugTypoTimes = False
            self.searchThreshold = True

    instance = None

    def __new__(cls):
        if not Variables.instance:
            Variables.instance = Variables.__Variables()
        return Variables.instance
