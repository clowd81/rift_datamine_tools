import ctypes
import sqlite3
import os
from Assets import AssetDatabase
import ntpath
import pyffi.formats.nif
from Asset_LangCDS import LangCDS
from _io import BytesIO, StringIO
from Utility import readUnsignedLeb128

def nifTextures(niffile):
    """Open the given NIF file and return the DDS textures referenced in it"""
    textures = [];
    stream = open(niffile, 'rb')
    data = pyffi.formats.nif.NifFormat.Data()
    try:
        data.read(stream)
        for s in data._string_list:
            ss = s.decode('UTF-8')
            if ss.endswith("dds"):
                textures.append(ss)
    except:
        print("Could not read textures in file: ", niffile)
    return textures
    
def nifPath(niffile):
    """Open the given NIF file and to get the pathname"""
    stream = open(niffile, 'rb')
    data = pyffi.formats.nif.NifFormat.Data()
    try:
        data.read(stream)
        for s in data._string_list:
            ss = s.decode('UTF-8')
            if ss.startswith("NIF Creation Information"):
                return ss.split(">>")[1].strip()
    except:
        print("Could not rename file: ", niffile)
        
    return ""
    
def nifName(niffile):
    """ try to guess the name from the nif file"""
    return ntpath.basename(os.path.splitext(nifPath(niffile))[0] + '.nif')

def extractAndDecryptTelaraDB(db):
    db.extractByName("telara.db", "telara.db") 
    os.system("decrypt_telaradb.exe")   # now decrypt it into a file called 'telara_decrypted.db'
    os.remove("telara.db")              # and cleanup
    
def extractUnencryptedTelaraDB(unencryptedDBFilename, extractDirectory):
    
    print("Begin extracting of " + unencryptedDBFilename)
    # load decompression DLL
    decompDLL = ctypes.CDLL("riftdecomp.dll")

    conn = sqlite3.connect(unencryptedDBFilename)
    conn.row_factory = sqlite3.Row
    ds = conn.cursor()
    
    # DatasetID appears to be a "category" of sorts, with the datasetkey being subcategories
    # For example, dataset 7701 has different keys for different languages.
    # Guesses at some randomly chosen dataset id contents:
    # 83 - ability formulas
    # 84 - worlds? contains NIF references
    # 111 - Scene?
    # 114 - sound bank reference
    # 4307 - profanity block?
    # 7701 - EULA
    
    # In test mode only the first row for each datasetid will be extracted, disable it to extract more than one row per datasetid
    ###############
    #
    # WARNING:    BE AWARE IF YOU DISABLE TEST MODE WITHOUT CHANGING THE SQL EURY YOU WILL PULL **EVERY RECORD** FROM THE DATABASE. 
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
        
        valueData = rowA['value']
        frequencyTable = freqRow["frequencies"] 
        
        buffer = BytesIO(valueData)
        
        uncompressedSize = readUnsignedLeb128(buffer)
        compressedSize = len(valueData) - buffer.tell()
    
        # create a buffer to decompress into
        inputData = buffer.read(compressedSize)
        outputData = ctypes.create_string_buffer(uncompressedSize)
        decompDLL.decompressData(frequencyTable, inputData, compressedSize, outputData, uncompressedSize)
    
        # write our new data to 
        f = open(os.path.join(extractDirectory + str(dsid) + "_" + str(dskey)), "wb")
        f.write(outputData)
        f.close()   

        dsc.close()

    ds.close()

    
    
   
if __name__ == '__main__':

    riftDir = "L:\\SteamStuff\\Steam2\\steamapps\\common\\rift\\"
    db = AssetDatabase(riftDir)
     
    extractDirectory = "telara_db_data\\"
    
    try:
        os.mkdir(extractDirectory)
    except FileExistsError:
        pass
    
    # Extract and decrypt telara, it will create a file called 'telara_decrypted.db'
    extractAndDecryptTelaraDB(db)
    extractUnencryptedTelaraDB('telara_decrypted.db', extractDirectory)
    # extract the lang cds to "cds.txt"
    #cds = LangCDS(db)

    # extract ALL the assets into a directory
    # No attempt is made to guess the name or extension
    #if False:
    #    try:
    #        os.mkdir("export")
    #    except FileExistsError:
    #        pass;
    #    for asset in db.getAllAssets():
    #        filename = asset.entryIDstr
    #        db.extractByAsset(asset, os.path.join("export/", filename))
    
    
    
    
    
    
    