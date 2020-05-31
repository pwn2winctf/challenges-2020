#!/usr/bin/python3
import socket


def pprint(s):
    print(str(s,"utf-8"),end="")

def recvline(s):
    resp=b""
    while True:
        chunk=s.recv(1)
        resp+=chunk
        if chunk==b"\n" or not chunk:
            break
    return resp


def sendElf(fname,addr="127.0.0.1",port=8080):
    with open(fname,"rb") as f:
        payload=f.read()
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((addr,port))

    for i in range(4):
        x=recvline(s)
        pprint(x)

    s.sendall(b"%i"%len(payload))
    x=recvline(s)
    pprint(x)
    s.sendall(payload)

    while True:
        part=recvline(s)
        pprint(part)
        if not part:
            break
sendElf("./solve")
