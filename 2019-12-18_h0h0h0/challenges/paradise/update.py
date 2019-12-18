#!/usr/bin/env python
from ctypes import cdll, c_char, create_string_buffer as csb
from socket import gethostname
from time import time, sleep
from subprocess import Popen, PIPE

protector = cdll.LoadLibrary("/root/libprotect.so")
h = gethostname().encode()
host = csb(h)
DELAY=30

def setPassword(host):
    t = int(time())
    buf = (c_char * 100).from_buffer(bytearray(100))
    protector.GeneratePassword(buf, host, t)
    pwd = buf.value.decode()
    with Popen(['passwd', 'flag'], stdin=PIPE, stdout=PIPE, stderr=PIPE) as p:
        (stdout, stderr) = p.communicate(input=(pwd+'\n'+pwd).encode())
    print(f'[+] t={t} flag:{pwd}')

print(f'[*] Starting script for hostname: {gethostname()}')
while True:
    setPassword(h)
    sleep(DELAY)
