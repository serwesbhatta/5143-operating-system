from .get_column_names import Get_column_names
from database.sqliteCRUD import SqliteCRUD
import os
from .encoder_decoder import Decode


dataPath = "../database/data/"
dbName = "filesystem.db"

dbFilePath = os.path.join(dataPath, dbName)
print("Checking for database at:", dbFilePath)

if os.path.exists(dbFilePath):
    fsDB = SqliteCRUD(dbFilePath)

else:
    fsDB = None
    print("Database file not found.")


def Convert_to_dictionary(table_name: str, data):
    column_names = Get_column_names(fsDB, table_name)

    rows = [dict(zip(column_names, row)) for row in data]
    for row in rows:
        if "contents" in row:
            if row["contents"] != "NULL":
                try:
                    row["contents"] = Decode(row["contents"])
                except:
                    row["contents"] = "Cannot Decode"
    return rows
