class Grid(object):
    _modifiers = {
        '1': lambda x: x * 2,
        '2': lambda x: x * 3,
        '4': lambda x: x + 10,
    }

    def __init__(self, grid):
        self._grid = grid.split(',')
        self._grid_mod = tuple(map(lambda x: self._modifiers.get(x, lambda _: _),
                                   self._grid))

    def score(self, word):
        score = 0
        for i in range(len(word)):
            score += self._grid_mod[i](word[i].value)

        return score

    def new_wordon(self, word):
        index = [i for i, l in enumerate(self._grid) if l is '3']
        wordons = []

        for i in index:
            if len(word) >= index:
                wordons.append(word[i])

        return wordons

    def __str__(self):
        return ','.join(self._grid)