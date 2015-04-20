__author__ = 'Ping'
import itertools

# i reused inverse_mod fuction from crypto lazy challenge
from crypto.lazy.utils import inverse_mod

# http://blogs.msdn.com/b/drnick/archive/2006/09/20/attacks-on-rsa.aspx

def solve_equation(a, b, c):
    """
    This function solve linear Diophantine equation of the form ax + by = c
    """
    q, r = divmod(a, b)
    if r == 0:
        return [0, c / b]
    else:
        sol = solve_equation(b, r, c)
        u = sol[0]
        v = sol[1]
        return [v, u - q * v]


def get_data_from_file():
    """
    Get list e, c and n from input file
    """
    f = open('captured_827a1815859149337d928a8a2c88f89f', 'r')
    n, list_c, list_e = 0, [], []
    captures = f.readlines()
    for capture in captures:
        capture = capture.strip()
        if capture.startswith('{0x'):
            capture_list = capture[1:-1].split(' : ')
            n = int(capture_list[0], 0)
            e = int(capture_list[1], 0)
            c = int(capture_list[2], 0)
            list_e.append(e)
            list_c.append(c)
    f.close()
    return n, list_c, list_e

n, c, e = get_data_from_file()

# Get 2-k-combination of set e
combine_e = list(itertools.combinations(e, 2))

a1, a2, e1, e2 = 0, 0, 0, 0


# try to solve Diophantine equation
for _e in combine_e:
    res = solve_equation(_e[0], _e[1], 1)
    if res != [0, 0]:
        a1 = res[0]
        a2 = res[1]
        e1 = _e[0]
        e2 = _e[1]

c1 = c[e.index(e1)]
c2 = c[e.index(e2)]

# i compute m = (a1^c1 * a2^c2) mod n
# http://en.wikipedia.org/wiki/Modular_exponentiation?hc_location=ufi
# the following formula given by my young friend zihawk
m = (pow(inverse_mod(c1, n), abs(a1), n) * pow(c2, a2, n)) % n


# and i got the flag
print hex(m)[2:-1].decode('hex')
