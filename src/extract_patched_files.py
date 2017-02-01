import Assets
import os
from extract import *

### RENAME THESE PATHS TO POINT TO THE CORRECT FILE OR DIRECTORY ON YOUR SYSTEM! ###
rift_dir = "E:\\RIFT\\PTS\\"
glyph_log = "C:\\Users\\Kyle\\AppData\\Local\\Glyph\\Logs\\GlyphClient.2.test.log"
output_dir = "E:\\RIFT\\datamine\\jan30-test\\"

asset_db = Assets.AssetDatabase(rift_dir)

def extract_nif_textures(nifFilename, output_dir):
    for texture in nifTextures(nifFilename):
        output_file = output_dir + texture
        try:
            asset_db.extractByName(texture, output_file)
        except:
            print("    could not find texture: ", texture)

def rename_file_by_type(filename):
    if os.path.exists(filename):
        f = open(filename, "rb")
        start_data = str(f.read(32))
        f.close()

        if 'Gamebryo File Format' in start_data:
            nifFilename = nifName(filename)
            rename = filename + "_" + nifFilename
            
            if not os.path.exists(rename):
                os.rename(filename, rename)

            extract_nif_textures(rename, filename[:filename.rfind('\\')] + "\\")
        elif 'DDS' in start_data:
            rename = filename + ".dds"
            
            if not os.path.exists(rename):
                os.rename(filename, rename)
        elif 'Exif' in start_data:
            rename = filename + ".tif"
            
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
        if "Inserting asset" in line and "Inserting assets from" not in line:
            asset_pak = line.split(' ')[7].split('/')[-1].split('.')[0]
            asset_file = line.split(' ')[11]
            asset_offset = int(line.split(' ')[14])

            # The patch_ paks tend to contain terrain models.  We don't care about those
            # right now.
            if 'patch_' not in asset_pak:
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
