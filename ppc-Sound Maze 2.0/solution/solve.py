#!/usr/bin/python3
# *-* coding: utf-8 -*-

from queue import Queue

from pwn import *

from datetime import datetime as dt2
from typing import Tuple, Optional

import base64

host = "soundmaze.pwn2.win"
port = 31337
s = remote(host, port)

flag_fmt = b'CTF-BR'

EMPTY, BOMB, WALL, END, BOOM, VISITED = tuple(b'.*#F0Z')
HASHES = {'052aee2948b3485bb5d12b231b508578146f16720e1c162f22408b55': WALL,
          '8c3ee205b91aa508bd2548d9f1c2888e7ad299b3e7f94d0e922f996a': END,
          'd804d31dc67f68e2a4d3de8b9fb8a916771b51f5f12d48c9148f8f21': EMPTY,
          '1e86360e4439f5af5850067d5ef3f8c09399db19b3cfa308d2923042': BOMB,
          'd14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f': VISITED,
          'b': BOOM}
INF = 9999999999999999999999999999999999
ANS = INF


class Maze:
    def __init__(self) -> None:
        self.el = {(0, 0): (EMPTY, INF)}
        self.xL = (0, 0)
        self.yL = (0, 0)
        self.d_end = INF
        
    def __contains__(self, pos: Tuple[int, int]) -> bool:
        return pos in self.el
        
    def __str__(self) -> str:
        return str(self.el)
        
    def get(self, pos: Tuple[int, int]) -> Optional[int]:
        if pos in self.el:
            return self.el[pos][0]
        
    def set(self, pos: Tuple[int, int], ev: bytes, d: int = INF) -> None:
        self.el[pos] = (ev, d)
        self.xL = (min(self.xL[0], pos[1]), max(self.xL[1], pos[1]))
        self.yL = (min(self.yL[0], pos[0]), max(self.yL[1], pos[0]))
        
    def set_d(self, pos: Tuple[int, int], d: int) -> None:
        self.el[pos] = (self.el[pos][0], d)
        
    def get_d(self, pos: Tuple[int, int]) -> Optional[int]:
        if pos in self.el:
            return self.el[pos][1]
        
    def isempty(self, pos: Tuple[int, int]) -> bool:
        return self.get(pos) == EMPTY
        
    def isend(self, pos: Tuple[int, int]) -> bool:
        return self.get(pos) == END
        
    def clear(self) -> None:
        self.__init__()


m = Maze()


def send_line(st):
    if isinstance(st, str):
        st = bytes(st, encoding='ascii')
    s.sendline(st)


def read_until(st: bytes, timeout=1.0) -> bytes:
    data = s.recvuntil(st, timeout=timeout)
    return data


def sha224(f: bytes) -> str:
    if f.endswith(b'.mp3'):
        b64 = bytes(base64.b64encode(open(f, 'rb').read()))
    else:
        b64 = f
    return hashlib.sha224(b64).hexdigest()


def new_position(pos: Tuple[int, int], c: bytes) -> Tuple[int, int]:
    if c == b'A':
        return pos[0]-1, pos[1]
    if c == b'D':
        return pos[0]+1, pos[1]
    if c == b'S':
        return pos[0], pos[1]+1
    if c == b'W':
        return pos[0], pos[1]-1


def content() -> bytes:
    try:
        cont = read_until(b'=\n\n\n').split(b'\n', 1)[1].split(b'=\n\n\n')[0]
        sha = sha224(cont)
        if sha in HASHES:
            return HASHES[sha]
        open('../deploy/test.mp3', 'wb').write(base64.b64decode(cont))
        print(f'Unknown file!\n{sha}')
        sys.exit(f'Unknown file!\n{sha}')
    except Exception as contentErr:
        raise Exception(f'content() - {contentErr}')


def go(pos: Tuple[int, int], c: bytes) -> Tuple[Tuple[int, int], bytes]:
    try:
        send_line(c)
        cont = content()
        npos = new_position(pos, c)
        if cont == BOOM:
            sys.exit('BOOOOOOOOM')
        if cont in [EMPTY, END] or (cont == VISITED and m.get(npos) in [EMPTY, END]):
            return npos, cont
        return pos, cont
    except Exception as goErr:
        raise Exception(f'go() - {goErr}')
    
    
op = {b'A': b'D', b'D': b'A', b'W': b'S', b'S': b'W'}

visited = set()


def dfs(v: tuple = (0, 0), d=0) -> None:
    global m
    try:
        if m.isend((0, 0)):
            m.d_end = 1
            return
        if m.isend(v):
            m.d_end = d+2
            return
        if v in visited or d > m.d_end:
            return
        if v != (0, 0):
            visited.add(v)
        for c in b'ADSW':
            c = bytes([c])
            if new_position(v, c) in visited:
                continue
            pos, ev = go(v, c)
            if pos != v:
                if ev != VISITED:
                    m.set(pos, ev)
                v = pos
                dfs(v, d+1)
                v, ev = go(v, op[c])
            else: 
                m.set(new_position(pos, c), WALL)
                visited.add(new_position(pos, c))
    except Exception as err2:
        print(f'dfs() - {err2}')


def bfs(ini: tuple = (0, 0)) -> int:
    if m.isend(ini):
        return 0
    fila = Queue()
    fila.put(ini)
    m.set_d(ini, 0)
    while not fila.empty():
        v = fila.get()
        for c in b'ADSW':
            c = bytes([c])
            w = new_position(v, c)  
            if w not in m:
                continue
            if m.get_d(w) == INF:   
                m.set_d(w, m.get_d(v)+1)
                if m.isend(w):
                    return m.get_d(w)  
                if m.isempty(w):
                    fila.put(w)  
    return -1


t0 = dt2.now()
data = ''
while True:
    try:
        m.clear()
        data = read_until(b'ROUND', timeout=1)
        t1 = dt2.now()
        print(data)
        if b'BR' in data:
            data += s.recvall()
            print(data)
            break
        visited = set()
        dfs()
        ANS = bfs()
        send_line(f'ANS {ANS}')
        print(f'ANS {ANS} {m.d_end}')
        t2 = dt2.now()
        print(t2-t1)
    except Exception as err:
        print(err)
        break

data += s.recvall()
print(data)
print(dt2.now()-t0)
