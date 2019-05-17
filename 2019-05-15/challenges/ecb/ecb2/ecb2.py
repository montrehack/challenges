#!/usr/bin/env python3

import base64
from argparse import ArgumentParser
import random
from os import urandom

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

from flask import Flask, request, send_from_directory

app = Flask(__name__)

secret = ""
key = b""


def main():
    global key, secret
    key = urandom(32)
    secret = gen_flag()


def encrypt(data):
    padder = padding.PKCS7(128).padder()
    data = padder.update(data) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend()).encryptor()
    return cipher.update(data) + cipher.finalize()


def gen_flag():
    a = "0123456789abcdef"
    b = "FLAG-{"
    for _ in range(0, random.randint(16, 32)):
            b = b + random.choice(a)
    b = b + "}"
    return b


@app.route('/')
def get_index():
    return send_from_directory('website', 'index.html')


@app.route('/api/encrypt', methods=["POST"])
def post_encrypt():
    data = base64.b64decode(request.get_json().get('data').encode('utf-8')).decode('utf-8')
    data = data + secret
    return base64.b64encode(encrypt(data.encode('utf-8')))


@app.route('/api/verify', methods=["POST"])
def verify_token():
    if request.get_json().get('flag') == secret:
        return "You won!"
    else:
        return "Not the right flag!"


@app.route('/<path:path>')
def get_website(path):
    return send_from_directory('website', path)

main()

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-H',
                        '--host',
                        action='store',
                        dest='host',
                        default='127.0.0.1',
                        help='Host address')
    parser.add_argument('-p',
                        '--port',
                        action='store',
                        dest='port',
                        default=5000,
                        help='Host port')

    args = parser.parse_args()

    app.run(host=args.host, port=args.port)
