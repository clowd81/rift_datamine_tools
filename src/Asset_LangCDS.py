from _io import BytesIO
from LittleEndianDataInputStream import LittleEndianDataInputStream
import ctypes
from Utility import readUnsignedLeb128

class LangCDS(object):
    def __init__(self, database, language="english", filename="english_lang_cds.txt"):
        self.database = database
        self.language = language
    
        # load decompression DLL
        decompDLL = ctypes.CDLL("riftdecomp.dll")
    
        stream = BytesIO()
        self.database.extractByNameToMemory("lang_" + language + ".cds", stream) 
        # seek to start
        stream.seek(0)
       
        dis = LittleEndianDataInputStream(stream)
        
        entryCount =  dis.read_int();
        
        # read the frequency table
        frequencyTable = stream.read(1024)
        
        print("entryCount:" + str(entryCount))  
        
        # not sure what these are
        for i in range(0, entryCount):
                key = stream.read(4)
                value = readUnsignedLeb128(stream)
        
        f = open(filename, "w", encoding='UTF-8')   
        
        for i in range(0, entryCount):   
            compressedSize = readUnsignedLeb128(stream)
            uncompressedSize = readUnsignedLeb128(stream)
            entryData = stream.read(compressedSize)
            
            # create a buffer to decompress into
            outputData = ctypes.create_string_buffer(uncompressedSize)
            # call a DLL to do the actual decompress. The ASM code to decompress was too complicated to reverse engineer, so I just
            # took the code and put it into a DLL 
            decompDLL.decompressData(frequencyTable, entryData, compressedSize, outputData, uncompressedSize)
            
            # And the results are in!
            
            # - The first 10 bytes we don't know, they seem to be the same between files though?
            buffer = BytesIO(outputData.raw)
            buffer.read(10)
            # - Then a LEB128 with length of string
            strLength = readUnsignedLeb128(buffer)
            # - Then string
            finalStringBytes = buffer.read(strLength)
            finalString = finalStringBytes.decode("utf-8")
            # print("doing entry: " + str(i) + ", length[" + str(strLength) + "]:" + finalString.encode(sys.stdout.encoding, errors="replace").decode(sys.stdout.encoding))
            
            print(finalString,file=f)
            
            
           
        f.close()    
        
    
