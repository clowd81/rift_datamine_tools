from LittleEndianDataInputStream import LittleEndianDataInputStream

import binascii
import os
import zlib
import Utility
from _ctypes import ArgumentError

class AssetDatabase(object):
    def __init__(self, riftDir):
        # TODO: Check 32/64 manifests
        self.assetsManifest64 = "assets64.manifest"
        self.manifest = Manifest(os.path.join(riftDir, self.assetsManifest64))
        self.assetsDir = os.path.join(riftDir, "assets\\")
        self.assets = []

        for file in os.listdir(self.assetsDir):
            asset = AssetFile(self.manifest, os.path.join(self.assetsDir, file))
            self.assets.append(asset)

    def getAllAssets(self):
        assetList = []
        for af in self.assets:
            for ae in af.getassets():
                assetList.append(ae)
        return assetList

    def extractByAsset(self, assetEntry, filename):
        """extract the given entry to the given filename"""
        af = self.getAssetFileByEntry(assetEntry)
        if af == None:
            raise Exception("Could not find asset file for asset id: " + assetEntry.entryIDstr)
        af.extractByEntry(assetEntry, filename)

    def extractByName(self, assetFilename, filename):
        """extract the asset with the given filename to the file given filename"""
        af = self.getAssetFileByName(assetFilename)
        if af == None:
            raise Exception("Could not find asset file for asset " + assetFilename)
        af.extractByName(assetFilename, filename)

    def getAssetByFilename(self, filename):
        """ get information about the asset for the given file """
        _hash = Utility.FNV1Hash(filename)
        for af in self.assets:
            if af.hasNameHash(_hash):
                return af.getAssetByNameHash(_hash)
        return None;

    def getAssetFileByName(self, filename):
        """Get the asset file that contains the file """
        _hash = Utility.FNV1Hash(filename)
        for af in self.assets:
            if af.hasNameHash(_hash):
                return af
        return None;
        
    def getAssetFileByEntry(self, entry):
        """Get the asset file that contains the file by its entry"""
        for af in self.assets:
            if af.hasID(entry.entryIDstr):
                return af
        return None;

    def getAssetFileByID(self, _id):
        """Get the asset file that contains the file by its id"""
        for af in self.assets:
            if af.hasID(_id):
                return af
        return None;

class AssetEntry(object):
    """ An entry in the asset file """
    def __init__(self, entryID, offset, size1, size2, filenum, flag, _hash, nameHash):
        self.entryID = entryID;
        self.entryIDstr = str(binascii.hexlify(entryID), 'ascii')
        self.nameHash = nameHash
        self.offset = offset;
        self.size = size1;
        self.sizeD = size2;
        self.compressed = flag > 0
        self._hash = _hash
        
    
class AssetFile(object):
    """ an asset file, eg, asset.001 """
    def __init__(self, manifest, assetFilename):
        self.assetName = ""
        self.assetIDEntryMap = {}
        self.assetNameHashEntryMap = {}

        self.assetName = assetFilename
        self.process(manifest, assetFilename)
    
    def getassets(self):
        return self.assetIDEntryMap.values();
    
    def extractByEntry(self, entry: AssetEntry, destinationFile):
        with open(self.assetName, "rb") as f:
            f.seek(entry.offset)
            data = f.read(entry.size)
            with open(destinationFile, "wb") as output:
                if entry.compressed:
                    output.write(zlib.decompress(data)) 
                else:
                    output.write(data) 
    def extractByName(self, filename, destinationFile):
        _hash = Utility.FNV1Hash(filename)
        self.extractByEntry(self.assetNameHashEntryMap[_hash], destinationFile)   
    def extractByNameHash(self, _hash, destinationFile):
        self.extractByEntry(self.assetNameHashEntryMap[_hash], destinationFile)   
    
    def getAssetByNameHash(self, _hash):
        return self.assetNameHashEntryMap[_hash]
    
    def hasID(self, _id):
        return _id in self.assetIDEntryMap

    def hasNameHash(self, _hash):
        return _hash in self.assetNameHashEntryMap
        
    def process(self, manifest, assetFilename):
        with open(assetFilename, "rb") as f:
            dis = LittleEndianDataInputStream(f)
            
            magicMarker = f.read(4).decode("utf-8") 
            if magicMarker != 'TWAD':
                raise Exception("Invalid magic marker, expected TWAD got '" + magicMarker + "'")
        
            version = dis.read_int();
            headersize = dis.read_int()
            maxfiles = dis.read_int()
            files = dis.read_int()   
            
            # For some reason, using the "files" variable doesnt read the proper amount of actual files, deleted? renamed? moved?
            for i in range(0, maxfiles):
                entryID = f.read(8)
                
                offset = dis.read_int()
                size1 = dis.read_int()
                size2 = dis.read_int()
                filenum = dis.read_short()
                flag = dis.read_short() # compressed
                _hash = f.read(20)
                entryIDstr = str(binascii.hexlify(entryID), 'ascii')
                # sometimes a id doesn't exist in the manifest.. not sure why?
                if offset > 0:
                    try:
                        nameHash = manifest.nameforid(entryIDstr)
                        entry = AssetEntry(entryID, offset, size1, size2, filenum, flag, _hash, nameHash)
                        self.assetIDEntryMap[entryIDstr] = entry
                        self.assetNameHashEntryMap[nameHash] = entry
                    except KeyError:
                        #print("No name to match for asset " + entryIDstr)
                        pass
                    
                    
        
class Manifest(object):
    '''
    classdocs
    '''
 

    def __init__(self, assetManifestFilename):
        self.nameEntryDict = {}
        self.entryNameDict = {}
        self.process(assetManifestFilename)
       
    def nameforid(self, _id):
        return self.entryNameDict[_id]
    
    def process(self, assetsManifest32):
        with open(assetsManifest32, "rb") as f:
                dis = LittleEndianDataInputStream(f)
                
                magicMarker = f.read(4).decode("utf-8") 
                if magicMarker != 'TWAM':
                    raise Exception("Invalid magic marker, expected TWAM got '" + magicMarker + "'")
                    
                majorV = dis.read_unsigned_short()
                minorV = dis.read_unsigned_short()
                print("Manifest version: " + str(majorV) + "." + str(minorV))
                
                unknown = f.read(24)
                tableOffset = dis.read_int()
                unknown_2 = dis.read_int()
                count = dis.read_int()
                
                print("Manifest entries:" + str(count))
                
                
                # each manifest entry is 56 bytes but we only actually read the first 12, we don't know what the rest are
                entrySize = 56;
                for i in range(0, count):
                    start = tableOffset + (i * entrySize)
                    f.seek(start)
    
                    entryID = f.read(8)
                    filenameHashO = f.read(4)
                    filenameHash = bytes([ filenameHashO[3], filenameHashO[2], filenameHashO[1], filenameHashO[0] ])
                    
                    entryIDstr = str(binascii.hexlify(entryID), 'ascii')
                    filenameHashStr = str(binascii.hexlify(filenameHash), 'ascii')
                    
                    self.nameEntryDict[filenameHashStr] = entryIDstr  
                    self.entryNameDict[entryIDstr] =   filenameHashStr