
# 5143 Shell Project
## Date: December 9, 2024
### Group Contributors
- Sangam Lamichhane
- Serwes Bhatta

## Project Summary

Following its initialization, the program consistently executes these steps:
- Captures a line from the standard input (`getch()`).
- Performs logical parsing of the line into an array of components for command interpretation (managing command pipes).
- Constructs a detailed list of arguments and flags for each command.
- Executes the identified command correctly.
- Handles multiple commands by passing output from one command as input to the next.
- Directs output to designated files when output redirection is specified, rather than displaying it in the console.

## Setup Instructions
** 1. Ensure all required packages from `requirements.txt` are installed.
** 2. Execute `shell.py` (e.g., `python3 shell.py`).
** 3. Enter your commands according to your needs (e.g., `ls -la`).

## Known Issues
- Input redirection functionality is currently unavailable.
- The left and right arrow keys do not function as expected.
  

## Project Files
| #  | File               | Description                                         |
|----|--------------------|-----------------------------------------------------|
| 1  | `shell.py`         | Main script facilitating user interaction through the shell interface. |
| 2  | `requirements.txt` | Contains all dependencies required for the project. |
| 3  | `cmds`             | Directory containing files, each with specific commands and some helper files.  |


