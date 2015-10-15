#!/usr/bin/env python3

from Session import Session
from getpass import getpass

s = Session.login('spam@ioexception.at', getpass())
s.resume()
s.listen()