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
            'gid': self.gamedata['id'],
            'cycle': int(self.gamedata['cycle']) + 1,
            'newchats': 0,
        }

        resp = requests.post(Session.SERVER_LISTEN, data).json()
        self.instance = resp.get('game', {})

    def update(self, data):
        pass