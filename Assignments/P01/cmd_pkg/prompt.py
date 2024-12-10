from .whoami import whoami
from rich.console import Console
from rich.style import Style
from .fs_state_manager import Fs_state_manager 

console = Console()

def prompt():
  # Getting the current directory to show to the prompt
  current_directory = Fs_state_manager.get_path()

  # # Sliting the path by "/"
  # path_parts = current_directory.split("/")

  # # Get the last three folders
  # current_directory ="/".join(path_parts[-3:])

  # Get current user
  user = Fs_state_manager.get_current_user()

  # ANSI color codes
  GREEN = "\033[92m"  # Green color
  BLUE = "\033[94m"   # Blue color
  YELLOW = "\033[93m" # Yellow color
  RESET = "\033[0m"   # Reset color to default

  # Construct the prompt with colors
  prompt = f"{GREEN}({user}){RESET} {BLUE}{current_directory}{RESET} {YELLOW}$ {RESET}"

  return prompt