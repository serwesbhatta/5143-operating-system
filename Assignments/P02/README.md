# Virtual File System Integration with 5143 Shell Project
## Date: December 9, 2024

## Group Contributors
- Sangam Lamichhane
- Serwes Bhatta

## Project Summary
This Virtual File System (VFS) is integrated within a custom shell environment, designed to simulate file management and operations akin to an operating system's file handling capabilities, but within a self-contained database environment. The VFS interacts with the shell to provide file and directory management via command-line interfaces. 

### Core Functionalities
- Allows creating, reading, updating, and deleting file and directory entries within a virtualized environment.
- Supports executing commands that interact with the virtual filesystem, such as listing contents, changing directories, and modifying file permissions.
- Maintains a history of commands executed within the shell, saving them within the virtual filesystem for persistence and review.
- Facilitates redirecting the output of commands to files within the virtual filesystem.


## Setup Instructions
1. Install necessary dependencies from the `requirements.txt`.

2. Run the main shell script to start interacting with the virtual file system.
    ```bash
    python3 shell.py
    ```
3. Enter commands as per your needs to interact with the virtual file system (e.g., `ls`, `cd`, `mkdir`, `touch`).

## Project Files

| #  | File                    | Description                                                    |
|----|-------------------------|----------------------------------------------------------------|
| 1  | `shell.py`              | Main script facilitating user interaction through the shell interface. |
| 2  | `requirements.txt`      | Contains all dependencies required for the project.            |
| 3  | `database/`             | Houses the SQLite database and scripts managing database operations. |
| 4  | `api/`                  | API layer that provides an interface between the shell and the database. |

