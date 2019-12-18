#!/usr/bin/env python
from ctypes import cdll, c_char, create_string_buffer as csb
from socket import gethostname
import time
from subprocess import Popen, PIPE
from pwn import *

HOST='127.0.0.1'
PORT=14141

info('Loading libprotect')
protector = cdll.LoadLibrary("./libprotect.so")

h = csb(b'paradise')
t = int(time.time())

info('Generating password for paradise...')
buf = (c_char * 100).from_buffer(bytearray(100))
protector.GeneratePassword(buf, h, t)

pwd = buf.value.decode()
success('flag:' + pwd)

p = ssh('flag', HOST, PORT, password=pwd)
s = p.process('/bin/sh')
s.sendline('cat ~/flag.txt')
s.recvuntil('FLAG')
flag = 'FLAG' + s.recvline()
success(flag)
