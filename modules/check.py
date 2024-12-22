from utils.utils import Print, run_cmd

def pacman_keys():
    keys = Print.input("Update pacman keys? (yes/no) ").lower() == "yes"

    if keys:
        try:
            Print.info("Update pacman keys...")
            run_cmd(["pacman-key", "--refresh-keys"])
            Print.success("Pacman keys updated\n")  
        except Exception as e:
            Print.error(f"Failed to update keys: {e}")
    else:
        Print.info("Keys update skipped")

    print()

def pacman_mirrors():
    mirrors = Print.input("Update pacman mirrors? (yes/no) ").lower() == "yes"
    
    if mirrors:
        try:
            Print.info("Update pacman mirrors...")
            run_cmd(["pacman", "-Sy", "--noconfirm"])
            run_cmd(["pacman", "-S", "reflector", "--noconfirm"])
            run_cmd(["reflector", "--verbose", "-l", "50", "-p", "http", "--sort", "rate", "--save", "/etc/pacman.d/mirrorlist"])
            run_cmd(["reflector", "--verbose", "-l", "15", "--sort", "rate", "--save", "/etc/pacman.d/mirrorlist"])
            run_cmd(["pacman", "-Sy", "--noconfirm"])
            Print.success("Pacman mirrors updated\n")
        except Exception as e:
            Print.error(f"Failed to update mirrors: {e}")
    else:
        Print.info("Mirror update skipped")

    print()
