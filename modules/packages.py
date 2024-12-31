from utils.logger import Print
from utils.commands import run_cmd

def install_packages(packages):
    Print.info("Install base packages...")
    run_cmd("pacstrap /mnt " + " ".join(packages))
    Print.success("Packages installed")
    print()

def install_yay():
    yay = Print.input("Install yay? (yes/no): ") == "yes"
    if yay:
        run_cmd("git clone https://aur.archlinux.org/yay.git /mnt/yay")
        run_cmd("cd /mnt/yay")
        run_cmd("makepkg -sirc --noconfirm")
        run_cmd("cd ..")
        run_cmd("rm -rf yay")
        Print.success("Yay installed")

