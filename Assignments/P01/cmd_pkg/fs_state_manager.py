class FileSystemStateManager:
    def __init__(self):
        self.current_directory = "~"  # Start at home directory by default
        self.current_path = "~"  # Represent the path as a list
        self.pid = 1  # Default parent ID (can be adjusted based on the root directory)
        self.oid = 1  # Owner ID, can be set later based on the user
        self.current_user = "root"

    def set_directory(self, new_dir):
        """Update the current directory name."""
        self.current_directory = new_dir

    def get_directory(self):
        """Return the full current directory path as a string."""
        if self.current_path == ["~"]:
            return "~"
        else:
            return "/" + "/".join(self.current_path)  # Join the path components with /

    def set_path(self, new_path):
        """Update the current path with the provided new path."""
        self.current_path = new_path

    def get_path(self):
        """Return the full current path as a string."""
        return self.current_path

    def set_pid(self, pid):
        """Set the parent ID."""
        self.pid = pid

    def get_pid(self):
        """Get the parent ID."""
        return self.pid

    def set_oid(self, oid):
        """Set the owner ID."""
        self.oid = oid

    def get_oid(self):
        """Get the owner ID."""
        return self.oid

    def get_current_user(self):
        return self.current_user

    def set_current_user(self, username):
        self.current_user = username


# Create a single instance to be shared across commands
Fs_state_manager = FileSystemStateManager()
