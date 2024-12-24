from utils.logger import Print
from utils.commands import run_cmd

def check_dependencies():
    Print.info("Checking dependencies...")
    run_cmd("pacman -Sy --noconfirm")
    run_cmd("pacman -S --noconfirm git")
    run_cmd("pacman -S --noconfirm python")
    run_cmd("pacman -S --noconfirm reflector")
    Print.success("Dependencies checked\n")

def pacman_keys():
    keys = Print.input("Update pacman keys? (yes/no) ").lower() == "yes"
    if keys:
        Print.info("Update pacman keys...")
        run_cmd("pacman-key --refresh-keys")
        Print.success("Pacman keys updated\n")  
    else:
        Print.info("Keys update skipped")
    print()

def pacman_mirrors():
    mirrors = Print.input("Update pacman mirrors? (yes/no) ").lower() == "yes"
    if mirrors:
        Print.info("Update pacman mirrors...")
        run_cmd("reflector --verbose -l 50 -p http --sort rate --save /etc/pacman.d/mirrorlist")
        run_cmd("reflector --verbose -l 15 --sort rate --save /etc/pacman.d/mirrorlist")
        run_cmd("pacman -Sy --noconfirm")
        Print.success("Pacman mirrors updated\n")
    else:
        Print.info("Mirror update skipped")
    print()
