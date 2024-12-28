from utils.logger import Print
from utils.commands import run_cmd

def check_dependencies():
    Print.info("Checking dependencies...")
    run_cmd("sudo pacman -Sy --noconfirm")
    run_cmd("sudo pacman -S --noconfirm git")
    run_cmd("sudo pacman -S --noconfirm python")
    run_cmd("sudo pacman -S --noconfirm reflector")
    Print.success("Dependencies checked\n")

def update_pacman_keys():
    keys = Print.input("Update pacman keys? (yes/no) ").lower() == "yes"
    if keys:
        Print.info("Update pacman keys...")
        run_cmd("sudo pacman-key --refresh-keys")
        Print.success("Pacman keys updated\n")  
    print()

def update_pacman_mirrors():
    mirrors = Print.input("Update pacman mirrors? (yes/no) ").lower() == "yes"
    if mirrors:
        Print.info("Update pacman mirrors...")
        run_cmd("sudo reflector --verbose -l 15 -p https --sort rate --save /etc/pacman.d/mirrorlist")
        run_cmd("sudo pacman -Sy --noconfirm")
        Print.success("Pacman mirrors updated\n")
    print()
