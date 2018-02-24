import Assets
import os
from extract import *

### RENAME THESE PATHS TO POINT TO THE CORRECT FILE OR DIRECTORY ON YOUR SYSTEM! ###
rift_dir = "E:\\RIFT\\PTS\\"
#rift_dir = "C:\\Program Files (x86)\\Glyph\\Games\\RIFT\\Live\\"
glyph_log = "C:\\Users\\Kyle\\AppData\\Local\\Glyph\\Logs\\GlyphClient.0.log"
output_dir = "E:\\RIFT\\datamine\\feb23-pts\\"

asset_db = Assets.AssetDatabase(rift_dir)

def extract_nif_textures(nifFilename, output_dir):
    for texture in nifTextures(nifFilename):
        output_file = output_dir + texture
        try:
            asset_db.extractByName(texture, output_file)
        except:
            print("    could not find texture: ", texture)

def rename_partbatch_nif(filename):
    """
    partbach files are often armor, weapon, and costume models.  Let's extract
    the model's primary texture to use as a name.
    """
    nif_file = open(filename, "rb")

    nif_file_start = str(nif_file.read(4096))
    nif_creation_info = nif_file_start.find('NIF Creation Information')
    nif_texture_info = nif_file_start.find('.dds')
    nif_filename = ""

    if (nif_texture_info > 0):
        nif_texture_end = nif_texture_info
        nif_texture_start = nif_file_start.rfind('\\x00', 0, nif_texture_end) + 4
        nif_filename = nif_file_start[nif_texture_start:nif_texture_end-2]

    nif_file.close()

    return nif_filename

def rename_file_by_type(filename):
    if os.path.exists(filename):
        f = open(filename, "rb")
        start_data = str(f.read(32))
        f.close()

        if 'Gamebryo File Format' in start_data:
            # NIF Files.  Extract the most appropriate name
            nifFilename = nifName(filename)

            rename = filename + "_" + nifFilename

            if "partBatch_temp" in nifFilename:
                rename = filename + "_" + rename_partbatch_nif(filename) + ".nif"

            if not os.path.exists(rename):
                os.rename(filename, rename)

            extract_nif_textures(rename, filename[:filename.rfind('\\')] + "\\")
        elif 'DDS' in start_data:
            rename = filename + ".dds"

            if not os.path.exists(rename):
                os.rename(filename, rename)
        elif 'Exif' in start_data:
            rename = filename + ".jpg"

            if not os.path.exists(rename):
                os.rename(filename, rename)

def extract_patch():
    log = open(glyph_log)
    log_lines = log.readlines()
    log.close()

    if not os.path.exists(output_dir):
        print("Making directory: " + output_dir)
        os.mkdir(output_dir)

    # Search the Glyph log indicated above for patch files to download
    for line in log_lines:
        # We are looking for asset insertions.  Such lines take the following form:
        #
        # [2017-01-30T23:37:42Z] Inserting asset 525D4C78FB699C54D77F234FD38F1D099E80AF07 from PAK file E:\RIFT\PTS\Download/TEST-304-66-A-1163253-x64/patch_core_2.pak.lzma2 into WAD file E:\RIFT\PTS\Assets\assets.089 at offset 108476510 with hash DD01FC3BE73C51D5A570253112ED0F15851D8CFC.
        #
        if "Inserting asset" in line and "Inserting assets from" not in line:
            # WOO! fun python string parsing!! just say this to yourself: MAAAAGIC
            asset_pak = line.split('PAK')[1].split('/')[-1].split('.')[0]
            asset_file = rift_dir + "Assets\\" + line.split('Assets\\')[1][:10]
            asset_offset = int(line.split('offset')[1].split(' ')[1])
            asset_hash = line.split('hash ')[1][:-1]

            #print(asset_pak, asset_file, asset_offset)

            new_output_dir = output_dir + asset_pak + "\\"
            output_name = new_output_dir + asset_file[-3:] + "_" + str(asset_offset)

            if not os.path.exists(new_output_dir):
                print("Making directory: " + new_output_dir)
                os.mkdir(new_output_dir)

            print("Extracting file as: ", output_name)

            asset_db.extractByOffset(asset_file, asset_offset, output_name)

            rename_file_by_type(output_name)

if __name__ == '__main__':
    extract_patch()
