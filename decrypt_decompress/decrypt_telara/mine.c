#include <stdio.h>
#include <stdlib.h>
#include "sqlite3.h"

/*
** This function is used to load the contents of a database file on disk 
** into the "main" database of open database connection pInMemory, or
** to save the current contents of the database opened by pInMemory into
** a database file on disk. pInMemory is probably an in-memory database, 
** but this function will also work fine if it is not.
**
** Parameter zFilename points to a nul-terminated string containing the
** name of the database file on disk to load from or save to. If parameter
** isSave is non-zero, then the contents of the file zFilename are 
** overwritten with the contents of the database opened by pInMemory. If
** parameter isSave is zero, then the contents of the database opened by
** pInMemory are replaced by data loaded from the file zFilename.
**
** If the operation is successful, SQLITE_OK is returned. Otherwise, if
** an error occurs, an SQLite error code is returned.
*/
int loadOrSaveDb(sqlite3 *pInMemory, const char *zFilename, int isSave){
  int rc;                   /* Function return code */
  sqlite3 *pFile;           /* Database connection opened on zFilename */
  sqlite3_backup *pBackup;  /* Backup object used to copy data */
  sqlite3 *pTo;             /* Database to copy to (pFile or pInMemory) */
  sqlite3 *pFrom;           /* Database to copy from (pFile or pInMemory) */

  /* Open the database file identified by zFilename. Exit early if this fails
  ** for any reason. */
  rc = sqlite3_open(zFilename, &pFile);
  if( rc==SQLITE_OK ){

    /* If this is a 'load' operation (isSave==0), then data is copied
    ** from the database file just opened to database pInMemory. 
    ** Otherwise, if this is a 'save' operation (isSave==1), then data
    ** is copied from pInMemory to pFile.  Set the variables pFrom and
    ** pTo accordingly. */
    pFrom = (isSave ? pInMemory : pFile);
    pTo   = (isSave ? pFile     : pInMemory);

    /* Set up the backup procedure to copy from the "main" database of 
    ** connection pFile to the main database of connection pInMemory.
    ** If something goes wrong, pBackup will be set to NULL and an error
    ** code and message left in connection pTo.
    **
    ** If the backup object is successfully created, call backup_step()
    ** to copy data from pFile to pInMemory. Then call backup_finish()
    ** to release resources associated with the pBackup object.  If an
    ** error occurred, then an error code and message will be left in
    ** connection pTo. If no error occurred, then the error code belonging
    ** to pTo is set to SQLITE_OK.
    */
    pBackup = sqlite3_backup_init(pTo, "main", pFrom, "main");

	if( pBackup ){
      (void)sqlite3_backup_step(pBackup, -1);
      (void)sqlite3_backup_finish(pBackup);
    }
	else fprintf(stderr, "Failed to begin decryption");
    rc = sqlite3_errcode(pTo);
  }
  else
	fprintf(stderr, "Failed to open decrypted db: %s\n", zFilename);

  /* Close the database connection opened on database file zFilename
  ** and return the result of this function. */
  (void)sqlite3_close(pFile);
  return rc;
}

static int callback(void *data, int argc, char **argv, char **azColName){
   int i;
   fprintf(stderr, "%s: ", (const char*)data);
   for(i=0; i<argc; i++){
      printf("%s = %s\n", azColName[i], argv[i] ? argv[i] : "NULL");
   }
   printf("\n");
   return 0;
}


int main(int argc, char **argv)
{
	char *sql = "select count(*) from sqlite_master";
        sqlite3 *db;
		char key[64];
        const char *keyFile = "db_key";
        char *zErrMsg = 0;
		const char* data = "Callback function";
		FILE *handle ;
        int rc = sqlite3_open("telara.db", &db);
        if (rc)
        {
                fprintf(stderr, "Can't open file: %s\n", sqlite3_errmsg(db));
                return 1;
        }
        fprintf(stderr, "File opened: %s\n", "telara.db");
        sqlite3_activate_see("7bb07b8d471d642e");
		
		
		handle = fopen(keyFile, "rb");
        if (NULL == handle)
        {
                fprintf(stderr, "Can't open file: %s\n", keyFile);
                return 1;
        }
        fread(key, 1,64, handle);
		fclose(handle);

        sqlite3_key(db, key, 32);

		
        /* Execute SQL statement */
           rc = sqlite3_exec(db, sql, callback, (void*)data, &zErrMsg);
           if( rc != SQLITE_OK ){
              fprintf(stderr, "SQL error: %s\n", zErrMsg);
              sqlite3_free(zErrMsg);
			  return 1;
           }else{
              fprintf(stdout, "Operation done successfully\n");
           }



    
        sqlite3_rekey(db, NULL, 0);

        loadOrSaveDb(db, "telara_decrypted.db", 1);

           sqlite3_close(db);


        return 0;
}
