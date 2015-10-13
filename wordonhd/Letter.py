class Letter(object):
    _values = {
        'ENIOA': 1,
        'SDTR': 2,
        'MLKPBG': 3,
        'ZVUFJH': 4,
        'CW': 5,
        'XY': 8,
        'Q': 10
    }

    def __init__(self, letter):
        self.letter = letter[-1]
        self.wordon = letter[0] == '!'

    @property
    def value(self):
        return list(filter(lambda x: self.letter in x[0], self._values.items()))[0][1]