import subprocess
from utils.config import DEBUG

class Print:
    COLORS = {
        "INFO": "\033[93m",     # yellow
        "FAILED": "\033[91m",   # red
        "SUCCESS": "\033[92m",  # green
        "DBUG": "\033[96m",     # blue
    }
    RESET = "\033[0m"   # reset color
    # BRACKET_COLOR = "\033[37m"  # white for text in brackets
    COLOR_WHITE = "\033[97m"     # white

    @staticmethod
    def log(message, level="info"):
        """basic logger method"""
        color = Print.COLORS.get(level, "\033[37m")      # default to white
        prefix = f"[ {color}{level[:4]}{Print.RESET} ]"  # color only inside brackets
        print(f"{prefix} {message}")

    @staticmethod
    def info(message):
        Print.log(message, level="INFO")

    @staticmethod
    def error(message):
        Print.log(message, level="FAILED")

    @staticmethod
    def success(message):
        Print.log(message, level="SUCCESS")

    @staticmethod
    def debug(message):
        Print.log(message, level="DBUG")

    @staticmethod
    def input(prompt):
        """Prompt user input with colored text."""
        colored_prompt = f"{Print.COLOR_WHITE}{prompt}{Print.RESET}"
        return input(colored_prompt).strip()

def run_cmd(command):
    """run system command"""
    if DEBUG:
        Print.debug(f"{' '.join(command)}")
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        Print.error(f"Command failed: {' '.join(command)}")
        Print.error(f"Error message: {e}")
        raise