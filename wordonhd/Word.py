from Grid import Grid
from copy import copy


class Word(object):
    def __init__(self, grid, letters, wordons=[]):
        assert isinstance(grid, Grid)
        self._grid = grid
        self._letters = letters
        self._wordons = wordons

    @property
    def value(self):
        value = self._grid.score(self._letters)
        missing = list(filter(lambda x: x not in self._letters, self._wordons))

        value -= sum(map(lambda x: x.value))

        if len(missing) == 0:
            value *= 2
        return value

    @staticmethod
    def find_all(letters, grid, locale='nl3'):
        words = []
        file = 'dictionary/{}.lang'.format(locale)
        letters_raw = list(map(lambda x: x.letter, letters))
        wordons = list(filter(lambda x: x.wordon, letters))

        with open(file, 'r') as f:
            for word in f.readlines():
                word = word.strip()
                order = []
                cache = list(letters_raw)
                valid = True

                for i in range(len(word)):
                    if word[i] in cache or '#' in cache:
                        order.append(i)
                        cache.pop(i)
                    else:
                        valid = False

                if valid:
                    letters_out = list(map(lambda x: copy(letters[x]), order))

                    # Find and ajust wildcards
                    for i in range(len(letters_out)):
                        if letters_out[i].letter == '#':
                            letters_out[i].real = word[i]

                    words.append(Word(grid, letters_out, wordons))

        words.sort(reverse=True, key=lambda x: x.value)
        return words