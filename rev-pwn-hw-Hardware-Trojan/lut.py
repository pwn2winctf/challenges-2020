#!/usr/bin/python3
import sys
import math

init_val = int(sys.argv[1], 16)
conditions_for = sys.argv[2]
assert conditions_for in {'0', '1'}

truthtable = bin(init_val)[2:]

num_inputs = math.ceil(math.log2(len(truthtable)))

truthtable = truthtable.rjust(2**num_inputs, '0')[::-1]

for i, val in enumerate(truthtable):
    if val == conditions_for:
        print(bin(i)[2:].rjust(num_inputs, '0'))
