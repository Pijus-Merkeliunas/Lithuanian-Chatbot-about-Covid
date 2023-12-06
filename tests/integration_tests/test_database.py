import unittest
import src.database as database
import src.answer as answer
from src.singleton_variables import Variables


class MyTestCase(unittest.TestCase):

    def test_add_question(self):
        word1 = 'pirmas'
        word2 = 'zodis'
        database.add_unique_word(word1)
        database.add_unique_word(word2)
        self.assertEqual(word1, Variables().unique_words[0])
        self.assertEqual(word2, Variables().unique_words[1])

        qa = {
            'labas': 'sveiki',
            'kaip sekas?': 'gerai',
            'koks jusu vardas?': 'ChatBot-19'
        }
        sk = 0
        for q, a in qa.items():
            database.add_question(q, a)
            self.assertEqual(a, Variables().questions[sk].answer[0])
            sk += 1

    def test_connect_to_database(self):
        self.test_add_question()
        database.connect_to_database(testing=True)

        db_questions = ['kada nuo koronos užsikrėtimo prasideda simptomai?', 'ar privaloma dėvėti kaukę parduotuvėje?',
                         'kur prasidėjo korona?', 'kam reikalinga kaukė?']
        for question in db_questions:
            self.assertTrue(
                question in [question.question for question in Variables().questions])

    def test_check_for_specific(self):
        # Arrange
        database.connect_to_database(testing=True)

        testsmap = {
            'korona': 'liga',
            'koronos': 'liga',
            'covid': 'liga',
            'covido': 'liga',
            'klaida': None
        }

        # Assert
        for word, changed in testsmap.items():
            result = answer.check_for_specific_word_patterns(word)
            self.assertEqual(changed, result)


if __name__ == '__main__':
    unittest.main()
