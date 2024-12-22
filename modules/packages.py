from utils.utils import Print, run_cmd

def install_packages(packages):
    try:
        Print.info("Install base packages...")
        run_cmd(["pacstrap", "/mnt"] + packages)
        Print.success("Packages installed")
    except Exception as e:
        Print.error(f"Failed to isntall package: {e}")
    print()