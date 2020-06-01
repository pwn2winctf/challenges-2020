#!/usr/bin/python3 -u
import os
from Crypto.Util.number import bytes_to_long
import random


def encode(m):
    return '{:0{}x}'.format(m, nbytes)


def decode(m):
    return '{:0{}b}'.format(int(m, 16), nbits)[-nbits:]

flag = b'_#__CTF-BR{_1s_th4t_HoW_u_1mPl3meNt_@_QUantUm_0ne_t1m3_paD_???}__'
nbytes = len(flag)
nbits = 8*nbytes
num_shots = 1
expanded_flag = decode(encode(bytes_to_long(flag)))

# In each connection
key = decode(encode(bytes_to_long(os.urandom(nbytes))))

pwd = input('passwd:\n')
try:
	expanded_pwd = decode(pwd)
	shot = ''
	for k, p, f in zip(key, expanded_pwd, expanded_flag):
		if k==p:
	        	# noise?
		        shot += f
		else:
			shot += '1' if random.randint(0, 1) else '0'
			res = encode(int(shot[::-1],2))
	print(res)

except:
	pass