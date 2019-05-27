#!/usr/bin/env python3

## CTR 1

# The problem here is the use of a static nonce, which is generated once the server is started and reused afterward for each request.

# This is a simple XOR Arithmetic. By XORing a known plaintext and ciphertext pair, you can get the keystream, which you can then XOR with a plaintext or ciphertext to encrypt/decrypt it.

import requests
import base64

address = "http://127.0.0.1:5005"

# Get the leaked ciphertext
c1 = base64.b64decode(requests.get(address + "/api/leak").text.encode())

# Get the encrypted value of 100 * 'a'
p2 = b"a" * 100
c2 = base64.b64decode(requests.post(address + "/api/encrypt", json={"data": p2.decode()}).text.encode())

# The maths are simple:
# p1 ^ c1 = keystream
# p2 ^ c2 = keystream
# p1 ^ c1 = p2 ^ c2
# p1 = c1 ^ p2 ^ c2

p1 = bytes([a ^ b ^ c for a,b,c in zip(c1, p2, c2)])

print(p1)

