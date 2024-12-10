def Directory_exists(self, directory_name, pid):
    """Check if a directory exists in the given parent directory (pid)."""
    query = "SELECT COUNT(*) FROM directories WHERE name = ? AND pid = ?"
    self.cursor.execute(query, (directory_name, pid))
    count = self.cursor.fetchone()[0]
    return count > 0
