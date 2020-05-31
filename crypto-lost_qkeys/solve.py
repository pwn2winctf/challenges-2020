from pwn import *
from Crypto.Util.number import long_to_bytes, bytes_to_long


def encode(m):
    return '{:0{}x}'.format(m, nbytes)

def decode(m):
    return '{:0{}b}'.format(int(m, 16), nbits)[-nbits:]

accum = []

for _ in range(50):
    #p = remote('quantum.pwn2.win', 1337)
    p = process(['./server.py'])

    p.readuntil('passwd:\n')
    p.sendline('0')
    res = p.readline()
    accum.append(res)

    nbytes = (max([len(e) for e in accum])-1)//2 + 1
    nbits = nbytes*8

    r = ['{:0{}b}'.format(int(s, 16), nbits) for s in accum]
    num_res = len(accum)

    counts = [0]*len(r[0])
    for entry in r:
        for i,a in enumerate(entry):
            if a=='1':
                counts[i] += 1

    # prob is 0.75
    out = ['0' if c < 0.5*num_res else '1' for c in counts]
    flag = ''.join(out)

    print(long_to_bytes(int(flag[::-1],2)))
