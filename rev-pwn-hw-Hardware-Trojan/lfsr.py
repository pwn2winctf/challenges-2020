#!/usr/bin/python3
import re

with open('Rocket.v') as f:
    code = f.read()

reg = 128 * [0]
poly = 0
for m in re.finditer(r"""\.INIT\(1'b([01])\)\)\s*\\trig_mem_data_reg\[(\d+)\].*?\.D\(([^)]+)\)""", code, re.DOTALL):
    val = int(m.group(1))
    pos = int(m.group(2))
    d = m.group(3)
    if '_GEN_277' not in d:  # just a shift-reg net
        if '\\trig_mem_data_reg[126]_0 [0]' not in d:  # not really a tap (carries the bit to the next FF in shift-reg)
            print(f'tap at {pos}: {d}')
            poly |= (1 << pos)
    reg[pos] = val

value = int('0b' + ''.join(map(str, reg[::-1])), 2)

print(f'initial value: {hex(value)}')
print(f'polynomial: {hex(poly)}')

target = int('0x' + b'CTF-BR{'[::-1].hex(), 16)

while (value & 0xffffffffffffff) != target:
    if (value & 1) == 1:
        value = (value >> 1) ^ poly
    else:
        value = (value >> 1)

flag = bytes.fromhex(hex(value)[2:])[::-1].decode('ascii')
print(f'flag: {flag}')
