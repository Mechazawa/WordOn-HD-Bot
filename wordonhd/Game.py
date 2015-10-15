from Session import Session, ScreenId
import requests


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

    def play(self):
        if self.gamedata['turnUserId'] != self.gamedata['yourId']:
            return
        if int(self.gamedata['state']) != 1:
            return

        print('skipping: {}'.format(self.gamedata['dictionaryId']))

    def swap(self):
        data = {
            'authToken': self.parent.authtoken,
            'gameId': self.id,
        }

        url = "{}/game/swap".format(Session.SERVER)
        requests.post(url, data)