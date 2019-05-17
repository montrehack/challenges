#!/usr/bin/env python3

import base64
import random
import json
from argparse import ArgumentParser
from os import urandom

from cryptography.hazmat.primitives import padding, hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey

from flask import Flask, request, send_from_directory, jsonify

app = Flask(__name__)

secret = b""
salt = b""
encrypted_secret = {}

users = {}


def main():
    global salt, secret, encrypted_secret

    salt = urandom(32)
    secret = gen_flag().encode('utf-8')
    key = urandom(32)

    id = base64.b64encode(urandom(16)).decode('utf-8')

    encrypted_secret = {'id': id, 'encrypted_password': base64.b64encode(encrypt(secret, key)).decode('utf-8')}

    secret = hash_password(secret)

    users[id] = key


def gen_flag():
    a = "0123456789abcdef"
    b = "FLAG-{"
    for _ in range(0, 32):
            b = b + random.choice(a)
    b = b + "}"
    return b


def encrypt(data, key):
    iv = urandom(16)
    padder = padding.PKCS7(128).padder()
    data = padder.update(data) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend()).encryptor()
    return iv + cipher.update(data) + cipher.finalize()


def decrypt(data, key):
    iv = data[0:16]
    data = data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend()).decryptor()
    data = cipher.update(data) + cipher.finalize()
    padder = padding.PKCS7(128).unpadder()
    return padder.update(data) + padder.finalize()


def hash_password(data):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(data)


@app.route('/')
def get_index():
    return send_from_directory('website', 'index.html')


@app.route('/api/check-password', methods=["POST"])
def check_password():
    id = request.get_json().get('id')
    encrypted_pass = base64.b64decode(request.get_json().get('encrypted_password').encode('utf-8'))
    key = users[id]
    try:
        password = decrypt(encrypted_pass, key)
        password_hash = hash_password(password)
        if secret == password_hash:
            return jsonify({'data': "Good password!"})
        else:
            return jsonify({'data': "Bad password!"})
    except:
        return jsonify({'data': "Bad password!"})


@app.route('/api/verify', methods=["POST"])
def verify_key():
    if hash_password(request.get_json().get('data').encode('utf-8')) == secret:
        return jsonify({'data': "You won!"})
    else:
        return jsonify({'data': "Invalid!"})


@app.route('/api/key-exchange', methods=["POST"])
def key_exchange():
    key_pair = X25519PrivateKey.generate()
    public_key = key_pair.public_key()
    peer_public_key = X25519PublicKey.from_public_bytes(base64.b64decode(request.get_json().get('data').encode('utf-8')))
    secret = key_pair.exchange(peer_public_key)
    id = base64.b64encode(urandom(16)).decode('utf-8')
    users[id] = secret
    return jsonify({'id': id, 'public_key': base64.b64encode(
        public_key.public_bytes(encoding=serialization.Encoding.Raw,
                                format=serialization.PublicFormat.Raw)).decode('utf-8')})


@app.route('/api/leak')
def get_leak():
    return jsonify({'data': json.dumps(encrypted_secret)})


@app.route('/<path:path>.wasm')
def get_wasm(path):
    return send_from_directory('website', path + ".wasm"), {'Content-Type': 'application/wasm'}


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
