from utils.logger import Print
from utils.commands import run_cmd

def install_packages(packages):
    Print.info("Install base packages...")
    run_cmd("pacstrap /mnt " + " ".join(packages))
    Print.success("Packages installed")
    print()