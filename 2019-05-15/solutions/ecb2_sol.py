#!/usr/bin/env python3

## CBC 2

# The problem here is the use of ECB by itself.

# This one requires a byte-by-byte brute-force of the flag. 
# Since we can control the block layout, we can create a block full of 'a' and a character we want to try, and another block full of 'a' and the first character of the flag.
# When we get the right character, we can see that the two blocks are equals.
# Then, we can so blocks with 14 'a', the character we know and the next one we want to find and so on.

import base64
import requests

address = "http://127.0.0.1:5001"

# First, we need to find the size of the flag.
# Because of the PKCS padding, we can add a character until the ciphertext is 16 byte larger.
# that mean that the current block is full and a padding block has been added.

found = False
data = b""

prev_length = len(requests.post(address + "/api/encrypt", json={"data": base64.b64encode(data).decode('utf-8')}).text)
while not found:
    response = base64.b64decode(requests.post(address + "/api/encrypt", json={"data": base64.b64encode(data).decode('utf-8')}).text.encode('utf-8'))
    if len(response) > prev_length:
        size = len(response) - 16 - len(data)
        found = True
    else:
        data = data + b"a"

# Then, we brute force the flag.
# Note that we need to bruteforce on "blocks" larger than the actual block size since the flag is larger than that.

flag = b""

chars = b"FLAG-{0123456789abcdef}"

data_size = ((size // 16) + 1) * 16

for i in range(0, size):
    for c in chars:
        guess = b"a" * (data_size - len(flag) - 1) + flag + bytes([c])
        final_block = guess + b"a" * (data_size - len(flag) - 1)
        response = base64.b64decode(requests.post(address + "/api/encrypt", json={"data": base64.b64encode(final_block).decode('utf-8')}).text.encode('utf-8'))
        if response[0:data_size] == response[data_size:data_size * 2]:
            flag = flag + bytes([c])
            print(flag)
            break

print(flag)
