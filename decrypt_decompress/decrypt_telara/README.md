RIFT Telara.db Decryption

This executable contains the decryption routines required to decrypt the telara.db file.

Telara.db is a encrypted SQLITE3 database.

The code uses source from here: https://github.com/newsoft/sqlite3-dbx
REMEMBER TO USE "-DSQLITE_HAS_CODEC"

files
-----
db_key							- Binary blob - AES256 key used to decrypt the database
mine.cpp 						- Main DLL and processing, opens the encrypted database "telara.db" and resaves it as a new decrypted database called "telara_decrypted.db"
sqlite3.c						- Slightly modified from https://github.com/newsoft/sqlite3-dbx
sqlite3.h						- from https://github.com/newsoft/sqlite3-dbx
sqlite3ext.h				- from https://github.com/newsoft/sqlite3-dbx

what 