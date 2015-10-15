from Session import Session, ScreenId
import requests
from Word import Word
from Letter import Letter
from Grid import Grid


class Game(object):
    def __init__(self, parent, data):
        assert isinstance(parent, Session)
        self.parent = parent
        self.gamedata = data

        data = {
            'authToken': parent.authtoken,
            'sid': ScreenId.GAME_VS_PLAYER,
            'gid': self.id,
            'cycle': int(self.gamedata['cycle']) + 1,
            'newchats': 0,
        }

        resp = requests.post(Session.SERVER_LISTEN, data).json()
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

    def play(self):
        if self.gamedata['turnUserId'] != self.gamedata['yourId']:
            return
        if int(self.gamedata['state']) != 1:
            return

        words = Word.find_all(self.letters, self.grid, self.locale)
        if len(words) == 0:
            self.swap()
        else:
            for word in words:
                if self.submit_word(word):
                    return
            self.swap()  # in case we couldn't play anything

    def submit_word(self, word):
        assert isinstance(word, Word)

        data = {
            'authToken': self.parent.authtoken,
            'word': word.__str__(),
            'bestWord': word.__str__().replace('!', ''),
            'gameId': self.id,
        }
        url = "{}/game/play".format(Session.SERVER)

        res = requests.post(url, data).json()
        if 'game' in res:
            self.instance = res['game']

        return 'game' in res

    def swap(self):
        data = {
            'authToken': self.parent.authtoken,
            'gameId': self.id,
        }

        url = "{}/game/swap".format(Session.SERVER)
        requests.post(url, data)