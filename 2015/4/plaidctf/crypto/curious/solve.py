from rsa_wiener_attack.RSAwienerHacker import hack_RSA

f = open('captured_a4ff19205b4a6b0a221111296439b9c7', 'r')

lines = f.readlines()

for line in lines:
    line = line.strip()
    if line.startswith('{0x'):
        line = line[1:-1].split(' : ')
        n = int(line[0], 0)
        e = int(line[1], 0)
        c = int(line[2], 0)
        d = hack_RSA(e, n)
        print '.',
        if d is not None:
            print '\n---------------------'
            m = pow(c, d, n)
            print 'flag = ' + hex(m)[2:-1].decode('hex')
            print '---------------------\n'