#!/usr/bin/python3
import re

with open('RocketTile.v') as f:
    code = f.read()

res = []
for m in re.finditer(r"\.INIT\(64'h66666F6666666066\)[^;]*?"
                     r"\.I1\(mem_reg_pc\[(\d+)\]\)[^;]*?"
                     r"\.I5\(dcacheArb_io_requestor_1_s1_data_data\[(\d+)\]",
                     code, re.DOTALL):
    pc_pos, word_pos = map(int, m.groups())
    res.append((pc_pos, word_pos))

res.sort()
for i, (pc_pos, word_pos) in enumerate(res):
    if i != 0 and word_pos != res[i - 1][1] + 1:
        print()
    print('trig_pc[%2d] = word[%2d]' % (pc_pos, word_pos))
