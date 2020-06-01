#!/usr/bin/env python3
import os
import gmpy2

flag = b'CTF-BR{HW_1p_Pr073cT1on_1S_$3Cur1ty_By_oBscUr4n71Sm}'
validate_eq = True

k  = int.from_bytes(os.urandom(256//8),byteorder='big')
m  = int.from_bytes(flag,byteorder='big')
p  = int(gmpy2.next_prime(int.from_bytes(os.urandom(len(flag)),byteorder='big')))
q  = int(gmpy2.next_prime(int.from_bytes(os.urandom(len(flag)),byteorder='big')))

kinv = int(gmpy2.invert(k,p))

c1 = (kinv*(p+m-q))%p
c2 = (kinv*(p+2-q))%p

assert (q+k*c1)%p == m
assert (q+k*c2)%p == 2

if validate_eq:
    from wolframclient.evaluation import WolframLanguageSession
    from wolframclient.language import wl, wlexpr
    session = WolframLanguageSession()
    res, = session.evaluate(wlexpr('q=%d;c2=%d;p=%d; ' % (q, c2, p) +
                                   'k /. Solve[Mod[q+k*c2, p] == 2 && 0 <= k < p, k, Integers]'))
    session.terminate()
    assert res == k

print('// LICENSE_KEY=%d' % k)
print()
print("Integer p  = 'h%x;" % p)
print("Integer q  = 'h%x;" % q)
print("Integer c1 = 'h%x;" % c1)
print("Integer c2 = 'h%x;" % c2)
