import subprocess
import shlex
if __name__ != "__main__":
    from utils.logger import Print
    from utils.debug import Debug
else:
    from logger import Print
    from debug import Debug

def run_cmd(command):
    # Print.debug(f"Debug: {Debug.DEBUG}")
    if Debug.DEBUG:
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
        # Print.error(f"{error_message}")
        Print.error(f"Failed: {command}")
        Print.error(f"{e}")
        input("")
    except FileNotFoundError:
        Print.error(f"Command not found: {command}")
        input("")

if __name__ == "__main__":
    DEBUG = True
    run_cmd("ls nana") 
    run_cmd("lssss")
    # run_cmd("passwd")
    # grub_packages = ["grub", "efibootmgr"]
    # run_cmd("sudo pacman -S --noconfirm " + " ".join(grub_packages))