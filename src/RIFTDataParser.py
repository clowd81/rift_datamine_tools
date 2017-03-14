'''
Created on 14Mar.,2017

'''
import os
from Utility import readUnsignedLeb128
from LittleEndianDataInputStream import LittleEndianDataInputStream

def log(sstr, indent):
    print(sstr.rjust(len(sstr) + indent))

class CodeResult(object):
    def __init__(self, _code, _data):
        self.code = _code
        self.data = _data
    def __str__(self):
        return "[" + str(self.code) + "][" + str(self.data) + "]";
        
class CodeResult2(object):
    def __init__(self, _code, _code2, _data):
        self.codeA = _code
        self.codeB = _code2
        self.count = _data
    def __str__(self):
        return "[" + str(self.codeA) + "][" + str(self.codeB) + "][" + str(self.count) + "]"        

def splitCode(cin):
    code = cin & 7
    data = cin >> 3
    if code == 7:
        data = cin >> 6
        v5 = (cin >> 3) & 7
        if v5 <= 4:
            code = v5 + 8
            return CodeResult(code, data)
    elif code <= 7:
        return CodeResult(code, data)
    return None

def readCodeAndExtract(stream, indent):
    value = readUnsignedLeb128(stream)
    if value == 0:
        return None
    codeResult = splitCode(value)
    log("READ result " + str(codeResult), indent)
    return codeResult

def readCodeThenReadTwice(stream, indent):
    value = readUnsignedLeb128(stream)
    if value == 0:
        return None
    
    codeResult = splitCode(value)
    if codeResult == None:
        return None
    codeA = codeResult.code
    codeResultB = splitCode(codeResult.data)
    codeB = codeResultB.code
    return CodeResult2(codeA, codeB, codeResultB.data)

def handleCode(stream, code, indent):
    
    if code == 0 or code == 1:
        log("handleCode:" + str(code) + ", boolean?", indent)
        log("bool? " + str(code), indent+1)
        return True
    if code == 2:
        #some kind of float/double. Can be UP to 80 bits long
        #IEEE 754 extended precision format maybe?
        log("handleCode:" + str(code) + ", (1)float/double?", indent)
        i = 1
        while stream.read_byte() < 0 and i < 10:
            i = i + 1

        return True
    if code == 3:
        #some kind of float/double. Can be UP to 80 bits long
        #IEEE 754 extended precision format maybe?
        log("handleCode:" + str(code) + ", (1)float/double?", indent)
        i = 1
        while stream.read_byte() < 0 and i < 10:
            i = i + 1
        return True
    if code == 4:
        log("handleCode:" + str(code) + ", int?", indent)
        log("int:" + str(stream.read_int()), indent+1)
        return True
    if code == 5:
        log("handleCode:" + str(code) + ", long?", indent)
        log("long:" + str(stream.read_long()), indent+1)
        return True
    if code == 6:
        log("handleCode:" + str(code) + ", string/data", indent)
        slen = readUnsignedLeb128(stream)
        sstr = stream.read_string(slen)
        log("string:" + sstr, indent+1)
        return True
    if code == 10 or code == 9:
        if code == 10:
            # a value then some kind of array?
            log("handleCode:" + str(code) + ", array?", indent)
            value = readUnsignedLeb128(stream)
            log ("value:" + str(value), indent+1)
            if value > 0xFFFF or value == 0:
                log("bad value code 10", indent+1)
                return False
        log("handleCode:" + str(code) + ", array2?", indent)
        
        while True:
            rr = readCodeAndExtract(stream, indent +1)
            if rr == None:
                break
            if rr.code == 8:
                return True
            if not handleCode(stream, rr.code, indent+1):
                break
        log("overrun while code 9", indent +1)
        return False
    if code == 11:
        log("handleCode:" + str(code) + ", array?", indent)
        result = readCodeAndExtract(stream, indent+1)
        if result == None:
            log("bad result code 11", indent+1)
            return False
        count = result.data
        if count == 0:
            return True
        i = 0
        log("handle array count[" + str(count) + "], startingCode[" + str(result.code) + "]", indent+1)
        while (handleCode(stream, result.code, indent+1)):
            i = i + 1
            if (i >= count):
                return True
        log("overrun while code 11", indent +1)
        return False
    if code == 12:
        log("handleCode:" + str(code) + ", array3?", indent)
        result = readCodeThenReadTwice(stream, indent +1)
        
        count = result.count
        if count == 0:
            return True
        i = 0
        log("handle Multidimensional array?:" + str(result), indent+1)
        while (handleCode(stream, result.codeA, indent+1) and handleCode(stream, result.codeB, indent+1)):
            i = i + 1
            if (i >= count):
                return True
        log("overrun while code 12", indent +1)
        return False
            
    if code == 8:
        log("handleCode:" + str(code) + ", end of object", indent)
        return False
    
    log("UNKNOWN CODE:" + str(code))
    exit(1)
        

def parse(file):
    file = open(file, "rb")

    stream = LittleEndianDataInputStream(file) 
    
    classCode = readUnsignedLeb128(stream)
    print ("Found class code:", classCode)
    
    i = 1
    done = False
    
    while not done:
        print("do member " + str(i))
        codeResult = readCodeAndExtract(stream, 1)
        done = not handleCode(stream, codeResult.code, 1)
        i = i+1
    file.close()
    





if __name__ == '__main__':
    parse("D:\\rift_stuff\\_unk_map1\\0011b0bb._unk_map1")