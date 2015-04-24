__author__ = 'Ping'
# coding: utf-8
def xgcd(a, b):
    """Giải thuật GCD(tìm ước chung lớn nhất) mở rộng:
    Trả về (gcd, x, y) với gcd là ước chung lớn nhất của a và b
    gcd = b nếu b khác 0, a = 0 và ngược lại.
    x,y là 2 số thỏa mãn gcd = ax+by."""
    prevx, x = 1, 0
    prevy, y = 0, 1
    while b:
        q, r = divmod(a, b)
        x, prevx = prevx - q * x, x
        y, prevy = prevy - q * y, y
        a, b = b, r
    return a, prevx, prevy


def modinv(a, m):
    """Trả về giá trị nghịch đảo qua modul m của a"""
    a, u, v = xgcd(a, m)
    if a <> 1:
        raise Exception('No inverse: %d (mod %d)' % (a, m))
    while (u < 0):
        u += m
    return u