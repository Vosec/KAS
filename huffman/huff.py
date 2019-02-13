"""KAS - semestrální práce - 1. úloha - Huffman"""
import argparse
import operator
from collections import OrderedDict
import re
#str to dict
import ast
def readfile(soubor):
    """čistě načte soubor a zbavý se písm>127 ascii"""
    x = ''
    with open(soubor, 'r', encoding="utf-8") as data:
        data = data.read()
    for d in data:
        if ord(d) > 127:
            x += '_'
        else:
            x += d
    return x

def makeDict(data):
    """Vytvoreni slovniku"""
    tmp = {}
    for item in data:
        if str(item) in tmp:
            tmp[str(item)] = tmp[str(item)] + 1
        else:
            tmp[str(item)] = 1
    tmp = sorted(tmp.items(), key=operator.itemgetter(1))
    return tmp

def codeHuff(probDict):
    """Zakodovani zpravy pomoci huffmana"""   
    tmp = probDict
    result = []
    tab = {}
    while len(tmp) > 2:
        last = tmp.pop(0)
        prelast = tmp.pop(0)
        tab = makeTable(last,prelast,tab)
        item = (last[0]+prelast[0],last[1]+prelast[1])
        tmp.append(item)
        tmp = sorted(tmp, key=operator.itemgetter(1))
        result.append(tmp)
    last = tmp.pop(0)
    prelast = tmp.pop(0)
    makeTable(last,prelast,tab)
    return tab

def makeTable(last,prelast,tab):
    """vytvoreni tabulky"""
    for k in list(last[0]):
        if k in tab:
            tab[k] = '0' + tab[k]
        else:
            tab[k] = '0'
    for k in list(prelast[0]):
        if k in tab:
            tab[k] = '1' + tab[k]
        else:
            tab[k] = '1'
    return tab

def makeFreq(data, mode):
    """Ziskani frekvenci znaku ze souboru"""
    probDict = {}
    countChar = 0
    newData = ''
    i = 0
    for c in data:
        if c not in probDict:
            probDict[c] = 1
            countChar += 1
            newData += c 
        else:
            probDict[c] += 1
            newData += c
        if(i == 8192):
            i=-1
            for key, val in probDict.items():
                tmp = val/countChar
                probDict[key] = tmp
            probDict = OrderedDict(sorted(probDict.items(), key=lambda x: x[1], reverse=True))
            tmpMainCode(probDict,mode, newData)
            probDict = {}
            countChar = 0
            newData = ''
        i = i + 1
    for key, val in probDict.items():
        tmp = val/countChar
        probDict[key] = tmp
    probDict = OrderedDict(sorted(probDict.items(), key=lambda x: x[1], reverse=True))
    tmpMainCode(probDict, mode, newData)

def encode(data,huff_dict):
    """encodovani"""
    compressed = ''
    for item in data:
        compressed += huff_dict[str(item)]
    return compressed

def msgToByte(compressed):
    """Padding, pridani 0 na konec v pripade nebytove zpravy"""
    count = 0
    if((len(compressed))%8 == 0):
        return compressed, count
    else:
        while((len(compressed))%8 != 0):
            compressed += "0"
            count += 1
    return compressed, count

def loadAndParseFile(file, mode):
    with open(file, 'rb') as f:
        data = f.read()
    bigsplit = re.split(b"\x1C\xF3\xF2\xB2\xE7", data)
    for item in bigsplit:
        if (item):
            tmp =  re.split(b'\xe1\xED', item)
            x = str(tmp[0].decode('ascii'))
            duff = ast.literal_eval(x)
            count = tmp[1]
            codedMsg = tmp[2]
            msg = ''.join(format(byte, '08b') for byte in codedMsg)
            if(int(count)>0):
                msg = msg[:-int(count)]  
            decode(duff, str(msg), mode)    

def decode(myDict, msg, mode):
    """Dekodovani zpravy"""
    word = ''
    result = ''
    for item in msg:
        word += str(item)
        if str(word) in myDict.values():
            result += list(myDict.keys())[list(myDict.values()).index(word)] 
            word = ''
    if mode == '0':
        with open(args.output, 'a') as f:
            f.write(result)
    else:
        print(result)

def printToFile(outFile, msg, freq, count):
    """vypis do souboru"""
    int_value = int(msg, 2).to_bytes((len(msg) + 7) // 8, 'big')
    c = int('00011100', 2).to_bytes((len('11101001') + 7) // 8, 'big')
    x = int('11110011', 2).to_bytes((len('11110011') + 7) // 8, 'big')
    y = int('11110010', 2).to_bytes((len('11110010') + 7) // 8, 'big')
    z = int('10110010', 2).to_bytes((len('10110010') + 7) // 8, 'big')
    w = int('11100111', 2).to_bytes((len('11100111') + 7) // 8, 'big')
    with open(outFile, 'a') as f:
        f.write(str(freq))
        f.write('á')
        f.write('í')
        f.write(str(count))
        f.write('á')
        f.write('í')
    with open(outFile, 'ab') as f:
        f.write(int_value)
        f.write(c)
        f.write(x)
        f.write(y)
        f.write(z)
        f.write(w)

def tmpMainCode(freq,mode, newData):
    duff = codeHuff(makeDict(freq))
    compressed = encode(newData,duff) 
    msgByte, count = msgToByte(compressed)
    if(mode == '0'):
        printToFile(args.output, msgByte, duff, count)
    elif(mode == '1'):
        print(duff)
        int_value = int(msgByte, 2).to_bytes((len(msgByte) + 7) // 8, 'big')
        print(int_value)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Huffman')
    parser.add_argument('choice', help="k = kodovaci rezim, d = dekodovaci rezim")
    parser.add_argument('file', help="soubor pro nacteni")
    parser.add_argument('output', nargs='?', help="Optional. zadavejte soubor pro vypis, jinak nechte volny pro stdout")
    args = parser.parse_args()
    #mode 0 = byl zadan soubor, 1 = vystup jde na stdout
    if(args.choice == 'k'):
        file = args.file
        data = readfile(args.file)
        if(args.output):
            makeFreq(data, "0")
        else: 
            makeFreq(data,'1')
    elif(args.choice == 'd'):
        file = args.file
        if(args.output):
            loadAndParseFile(file, "0")
        else:
            loadAndParseFile(file, "1")
    else:
        print('chybne zadany parametr| k = kodovat, d = dekodovat')
 