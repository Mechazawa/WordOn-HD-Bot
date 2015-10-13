class Letter(object):
    _values = {
        '#': 0,  # Wildcard
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
        self.real = letter[-1]

    @property
    def weight(self):
        return self.value + self.wordon * 100

    @property
    def value(self):
        return list(filter(lambda x: self.letter in x[0], self._values.items()))[0][1]

    @staticmethod
    def from_raw(data):
        data = data.split(',')
        return list(map(Letter, data))

    def __str__(self):
        out = self.letter
        if self.wordon:
            out = '!' + out
        if self.letter != self.real:
            out += self.real

        return out

    def __repr__(self):
        return "<Letter '{}({})' val '{}'>".format(self.letter, self.real, self.value)

    def __cmp__(self, other):
        assert isinstance(other, Letter)
        return self.wordon == other.wordon and self.letter == other.letter