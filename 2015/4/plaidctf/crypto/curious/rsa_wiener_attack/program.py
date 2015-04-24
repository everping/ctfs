__author__ = 'Ping'
from common import *
# print modinv(37, 120)
p = 11
q = 13
n = p * q
phi = (p - 1) * (q - 1)
e = 17
d = modinv(e, phi)
m = 123
c = pow(m, e, n)
print c
print pow(c, d, n)