"""KAS - semestrální práce - 3. úloha - šifrování"""
"""Klíč je generován souborem generateKey.py"""
import argparse
import string
import numpy as np
import re

ALPHABET = string.ascii_letters
ALPHABET += string.digits
ALPHABET += ' '
ALPHABET += '\\'

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def readfile(file):
    bckslash = "\\"
    with open(file, 'r', encoding="utf-8") as f:
        data = f.read()
    chars = ''
    for d in data:
        if ord(d) > 127:
            d = '_'
        if d not in ALPHABET:
            bckslash += hex(ord(d))
            chars += bckslash
            bckslash = "\\"
        else:
            chars += d
    return chars

def getKeys():
    with open(args.key, 'r') as f:
        key = f.read()
    key = key.split("?")
    num = key[0]
    key = key[1]
    key = list(key)
    keys = np.reshape(np.array(key), (-1,64))
    return keys, num

def cypherText(msg):
    keys, num = getKeys()
    index = 0
    res = ''
    for char in msg:
        if(index == int(num)):
            index = 0
        c = ALPHABET.find(char)
        res += keys[index][c]
        index+=1

    if(args.output):
        print(res)
        with open(args.output, 'w') as f:
            f.write(res)
    else:
        print(res)
def loadAndDecode(file):
    keys, num = getKeys()
    with open(file, 'r') as f:
        data = f.read()
    res = ''
    index = 0
    for c in data:
        if(index == int(num)):
            index = 0
        r = keys[index][:]
        r = r.tolist()
        r = r.index(c)
        res += ALPHABET[r]
        index +=1
    
    hexa = re.findall(r'\\0x[0-9A-F]+', res, re.I)
    for h in hexa:
        tmp = h[1:5]
        short = h[1:4]
        if ((int(tmp,16)) > 127 and (int(short,16)) == 10):
            ok = short
        elif (int(tmp, 16) > 127):
            ok = short
        else:
            ok = tmp

        new = chr(int(ok,16))
        tmp = ok
        ok = '\\'
        ok += tmp
        res = res.replace(ok,new)
    
    if(args.output):
        with open(args.output, 'w') as f:
            f.write(res)
    else:
        print(res)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Polyalph. cipher')
    parser.add_argument('choice', help="k = kodovaci rezim, d = dekodovaci rezim")
    parser.add_argument('key', help="soubor s klicem")
    parser.add_argument('file', help="soubor pro nacteni")
    parser.add_argument('output', nargs='?', help="Optional. zadavejte soubor pro vypis, jinak nechte volny pro stdout")
    args = parser.parse_args()
    if(args.choice == 'k'):
        file = args.file
        data = readfile(args.file)
        #print(data)
        if(args.output):
            cypherText(data)
        else:
            cypherText(data)
    elif(args.choice == 'd'):
        file = args.file
        if(args.output):
            loadAndDecode(file)
        else:
            loadAndDecode(file)
    else:
        print('chybne zadany parametr| k = kodovat, d = dekodovat')
 