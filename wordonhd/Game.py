import requests
from Word import Word
from Letter import Letter
from Grid import Grid
from time import sleep


class Game(object):

    SERVER = 'http://game.wordonhd.com'
    SERVER_LISTEN = 'http://listen.wordonhd.com/listen'

    def __init__(self, parent, data):
        self.parent = parent
        self.gamedata = data

        data = {
            'authToken': parent.authtoken,
            'sid': 9,
            'gid': self.id,
            'cycle': int(self.gamedata['cycle']) + 1,
            'newchats': 0,
        }

        resp = requests.post(self.SERVER_LISTEN, data).json()
        self.instance = resp['game']

    @property
    def id(self):
        return self.gamedata['id']

    @property
    def letters(self):
        return Letter.from_raw(self.instance['yourLetters'] +
                               self.instance.get('yourWordons', ''))

    @property
    def grid(self):
        return Grid(self.instance['yourGrid'])

    @property
    def locale(self):
        return self.gamedata["dictionaryId"]

    @property
    def my_turn(self):
        if self.gamedata['turnUserId'] != self.gamedata['yourId']:
            return False
        if int(self.gamedata['state']) != 1:
            return False

        return True

    def play(self):
        if not self.my_turn:
            return

        words = Word.find_all(self.letters, self.grid, self.locale)
        if len(words) == 0:
            self.swap()
        else:
            for word in words:
                if self.submit_word(word):
                    return
            self.swap()

    def submit_word(self, word, wait=3):
        assert isinstance(word, Word)
        if wait > 0:
            print('Waiting {}s'.format(wait))
            sleep(wait)
        print('playing {} for {} points against {}'
              .format(word.__str__(), word.value, self.gamedata['otherName']))

        data = {
            'authToken': self.parent.authtoken,
            'word': word.__str__(),
            'bestWord': word.__str__().replace('!', ''),
            'gameId': self.id,
        }
        url = "{}/game/play".format(self.SERVER)

        res = requests.post(url, data).json()
        valid = 'game' in res

        if valid:
            self.instance = res['game']

        return valid

    def swap(self):
        data = {
            'authToken': self.parent.authtoken,
            'gameId': self.id,
        }

        print('swapping')
        url = "{}/game/swap".format(self.SERVER)
        requests.post(url, data)