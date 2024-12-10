from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
from datetime import datetime
from pydantic import BaseModel

# Builtin libraries
import os, sys

# Add the parent directory to the system path to import 'database'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Classes from your module
from database import SqliteCRUD

# import different routes as modules
from routes import *


CURRENT_TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# FastAPI application instance
description = """🚀
## File System API (Simulated using SQLite)
"""

app = FastAPI(
    title="File System",
    description=description,
    version="0.0.1",
    terms_of_service="https://serwes.com/terms/",
    contact={
        "name": "FileSystemAPI",
        "url": "https://serwes.com/contact/",
        "email": "chacha@serwes.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

# Database setup
# dataPath = os.getenv("DB_PATH")
# dbName = os.getenv("DB_NAME")

dataPath = "../database/data/"
dbName = "filesystem.db"

dbFilePath = os.path.join(dataPath, dbName)
print("Checking for database at:", dbFilePath)

if os.path.exists(dbFilePath):
    fsDB = SqliteCRUD(dbFilePath)

else:
    fsDB = None
    print("Database file not found.")


class WriteData(BaseModel):
    oid: int
    pid: int
    filepath: str
    content: str


class IdentifyFileOrDir(BaseModel):
    oid: int
    pid: int
    name: str


class Copy(BaseModel):
    oid: int
    pid: int
    name: str
    target_pid: int


class Permission(BaseModel):
    file: bool
    oid: int
    pid: int
    name: str
    mode: str


class Rename(BaseModel):
    oid: int
    pid: int
    name: str
    new_name: str


# API Routes
@app.get("/")
async def docs_redirect():
    return RedirectResponse(url="/docs")


@app.get("/columnNames")
def get_column_names(table_name: str):
    return Get_column_names(fsDB, table_name)


@app.get("/files")
def get_files_route(oid: int, pid: int, name: str = None):
    return Get_files(fsDB, oid, pid, name)


@app.post("/touch")
def create_file_route(data: IdentifyFileOrDir):
    return Create_file(fsDB, data.oid, data.pid, data.name)


@app.delete("/rm")
def delete_file_route(data: IdentifyFileOrDir):
    return Delete_file(fsDB, data.oid, data.pid, data.name)


@app.get("/file")
def read_file_content(oid: int, pid: int, filename: str):
    return Read_file(fsDB, oid, pid, filename)


@app.put("/write")
def write_file_route(data: WriteData):
    return Write_file(fsDB, data.oid, data.pid, data.filepath, data.content)


@app.put("/mv")
def move_file_route(data: Copy):
    return Move_file(
        fsDB,
        data.oid,
        data.pid,
        data.name,
        data.target_pid,
    )


@app.put("/renameFile")
def rename_file(data: Rename):
    return Rename_file(fsDB, data.oid, data.pid, data.name, data.new_name)


@app.post("/createDir")
def create_directory(data: IdentifyFileOrDir):
    return Create_directory(fsDB, data.oid, data.pid, data.name)


@app.delete("/deleteDir")
def delete_directory(oid: int, pid: int, directory_name: str):
    return Delete_directory(fsDB, oid, pid, directory_name)


@app.get("/dirs")
def list_directories(oid: int, pid: int, name: str = None):
    return List_directories(fsDB, oid, pid, name)


@app.get("/dirById")
def dir_by_id(oid: int, id: int):
    return Dir_by_id(fsDB, oid, id)


@app.get("/parentDir")
def get_parent_directory(id: int):
    return Get_parent_directory(fsDB, id)


@app.get("/users")
def get_users(user_id: int = None):
    return Get_users(fsDB, user_id)


@app.post("/copy")
def copy_file(data: Copy):
    return Copy_file(
        fsDB,
        data.oid,
        data.pid,
        data.name,
        data.target_pid,
    )


@app.put("/setpermissions")
def set_permissions(data: Permission):
    return Set_permissions(fsDB, data.file, data.oid, data.pid, data.name, data.mode)


if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8080, log_level="debug", reload=True)
