#!/usr/bin/env python3

## CBC 4

# The problem here is that the server gives you an information regarding wether or not the padding of the ciphertext is valid.
# What gives the oracle is the really high value of PBKDF2 iteration of the password.
# PBKDF2 is a Key Drivation Function that basically takes a password and hash it multiple time to make it harder to brute-force.
# Here, the iteration count is so absurd that it gives a major and noticeable delay when the server tries to hash the password, which it will try whenever it has been able to decrypt it(when the padding is valid)

# This one is a time based padding oracle. This is well documented on the internet.
# Basically, we can try to brute-force the last byte of the second last block to influence padding.
# Once we get a valid padding, that means that the decrypted padding was \x01(or the true padding, which is a edge case to consider).
# Then, if we XOR the initial byte with the new value and the \x01, we can get the true value of the last byte, by the power of maths.
# So basically: 
#  real_value ^ real_padding = decrypted_value
#  modified_value ^ modified_padding = decrypted_value
#  real_value ^ real_padding = modified_value ^ modified_padding
#  real_value = real_padding ^ modified_value ^ modified_padding
# Next, we can force this byte to \x02 with another XORing trick:
#  modified_value = modified_padding(\x02) ^ real_value ^ real_padding
# We can then brute-force the next byte by trying to get a valid padding by forcing \x02 to the second last byte.
# We continue, while taking care of dealing with the edge cases and block switches.
# To brute force the first block, we can crack it by usig the IV as the previous block.
# Sorry for the terrible script!

import requests
import base64
import json

address = 'http://127.0.0.1:5004'

# Get the leaked data
leak = json.loads(requests.get(address + '/api/leak').json().get('data'))

user_id = leak.get('id')
leaked_pass = base64.b64decode(leak.get('encrypted_password').encode('utf-8'))

answer = []

# This is the "correct" padding of the current step
pm = 1

# Get time delta. This is a simple treshold to determine if the padding was valid, but this can be done better with a bit of statistical theory for better results with lower delay or higher network jitter.
good_time = requests.post(address + '/api/check-password', json={'id': user_id,
                                                                            'encrypted_password': base64.b64encode(
                                                                                leaked_pass).decode(
                                                                                'utf-8')}).elapsed.total_seconds()
bad_time = requests.post(address + '/api/check-password',
                         json={'id': user_id, 'encrypted_password': base64.b64encode(
                             leaked_pass[:-17] + bytes([0x00]) + leaked_pass[-16:]
                         ).decode('utf-8')}).elapsed.total_seconds()

time_delta = (good_time - bad_time) * 0.5 + bad_time

print("Treshold: " + str(time_delta))

# This is the major loop that brute-force one character at the time.
for _ in range(0, len(leaked_pass) - 16):
    # Get current part of the answer for the setup
    if len(answer) < 16:
        current_ans = answer
    else:
        current_ans = answer[:-(len(answer) // 16) * 16]

    # Setup for the oracle to get correct padding on the known bytes.
    setup = [a ^ pm ^ leaked_pass[-16 - len(answer) + i] for (i, a) in enumerate(current_ans)]

    # This is the single-byte brute-force part
    for i in range(0, 256):

        # Get the last block
        if len(answer) < 16:
            last_block = leaked_pass[-16:]
        else:
            last_block = leaked_pass[-(len(answer) // 16 + 1) * 16:-(len(answer) // 16) * 16]

        # This is the actual payload to send.
        # Truncated current block + byte to brute-force + current answer + next block
        payload = leaked_pass[:-((len(answer) // 16 + 1) * 16) - 1 - len(setup)] \
                  + bytes([i]) + bytes(setup) + last_block

        # Send payload and check the oracle
        if not (payload == leaked_pass and len(answer) == 0):
            if requests.post(address + '/api/check-password',
                             json={'id': user_id,
                                   'encrypted_password': base64.b64encode(
                                       payload).decode(
                                       'utf-8')}).elapsed.total_seconds() > time_delta:
                # Get the plaintext char of the successful try and add it to the answer
                current_char = leaked_pass[-16 - 1 - len(answer)] ^ i ^ pm
                answer.insert(0, current_char)

                # Cycle pm from 1 to 16
                pm = pm % 16 + 1
                print(bytes(answer))
                break

# Remove padding
flag = bytes(answer[:-answer[-1]])

print("Flag: " + flag.decode('utf-8'))
