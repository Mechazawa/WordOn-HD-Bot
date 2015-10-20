from unittest import TestCase, main
from Word import Word
from Grid import Grid
from Letter import Letter
from collections import namedtuple


WordFindTest = namedtuple('WordTest', ['letters', 'grid', 'topword', 'language', 'topvalue', 'wordcount'])
WordValueTest = namedtuple('WordValueTest', ['letters', 'grid', 'value', 'wordons'])


class WordTestCase(TestCase):
    pass


cases = [
    WordFindTest('A,I,G,O,E,E,N,!D,!#', '3,2,3,0,0,0,4', 'A,G,E,^R,E,N,!D', 'nl', 50, 1928),
    WordValueTest('!A,L,A,R', '1,0,0,3,0,3,4', 4, 'I,A'),
    WordValueTest('S,L,A,N,T,E,!R', '1,0,0,3,0,3,4', 36, 'R'),
]


def _find_case_generator(test):
    def test_case_find(self):
        letters = Letter.from_raw(test.letters)
        grid = Grid(test.grid)
        words = Word.find_all(letters, grid, test.language)

        assert len(words) is test.wordcount
        assert words[0].__str__() == test.topword
        assert words[0].value == test.topvalue

    return test_case_find


def _value_case_generator(test):
    def test_case_value(self):
        letters = Letter.from_raw(test.letters)
        grid = Grid(test.grid)
        word = Word(grid, letters, Letter.from_raw(test.wordons))
        print(word.__repr__())

        assert word.value is test.value

    return test_case_value

if __name__ == '__main__':

    for test in cases:
        name = 'unknown'
        test_case = lambda x: None

        if isinstance(test, WordFindTest):
            test_case = _find_case_generator(test)
            name = 'find'
        if isinstance(test, WordValueTest):
            test_case = _value_case_generator(test)
            name = 'value'

        sanitize = lambda x: ''.join(l for l in x if l not in ',!#')
        name = "test_{}_{}_{}".format(name, sanitize(test.letters), sanitize(test.grid))
        setattr(WordTestCase, name, test_case)

    main()
