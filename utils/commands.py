import subprocess
import shlex
if __name__ != "__main__":
    from utils.logger import Print
    from utils import settings
else:
    from logger import Print
    import settings

def run_cmd(command):
    """run system command (example arg: "command")"""
    # Print.debug(f"Debug: {settings.DEBUG}")
    if settings.DEBUG:
        Print.debug(f"{command}")
    try:
        command_list = shlex.split(command)
        subprocess.run(
                        command_list, 
                        check=True, 
                        # stdout=subprocess.PIPE, 
                        # stderr=subprocess.PIPE,
                        text=True)
    except subprocess.CalledProcessError as e:
        # error_message = e.stderr.strip()
        error_message = e.strip()
        Print.error(f"Failed: {command}")
        Print.error(f"{error_message}")
        # Print.error(f"{e}")
        input()
    except FileNotFoundError:
        Print.error(f"Command not found: {command}")
        input()

if __name__ == "__main__":
    DEBUG = True
    run_cmd("ls nana") 
    run_cmd("lssss")
    run_cmd("ls")
    # grub_packages = ["grub", "efibootmgr"]
    # run_cmd("sudo pacman -S --noconfirm " + " ".join(grub_packages))