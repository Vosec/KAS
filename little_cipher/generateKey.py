"""velikost klíče je generována náhodně"""
import string
from random import randint
from random import shuffle

ALPHABET = string.ascii_letters
ALPHABET += string.digits
ALPHABET += ' '
ALPHABET += '\\'

def generateKey():
    n = randint(1,255)
    print(n)
    res = ''
    alph = list(ALPHABET)
    for x in range(n):
        shuffle(alph)
        res += ''.join(alph)

    with open('key.txt', 'w') as f:
        f.write(str(n))
        f.write('?')
        f.write(res)

if __name__ == '__main__':
    generateKey()