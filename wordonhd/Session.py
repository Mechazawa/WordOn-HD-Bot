from enum import Enum
from logging import Logger
from string import ascii_letters, digits
from random import choice
from hashlib import md5
from Game import Game
from Util import post


def _random_string(length=16, pool=ascii_letters + digits):
    return ''.join(choice(pool) for _ in range(length))


class ScreenId(Enum):
    UNKNOWN = 0
    SPLASH = 1
    WELCOME = 2
    EMAIL_LOGIN = 3
    GAME_OVERVIEW = 4
    NEW_GAME = 5
    FRIENDS = 6
    FRIENDS_FB = 7
    SHOP = 8
    GAME_VS_PLAYER = 9
    SETTINGS = 10
    CHAT = 11
    EDIT_ACCOUNT = 12
    GAME_VS_CPU = 13
    GAME_TUTORIAL = 14
    SEARCH_PLAYER = 15
    LEGAL = 16
    AUTOLOGIN_FAIL = 17
    PROMOSHARE = 18
    NEW_GAME_SETTINGS = 19
    PROMOREDEEM = 20


class Session(object):
    SERVER = 'http://game.wordonhd.com'
    SERVER_LISTEN = 'http://listen.wordonhd.com/listen'
    SALT = 'ohf87ewyr87wfhj'

    overview_id = 0
    instances = {}

    def __init__(self, authtoken):
        self.logger = Logger('WordOn')
        self.authtoken = authtoken

    @staticmethod
    def login(email, password):
        data = {
            'udId': _random_string(pool=ascii_letters.lower() + digits),
            'deviceToken': _random_string(183, ascii_letters + digits + '-_'),
            'password': md5((password + Session.SALT).encode('ascii')).hexdigest(),
            'username': email,
            'country': 'nl-NL',
            'deviceId': 'Android Linux',
            'version': '1.88',
            'locale': 'nl',
        }

        resp = post('{}/account/login'.format(Session.SERVER), data=data)
        return Session(resp['user']['authToken'])

    def resume(self):
        self.logger.info('Resuming connection')

        data = {
            'authToken': self.authtoken,
            'timestamp': 0
        }

        resp = post('{}/game/resume'.format(self.SERVER), data=data)

        if 'invitesPending' in resp:
            for invite in resp['invitesPending']:
                self.invite_accept(invite)

    def listen(self, on_list=None, on_overview=None, on_invite=None):
        while True:
            data = {
                'authToken': self.authtoken,
                'overviewId': self.overview_id,
                'sid': ScreenId.GAME_OVERVIEW,
            }
            self.overview_id += 1

            #print('beep')
            resp = post(self.SERVER_LISTEN, data, timeout=None)
            #print(json.dumps(resp, indent=4))
            if 'gameList' in resp:
                (on_list or self.parse_game_list)(resp['gameList'])
            if 'gameOverview' in resp:
                print('overview')
                (on_overview or self.handle_overview)(resp['gameOverview'])
            if 'invite' in resp:
                func = on_invite or self.invite_accept
                list(map(func, resp['invite']['invitesPending']))

            for _, game in self.instances.items():
                game.play()

    def invite_accept(self, pending):
        url = "{}/game/invitation".format(self.SERVER)
        key = 'id' if 'displayname' in pending else 'invId'
        print('accepting invite from ' + pending[key])
        data = {
            'gameInviteId': pending[key],
            'action': 'accept',
            'authToken': self.authtoken,
            'tilesetId': 0,
        }

        post(url, data)

    def parse_game_list(self, data):
        for game in data:
            if int(game['state']) != 1:
                continue

            self.instances[game['id']] = Game(self, game)

    def handle_overview(self, data):
        self.instances[data['id']].update(data)