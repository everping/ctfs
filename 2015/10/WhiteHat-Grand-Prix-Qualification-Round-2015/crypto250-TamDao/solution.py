import copy
import requests

BLOCK_SIZE = 16
HMAC_SIZE = 20

URL = "http://lab11b.grandprix.whitehatvn.com:1337/"


def get_msg(ck):
    cookie = dict(wanted=ck)
    r = requests.get(URL, cookies=cookie)
    return r.text


def chunks(l, n):
    if n < 1:
        n = 1
    return [l[i:i + n] for i in range(0, len(l), n)]


def get_cipher(prefix='', suffix=''):
    url = (URL + '?pre=%s&suf=%s' % (prefix, suffix))
    r = requests.get(url)
    return r.cookies['wanted'].decode('hex')


def get_secret_size():
    base_len = len(get_cipher())
    for s in range(1, BLOCK_SIZE + 1):
        prefix = chr(0x42) * s
        trial = len(get_cipher(prefix))
        if trial > base_len: break
    return base_len - BLOCK_SIZE - HMAC_SIZE - s


# This challenge is related to a known attack - Poodle Attack
# I did look into the code of l4w for reference http://l4w.io/2015/01/tetcon-ctf-2015-crypto200-the-poodle-attack/
# Thanks young guy :)
def get_secret():
    secret_size = get_secret_size()
    _secret = ""
    for m in range(1, 3):
        for n in range(BLOCK_SIZE - 1, -1, -1):
            if len(_secret) == secret_size:
                break

            prefix = 'B' * (n % BLOCK_SIZE)
            suffix = 'C' * (secret_size - (n % BLOCK_SIZE))
            cookie = get_cipher(prefix, suffix)
            cipher_block = chunks(cookie, 16)

            for i in range(256):
                xor_byte = ord(cipher_block[m - 1][-1])
                new_block = copy.copy(cipher_block)
                new_block.append(new_block[m])
                new_block[len(cipher_block) - 1] = '\xff' * 15 + chr(i)
                response = get_msg(''.join(new_block).encode('hex'))
                if "wrong" not in response:
                    c = 31 ^ i ^ xor_byte
                    _secret += chr(c)
                    print 'Secret = ', _secret
                    break

    return _secret


def get_flag():
    wanted = get_secret()
    message = wanted[:8] + wanted[12:]
    r = requests.get(URL + "test?msg=" + message)
    return get_msg(r.text)


print get_flag()
