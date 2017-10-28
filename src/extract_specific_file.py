import Assets
import os
from extract import *

def extract_nif_textures(nifFilename, output_dir):
    for texture in nifTextures(nifFilename):
        output_file = output_dir + texture
        try:
            asset_db.extractByName(texture, output_file)
        except:
            print("    could not find texture: ", texture)

models = ["2h_staff_408_extralife.nif"]

rift_dir = "C:\\Program Files (x86)\\Glyph\\Games\\RIFT\\Live\\"
output_dir = "E:\\RIFT\\datamine\\articles\\"

asset_db = Assets.AssetDatabase(rift_dir)

for model in models:
    model_name = model.split(':')[0]
    print(model_name)
    try:
        asset_db.extractByName(model_name, output_dir + model_name)
        extract_nif_textures(output_dir + model_name, output_dir)
    except:
        print("Could not find")
