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

        value -= sum(map(lambda x: x.value, missing))

        if len(missing) == 0:
            value *= 2
        return value

    @staticmethod
    def find_all(letters, grid, locale='nl3'):
        words = []
        file = 'dictionary/{}.lang'.format(locale)
        letters.sort(key=lambda x: x.weight, reverse=True)
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
                        indexes = [j for j, k in enumerate(letters_raw) if k == word[i]]
                        for j in indexes:
                            if j not in order:
                                order.append(j)
                                break
                        cache.pop(cache.index(word[i]))
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

    def __str__(self):
        return ','.join(l.__str__() for l in self._letters)