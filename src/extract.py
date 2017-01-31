import os
from Assets import AssetDatabase
import ntpath
import pyffi.formats.nif

def nifTextures(niffile):
    """Open the given NIF file and return the DDS textures referenced in it"""
    textures = [];
    stream = open(niffile, 'rb')
    data = pyffi.formats.nif.NifFormat.Data()
    data.read(stream)
    for s in data._string_list:
        ss = s.decode('UTF-8')
        if ss.endswith("dds"):
            textures.append(ss)
    return textures
def nifPath(niffile):
    """Open the given NIF file and to get the pathname"""
    stream = open(niffile, 'rb')
    data = pyffi.formats.nif.NifFormat.Data()
    data.read(stream)
    for s in data._string_list:
        ss = s.decode('UTF-8')
        if ss.startswith("NIF Creation Information"):
            return ss.split(">>")[1].strip()
    return ""
def nifName(niffile):
    """ try to guess the name from the nif file"""
    return ntpath.basename(os.path.splitext(nifPath(niffile))[0] + '.nif')
    

if __name__ == '__main__':
    riftDir = "L:\\SteamStuff\\Steam2\\steamapps\\common\\rift\\"
    
    # extract a file
    db = AssetDatabase(riftDir) 
    db.extractByName("crucia.nif", "crucia.nif")
    
    
    # extract ALL the assets into a directory
    # No attempt is made to guess the name or extension
    if False:
        try:
            os.mkdir("export")
        except FileExistsError:
            pass;
        for asset in db.getAllAssets():
            filename = asset.entryIDstr
            db.extractByAsset(asset, os.path.join("export/", filename))
    
    
    
    
    
    
    
    