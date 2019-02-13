"""KAS - semestrální práce - 2. úloha - Hamming (8,4)"""
import argparse

def readfile(file):
    new = ''
    with open(file, 'r', encoding="utf-8") as data:
        data = data.read()
    for d in data:
        if ord(d) > 127:
            new += '_'
        else:
            new += d
    return new

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def makeHam(data, mode):
    new_bits = ''
    x = ''
    o = ''
    for c in data:
        int_value = text_to_bits(c)
        for bit in int_value:
            x += bit
            if len(x) == 4096:
                #print("POZOR!")
                #print(len(x))
                crc = myCRC(x)
                crc = bin(int(crc, 16))[2:]
                #print(len(crc))
                j = ''
                p = ''
                for n in crc:
                    p += n
                    if(len(p) == 4):
                        j += toHamming(p)
                        p = ''
                o = ''
                for c in x:
                    o += c
                    if(len(o) == 4):
                        new_bits += toHamming(o)
                        o = ''
                tmpMainCode(new_bits, mode, j)
                new_bits = ''
                x = ''

    crc2 = myCRC(x)
    crc2 = bin(int(crc2, 16))[2:] 
    for c in x:
        o += c
        if(len(o) == 4):
            new_bits += toHamming(o)
            o = ''
    o = ''
    j = ''
    for n in crc2:
        o += n
        if(len(o) == 4):
            j += toHamming(o)
            o = ''
    tmpMainCode(new_bits, mode, j)

def toHamming(bits):
    p1 = parity(bits, [0,1,3])
    p2 = parity(bits, [0,2,3])
    p3 = parity(bits, [1,2,3])
    p = parity(p1 + p2 + bits[0] + p3 + bits[1:], [0,1,2,3,4,5,6])
    return p1 + p2 + bits[0] + p3 + bits[1:] + p

def parity(string, indicies):
    sub = ''
    for i in indicies:
        sub += string[i]
    return str(str.count(sub, "1") % 2)

def myCRC(msg):
    table = crc_table()
    crc32_value = 0xffffffff
    for ch in msg:
        lookup_index = (int(ch, 2) ^ crc32_value) & 0xff
        crc32_value = table[lookup_index] ^ (crc32_value >> 8)

    return hex(crc32_value ^ 0xFFFFFFFF)

def crc_table():
    table = []
    for byte in range(256):
        crc = 0
        for bit in range(8):
            if (byte ^ crc) & 1:
                crc = (crc >> 1) ^ 0x04C11DB7
            else:
                crc >>= 1
            byte >>= 1
        table.append(crc)
    return table

def tmpMainCode(msg, mode, crc):
    if(mode == '0'):
        printToFile(msg, crc)
        #print(msg)
        #print('len msg v tmpmaincode')
        #print(len(msg))
        #print(crc)
        #print("len crc v tmpmaincode")
        #print(len(crc))
    elif(mode == '1'):
        print(msg)
        print(crc)

def printToFile(msg, crc):
    msg = int(msg, 2).to_bytes((len(msg) + 7) // 8, 'big')
    crc = int(crc, 2).to_bytes((len(crc) + 7) // 8, 'big')

    with open(args.output, 'ab') as f:
        f.write(msg)
        f.write(crc)

def loadAndParseFile(file, mode):
    with open(file, 'rb') as f:
        data = f.read()
    msg = ''.join(format(byte, '08b') for byte in data)
    decoded = decode(msg)
    block = ''
    msg = ''
    result = ''
    tmp = ''
    for c in decoded:
        block += c
        if((len(block)) == 4128):
            tmp = ''
            crc = block[-32:]
            msg = block[:-32]
            newCRC = myCRC(msg)
            newCRC = bin(int(newCRC, 16))[2:]
            n = int(msg, 2)
            tmp += n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
            if(crc == newCRC):
                print('shoda')
                result += tmp
            else:
                print('crc !=')
                result+= "0"
            block = ''

    tmp = ''        
    crc = block[-32:]
    msg = block[:-32]
    n = int(msg, 2)
    tmp += n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
    #print(result)
    newCRC = myCRC(msg)
    newCRC = bin(int(newCRC, 16))[2:]
    
    if(crc == newCRC):
        print('shoda')
        result += tmp
    else:
        print('crc !=')
        result+= "0"

    if mode == "0":
        with open(args.output, "w") as f:
            f.write(result)
    else:
        print(result)
def decode(msg):
    decoded = ''
    while len(msg) >= 8:
        nibble = msg[0:8]
        nibble = fromHamming(nibble)
        if nibble != None:
            decoded += nibble
        else:
           return None
        msg = msg[8:] 
    return decoded

def fromHamming (bits):
    G = ['00000000', '11010010', '01010101', '10000111',
        '10011001', '01001011', '11001100', '00011110', 
        '11100001', '00110011', '10110100', '01100110', 
        '01111000', '10101010', '00101101', '11111111']
    for code in G:
        hamm1 = [int(k) for k in bits]
        hamm2 = [int(k) for k in code]
        diff = []
        i = 0
        while i < 8: 
            if hamm1[i] != hamm2[i]:
                diff.append(i+1)
            i += 1
        if len(diff) == 0: 
            return bits[2] + bits[4] + bits[5] + bits[6]
        if len(diff) == 1:
            print("1 chyba, mozna oprava")
            return code[2] + code[4] + code[5] + code[6]
        if len(diff) == 2:
            print("2 chyby ve 4 bitech")
            return None
    print("3 nebo vice chyb ve 4 bitech")
    return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hamming (8,4)')
    parser.add_argument('choice', help="k = kodovaci rezim, d = dekodovaci rezim")
    parser.add_argument('file', help="soubor pro nacteni")
    parser.add_argument('output', nargs='?', help="Optional. zadavejte soubor pro vypis, jinak nechte volny pro stdout")
    args = parser.parse_args()
    #mode 0 = byl zadan soubor, 1 = vystup jde na stdout
    if(args.choice == 'k'):
        file = args.file
        data = readfile(args.file)
        if(args.output):
            makeHam(data, "0")
        else:
            makeHam(data, "1")
    elif(args.choice == 'd'):
        file = args.file
        if(args.output):
            loadAndParseFile(file, "0")
        else:
            loadAndParseFile(file, "1")
    else:
        print('chybne zadany parametr| k = kodovat, d = dekodovat')
 