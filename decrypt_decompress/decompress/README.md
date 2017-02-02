RIFT Decompression Library

This library contains the decompression routines required to decompress some RIFT data.

RIFT contains a bunch of asset files. These asset files use simple ZLIB encoding. However, once extracted, some of those files are ALSO compressed.

An example is: lang_english.cds and also data from telara.db

These files use a 1024 byte tables to encode huffman frequencies and a bunch of compressed data.

Standard creation of a huffman tree yields suboptimal results and the correct algorithim was unable to be determined so the decompression routines were pulled from RIFT and turned into assembly files.

Compile into a DLL and link into whatever you need.

files
-----
123.cpp 						- Main DLL and processing
huffmanTree.asm 		- Contains the routines specifically for creating the huffman tree data from the frequency table.
huffmanDecode.asm 	- decompresses using the tree built earlier

To use, call  decompressData() method with the required data.
