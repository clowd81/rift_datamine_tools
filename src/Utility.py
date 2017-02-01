import struct

def FNV1Hash(filename):
    """
    FNV hash a filename to be used to find it's ID in the manifest
    """
    
    FNV1_32_INIT = 0x811c9dc5
    FNV1_PRIME_32 = 16777619

    lowerName = filename.lower()
    
    _hash = FNV1_32_INIT
    uint32_max = 2 ** 32
    
    for c in lowerName:
        _hash = (_hash * FNV1_PRIME_32) % uint32_max
        _hash = _hash ^ ord(c)
    return format(_hash, 'x')


def readUnsignedLeb128(stream):
    result = 0
    i = 0
    index = 0
    currentByte = 0
    
    while i < 35:
        index = i
        i = i + 7
        cByte = stream.read(1)
        currentByte = ord(cByte)
        result |= (currentByte & 0x7f) << index
        signed = currentByte - 256 if currentByte > 127 else currentByte
        if signed > 0:
            return result
    return 0