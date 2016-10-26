This program is capable of converting files to and from the semi-custom format
used by the Wwise platform.

When decoding, input files must be Wwise IMA ADPCM files, and the output 
format will be a normal PCM wave of the same bitrate as the input.

When encoding, input files must be 16 bit, signed, PCM wave files. Any standard 
bitrate will do.

This tool is used from the command line. Command line options are as follows.
 -e infile outfile
 -d infile outfile
 -e_all
 -d_all 

 -e will encode a file from PCM to Wwise IMA ADPCM.
 -d will decode a file from Wwise IMA ADPCM to PCM.
 -e_all will encode all files in the folder from PCM to Wwise IMA ADPCM.
 -d_all will decode all files in the folder from Wwise IMA ADPCM to PCM.

 
Notes: This tool does not yet support loop points, and may result in errors at 
runtime when a sound that requires loop points is replaced. Support is planned.
Decoded files are ~3-5 times larger than encoded files. Make sure you have 
sufficient disk space. Input and output file must not be the same file. Attempts
to do this will result in undefined behaviour.

Please report any bugs you find on the issue tracker located on the project page.

Changes:
 1.1:
  - Added checking on the input format for decoding and give a meaningful error 
    message when it doesn't match what is expected.
  - Don't create output file before checking the input file for validity.
 1.11:
  - Changed file mode to create from open or create. This should fix a bug where 
    trying to overwrite a file would append to the file instead of replacing it.
 1.12:
  - Changed exceptions into console output to assist in running the tool from automated scripts.
 1.13:
  - Added ability to encode/decode all files in the folder.
 1.14:
  - Fixed encoding bug related to file playback length.
 1.15:
  - Fixed encoding bug related to loud static.
  - Fixed encoding bug related to mono files.
  - Fixed decoding bug related to writing an incorrect file size.

~Zwagoth