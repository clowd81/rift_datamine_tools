import ctypes
import sqlite3
import os
from _io import BytesIO
from Utility import readUnsignedLeb128
 # load decompression DLL
decompDLL = ctypes.CDLL("riftdecomp.dll")


def extractAndDecryptTelaraDB(db):
    db.extractByName("telara.db", "telara.db") 
    os.system("decrypt_telaradb.exe")   # now decrypt it into a file called 'telara_decrypted.db'
    os.remove("telara.db")              # and cleanup

def decompress(frequencyTable, valueData):
    buffer = BytesIO(valueData)
    uncompressedSize = readUnsignedLeb128(buffer)
    compressedSize = len(valueData) - buffer.tell()
    # create a buffer to decompress into
    inputData = buffer.read(compressedSize)
    outputData = ctypes.create_string_buffer(uncompressedSize)
    decompDLL.decompressData(frequencyTable, inputData, compressedSize, outputData, uncompressedSize)
    return BytesIO(outputData.raw)
    
def extractFromUnencryptedTelaraDB(unencryptedDBFilename, extractDirectory):
    
    print("Begin extracting of " + unencryptedDBFilename)
   

    conn = sqlite3.connect(unencryptedDBFilename)
    conn.row_factory = sqlite3.Row
    ds = conn.cursor()
    
    # DatasetID appears to be a "category" of sorts, with the datasetkey being subcategories
    # For example, dataset 7701 has different keys for different languages.
    # Guesses at some randomly chosen dataset id contents:
    # 83 - ability formulas
    # 84 - worlds? contains NIF references
    # 111 - Scene cubemaps (environment)
    # 113 - scene sounds
    # 114 - sound bank reference
    # 2204 - achievments?
    # 4087 - promotions?
    # 4307 - profanity block?
    # 7304 - pointers to HKX (havok collision data)
    # 7305 - points to NIF files - terrain
    # 7701 - EULA
    
    # In test mode only the first row for each datasetid will be extracted, disable it to extract more than one row per datasetid
    ###############
    #
    # WARNING:    BE AWARE IF YOU DISABLE TEST MODE WITHOUT CHANGING THE SQL QUERY YOU WILL PULL **EVERY RECORD** FROM THE DATABASE. 
    # WARNING:    THERE ARE 400,000+ AND MOST ARE UNDER 1KB.BE AWARE THAT your filesystem might not appreciate 400,000 1KB files suddenly appearing
    # WARNING:    You may wish to filter the first query by a specific datasetId, eg:
    # WARNING:    ds.execute('SELECT * from dataset where datasetId=?', (7701,))
    #
    ###############    
    TEST_MODE = True
    test_mode_ids = set()  

    ds.execute('SELECT * from dataset order by length(value) desc')
    while (1) :
        rowA = ds.fetchone()
        if rowA == None:
            break;

        dsc = conn.cursor()
        
        dsid = rowA["datasetId"]
        dskey = rowA["datasetKey"]
        dsname = rowA["name"] # some entries have a "name" that can be useful to identify, but often have funny characters in them so we can't use them directly

        if TEST_MODE:
            if dsid in test_mode_ids:
                continue
            test_mode_ids.add(dsid)
        
        dsc.execute("select * from dataset_compression where datasetid= ?", (dsid,) )
        freqRow = dsc.fetchone()
        if freqRow is not None:
            print ("found compression table, decompressing")
            valueData = rowA['value']
            frequencyTable = freqRow["frequencies"] 
            outputData = decompress(frequencyTable, valueData)
        else :
            outputData = rowA['value']
    
        # write our new data to 
        f = open(os.path.join(extractDirectory + str(dsid) + "_" + str(dskey)), "wb")
        outputData.seek(0)
        f.write(outputData.read())
        f.close()   

        dsc.close()

    ds.close()

if __name__ == '__main__':
    extractFromUnencryptedTelaraDB('telara_decrypted.db', "")
    