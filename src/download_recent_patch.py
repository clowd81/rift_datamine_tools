import urllib2

import fnmatch
import os
import subprocess
import time

# Glyph log file location (Windows 10)
## MODIFY BELOW TO POINT TO YOUR GLYPH LOG DIRECTORY AND TO THE LOG FILE TO PARSE FOR DOWNLOADS! ##
glyph_log = "C:\\Users\\Kyle\\AppData\\Local\\Glyph\\Logs\\GlyphClient.2.log"

# Directory to download and extract assets
output_dir = "E:\\RIFT\\datamine\\apr28-pts-paks\\"

def download_patch():
    log = open(glyph_log)
    log_lines = log.readlines()

    if not os.path.exists(output_dir):
        print "Making directory: " + output_dir
        os.mkdir(output_dir)

    # Search the Glyph log indicated above for patch files to download
    for line in log_lines:
        if "Downloading from" in line:
            download_loc = line.split(' ')[4].rstrip()
            filename = download_loc.split('/')[-1:][0].split('?')[0].rstrip()

            print "Downloading from " + download_loc + " to " + output_dir + filename
            try:
                response = urllib2.urlopen(download_loc)
                data = response.read()

                f = open(output_dir + filename, "wb")
                f.write(data)
                f.close()
            except:
                print "failed to download " + download_loc

    log.close()

# Quick BMS file locations
## MODIFY BELOW TO POINT TO THE QUICKBMS EXECUTABLE ##
quickbms_dir = "E:\\RIFT\\quickbms\\"

quickbms_exe = quickbms_dir + "quickbms.exe"
quickbms_riftlzma = quickbms_dir + "riftlzma2.bms"
quickbms_riftpak = quickbms_dir + "riftpak.bms"

def extract_lzma2():
    asset_files = os.listdir(output_dir)

    # decompress lzma2 files into pak files
    for asset in asset_files:
        if (asset[-5:] == "lzma2") and ("physics" not in asset):
            asset_path = output_dir + asset
            print "Extrating assets from " + asset_path + " to " + output_dir
            proc = subprocess.Popen([quickbms_exe, quickbms_riftlzma, asset_path, output_dir])
            time.sleep(5)
            proc.terminate()

def extract_pak():
    asset_files = os.listdir(output_dir)

    # Extract PAK files into folders
    for asset in asset_files:
        if asset[-3:] == "pak":
            asset_path = output_dir + asset
            output_path = output_dir +  asset.split('.')[0]
            if not os.path.exists(output_path):
                print "Making directory: " + output_path
                os.mkdir(output_path)
            print "Extrating assets from " + asset_path + " to " + output_path
            proc = subprocess.Popen([quickbms_exe, quickbms_riftpak, asset_path, output_path])
            time.sleep(15)
            proc.terminate()

def nif_try_rename(filename):
    file_size = os.path.getsize(filename)
    nif_file = open(filename, "rb")

    nif_file_start = nif_file.read(2048)
    nif_creation_info = nif_file_start.find('NIF Creation Information')
    nif_texture_info = nif_file_start.find('.dds')
    nif_filename = None

    if (nif_creation_info > 0):
        nif_creation_start = nif_creation_info + 28
        nif_creation_end = nif_file_start.find('.ma')
        nif_filename = nif_file_start[nif_creation_start:nif_creation_end].split('/')[-1]

    if (nif_texture_info > 0 and ((nif_filename == None) or (nif_filename == "partBatch_temp"))):
        nif_texture_end = nif_texture_info
        nif_texture_start = nif_file_start.rfind('\00', 0, nif_texture_end) + 1
        nif_filename = nif_file_start[nif_texture_start:nif_texture_end]

    nif_file.close()

    if (nif_filename != None):
        rename = filename[:-12] + nif_filename + '_' + filename[-12:] + '.nif'

        print "Renaming nif file: " + filename + " to " + nif_filename + '.nif'

        os.rename(filename, rename)
        return True

    return False

def rename_nif_files():
    nif_files = []
    for root, dirnames, filenames in os.walk(output_dir):
        for filename in fnmatch.filter(filenames, '0*.nif'):
            nif_filename = os.path.join(root, filename)
            nif_try_rename(nif_filename)

download_patch()
extract_lzma2()
extract_pak()
rename_nif_files()

print "Done!"
