import sqlite3
from database.operations.directory_exists import Directory_exists
from prettytable import PrettyTable
from .operations import *

class SqliteCRUD:
    """A class to perform CRUD operations on a SQLite database."""

    def __init__(self, db_path):
        """Initialize the database connection and cursor."""
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def get_column_names(self, table_name):
        return Get_column_names(self.cursor, table_name)
   
    def create_table(self, table_name, columns):
        Create_table(self.cursor, self.conn, table_name, columns)

    def drop_table(self, table_name):
        Drop_table(self.cursor, self.conn, table_name)

    def show_tables(self, raw=True):
        return Show_tables(self.cursor, raw)

    def describe_table(self, table_name, raw=False):
        return Describe_table(self.cursor, table_name, raw)

    def insert_data(self, table_name, data):
        Insert_data(self.cursor, self.conn, table_name, data)

    def read_data(self, table_name, filters=None):
        return Read_data(self.cursor, table_name, filters)

    def update_data(self, table_name, column, new_value, condition_column, condition_value):
        return Update_data(self.cursor, self.conn, table_name, column, new_value, condition_column, condition_value)

    def delete_data(self, table_name, condition_column, condition_value):
        Delete_data(self.cursor, self.conn, table_name, condition_column, condition_value)

    def table_exists(self, table_name):
        return Table_exists(self.cursor, table_name)

    def get_file_content(self, filters):
        return Get_file_content(self.cursor, filters)

    def set_permissions(self, table_name, permissions,filters):
        return Set_permissions(self.cursor, self.conn, table_name, permissions, filters)
    
    def update_multiple_data(self, table_name, filters, new_values):
        return Update_multiple_data(self.cursor, self.conn, table_name, filters, new_values)
    
    ##def directory_exists(self, directory_name):
       ## return Directory_exists(self.cursor, directory_name)


    def directory_exists(self, directory_name, pid):
        """Check if a directory exists in the given parent directory (pid)."""
        query = "SELECT COUNT(*) FROM directories WHERE name = ? AND pid = ?"
        self.cursor.execute(query, (directory_name, pid))
        count = self.cursor.fetchone()[0]
        return count > 0

    def get_directory_pid(self, directory_name, pid):
        query = "SELECT id FROM directories WHERE name = ? AND pid = ?"
        self.cursor.execute(query, (directory_name, pid))
        result = self.cursor.fetchone()
        if result:
            return result[0]  # Return the directory ID (pid)
        return None
    
    def get_parent_directory(self, pid):
        """Retrieve the parent directory for the given directory ID (pid)."""
        query = "SELECT name, pid FROM directories WHERE id = ?"
        self.cursor.execute(query, (pid,))
        result = self.cursor.fetchone()
        if result:
            return {'name': result[0], 'pid': result[1]}  # Return a dictionary with name and pid
        return None
    
    def file_belongs_to_directory(self, file_name, directory_pid):
        """Check if a file belongs to a specific directory."""
        query = "SELECT COUNT(*) FROM files WHERE name = ? AND pid = ?"
        self.cursor.execute(query, (file_name, directory_pid))
        count = self.cursor.fetchone()[0]
        return count > 0
    
    def file_exists(self, file_name, pid):
        """Check if a file exists in the given directory (pid)."""
        query = "SELECT COUNT(*) FROM files WHERE name = ? AND pid = ?"
        result = self.execute(query, (file_name, pid))
        return result[0][0] > 0  # Return True if file exists

    def get_file_contents(self, file_name, pid):
        """Retrieve the contents of a file in the given directory (pid)."""
        query = "SELECT contents FROM files WHERE name = ? AND pid = ?"
        result = self.execute(query, (file_name, pid))
        if result:
            return result[0][0]  # Return the contents (as BLOB)
        return None

    def execute(self, query, params=None):
        """Execute a query with optional parameters."""
        if params is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, params)
        self.conn.commit()
        return self.cursor.fetchall()

    def close_connection(self):
        """Close the database connection."""
        self.conn.close()
        print("Database connection closed.")
