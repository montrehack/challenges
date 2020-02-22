#!/usr/bin/env python
# Encodes a flag for reveal
from itertools import cycle
from base64 import b64encode as b64
from random import randrange

# The key to use for xoring the base64
KEY = [ 0x42, 0x25, 0x33, 0x76]

FLAG = b"FLAG-vpsffrUV4OwpIqAR0j1HnwPelag0uL8C"

KEY2 = [f ^ k for (f, k) in zip(b64(FLAG), cycle(KEY))]
print(f'Flag Data is {len(KEY2)} bytes long')

DATA = [randrange(0x00, 0xFF) for _ in range(500)]
DATA[50:50+len(KEY2)] = KEY2


out = 'const KEY: [u8; 500] = [\n'
out += ', '.join([f'0x{b:02x}' for b in DATA])
out += '];'

print(f'// KEY: {KEY2}')
print(out)



key = ''.join([f'\\x{b:02x}' for b in KEY])
solve = f'''
# Solution:
echo -en "{key}" > uVh32NpQz
echo -en "{FLAG.decode()}" >> uVh32NpQz
'''

print(solve)



