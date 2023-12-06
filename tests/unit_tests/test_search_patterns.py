import unittest
import src.helpers.search_patterns as patterns


class MyTestCase(unittest.TestCase):

    def test_decompose(self):
        # Arrange
        testsmap = {
            'Labas vakaras. Kaip gyvuojate. Kiek šiandien M. K. Brazausko atvejų?': 'Kiek šiandien M. K. Brazausko '
            'atvejų?',
            'Kiek dabar valandų? Ar dar dirba parduotuvė?': 'Kiek dabar valandų?',
            'Kiek šiandien koronos atvejų?': 'Kiek šiandien koronos atvejų?',
            'Kur aš gyvenu????????': 'Kur aš gyvenu?',
            'kiek pasaulyje susirgimų': 'kiek pasaulyje susirgimų'
        }

        # Assert
        for sentence, correct in testsmap.items():
            result = patterns.decompose(sentence)
            self.assertEqual(correct, result)

    def test_multiple_question_marks(self):
        # Arrange
        testsmap = {
            'kaip laikaisi?????': 'kaip laikaisi?',
            'kaip laikaisi????? Ar gerai???': 'kaip laikaisi? Ar gerai?',
            'ne klausimas': 'ne klausimas'
        }

        # Assert
        for sentence, correct in testsmap.items():
            result = patterns.multiple_question_marks(sentence)
            self.assertEqual(correct, result)


if __name__ == '__main__':
    unittest.main()
