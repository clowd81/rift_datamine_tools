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
