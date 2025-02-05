from utils.logger import Print
from utils.commands import run_cmd

def dependencies():
    Print.info("Checking dependencies...")
    run_cmd("sudo pacman -Sy --noconfirm")
    run_cmd("sudo pacman -S --noconfirm python")
    Print.success("Dependencies checked\n")