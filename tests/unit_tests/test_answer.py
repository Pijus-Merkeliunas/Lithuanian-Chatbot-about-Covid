import unittest
import src.answer as answer
import src.helpers.search_patterns as search_patterns
from src.helpers.soundex import soundex


class test_answer(unittest.TestCase):

    def test_synonyms(self):
        # Arrange
        testsmap = {
            'ragana': ['Žiežula', 'Žiežmara', 'Šatrija', 'Vydraga', 'Furija'],
            'mirtis': ['Myris', 'Mirtinoji', 'Paskutinioji',
                       'Pastaroji', 'Baigtis', 'Galas', 'Galinė', 'Giltinė'],
            'siandien': ['Šiandieną', 'Nūdien'],
            'baf': [],
            'ne': []
        }

        # Assert
        for word, synonyms in testsmap.items():
            self.assertEqual(synonyms, answer.synonyms(word))

    """
        def test_check_for_typos(self):
            # Arrange
            test_keywords = ['automobilis', 'transportas', 'mašina', 'virusas', 'žmogus']
            testsmap = {
                'automobils' : ['automobilis'],
                'ransportas' : ['transportas'],
                'masina' : ['mašina'],
                'virusaz' : ['virusas'],
                'žmogus' : ['žmogus'],
                'marka' : []
            }

            # Assert
            for word, correct in testsmap.items():
                result = answer.check_for_typos([], word, test_keywords)
                self.assertEqual(correct, result)
    """

    def test_typos_with_soundex(self):
        # Arrange
        dictionary_with_soundex_codes = {}
        test_keywords = ['automobilis', 'transportas',
                         'mašina', 'virusas', 'žmogus']
        testsmap = {
            'automobils': ['automobilis'],
            'trnsportas': ['transportas'],
            'mašin': ['mašina'],
            'virusaz': ['virusas'],
            'žmogus': ['žmogus'],
            'morka': []
        }

        # Act
        for word in test_keywords:
            dictionary_with_soundex_codes[soundex(word)] = word

        # Assert
        for word, correct in testsmap.items():
            result = answer.typos_with_soundex(
                [], word, dictionary_with_soundex_codes)
            self.assertEqual(correct, result)

    def test_insert_all_lithuanian(self):
        # Arrange
        test_keywords = ['dėvėtas', 'žiežirba', 'ąžuolas', 'užšoko']
        testsmap = {
            'devetas': ['dėvėtas'],
            'ziezirba': ['žiežirba'],
            'azuolas': ['ąžuolas'],
            'uzsoko': ['užšoko']
        }

        # Assert
        for word, correct in testsmap.items():
            result = answer.insert_all_lithuanian(word, test_keywords)
            self.assertEqual(correct, result)


if __name__ == '__main__':
    unittest.main()
