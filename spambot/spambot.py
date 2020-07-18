import requests
import json
import string
import os
import random
import argparse

def _get_data():
    with open('db.json', 'r') as f:
        return json.load(f)


db = _get_data()

NAMES = db['names']
CARRIERS = db['carriers']
PASSWORDS = db['passwords']

SALT_DIGITS = (0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 4, 4, 5)

class Payload:
    @staticmethod
    def _get_salt():
        number_of_digits = random.choice(SALT_DIGITS)
        return ''.join(str(random.randint(0, 9)) for x in range(number_of_digits))

    def __init__(self):
        self._name = random.choice(NAMES) + self._get_salt()
        self._carrier = random.choice(CARRIERS)
        self.password = random.choice(PASSWORDS) + self._get_salt()

    @property
    def email(self):
        return f'{self._name}@{self._carrier}'

def send_request(session, url, email_field, password_field):
    payload = Payload()
    session.post(url, data={
        email_field:payload.email,
        password_field:payload.password
    })

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('email')
    parser.add_argument('password')
    parser.add_argument('-t', '--requests')
    args = parser.parse_args()

    session = requests.Session()
    for i in range(args.requests or 1000):
        send_request(session, url, args.email, args.password)
