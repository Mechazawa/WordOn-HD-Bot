from enum import Enum


class ApiErrorCode(Enum):
    PHP_INVALID = 0
    PHP_MISSING_PARAMS = 1
    PHP_AUTH_FAILED = 2
    PHP_NAME_INVALID = 4
    PHP_USERNAME_INVALID = 5
    PHP_USER_ALREADY_EXISTS = 6
    PHP_PASSWORD_INVALID = 7
    PHP_USER_NOT_FOUND = 8
    PHP_WORD_INVALID = 9
    PHP_USER_UNAUTH = 10
    PHP_NAME_EXISTS = 11
    PHP_ALREADY_HAS_ITEM = 12
    PHP_NOT_ENOUGH_COINS = 13
    PHP_MAX_NAMECHANGES = 14
    PHP_USER_MAX_GAMES = 15
    PHP_OTHER_USER_MAX_GAMES = 16
    PHP_FB_ALREADY_EXISTS = 17
    PHP_GAME_INVITE_ALREADY_SENT = 18
    PHP_GET_LOCK_FAIL = 19
    PHP_NOT_ENOUGH_STARS = 20
    PHP_PAYMENT_APPROVAL = 21
    PHP_MAX_HS = 22
    PHP_USER_TYPE_INVALID = 23
    PHP_MISSING_ITEM = 24
    PHP_IS_FB_USER = 25
    PHP_PROMOCODE_INVALID = 32
    PHP_PROMOCODE_ONLY_NEW_PLAYERS = 33
    PHP_PROMOCODE_ALREADY_REDEEMED = 34
    PHP_DEFINITION_UNSUPPORTED = 48
    PHP_DEFINITION_UNAVAILABLE = 49
    PHP_DEFINITION_PARSE_ERROR = 50
    POLL_INVALID_GAME = 237
    POLL_INVALID_AUTH = 238
    POLL_INVALID_REQUEST = 239
    ALERT_MAX_GAMES = 1
    ALERT_SNEAK_PEEK = 2
    NULL_ERROR = 251
    PARSE_ERROR = 252
    SECURITY_ERROR = 253
    IO_ERROR = 254
    TIME_OUT_ERROR = 255


class ApiException(Exception):
    def __init__(self, code):
        if isinstance(code, dict):
            code = code['error']
        name = ApiErrorCode(code).name
        message = 'ApiException: {name}, {code}'.format(name=name, code=code)
        super(ApiException, self).__init__(message)