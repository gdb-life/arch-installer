from utils.utils import Print, run_cmd

def install_grub(disk):
    Print.info("Installing GRUB...")
    try:
        grub_packages = ["grub", "efibootmgr"]
        run_cmd(["arch-chroot", "/mnt", "pacman", "-S", "--noconfirm"] + grub_packages)
        run_cmd(["arch-chroot", "/mnt", "grub-install", disk])
        run_cmd(["arch-chroot", "/mnt", "grub-mkconfig", "-o", "/boot/grub/grub.cfg"])
        Print.success("Installing GRUB complete")
    except Exception as e:
        Print.error(f"Failed to install GRUB: {e}")
    print()


def configure_system(hostname):
    try:
        Print.info("Configuring locale...")
        locale_file = "/mnt/etc/locale.gen"
        with open(locale_file, "r+") as f:
            content = f.read()
            content = content.replace("#en_US.UTF-8 UTF-8", "en_US.UTF-8 UTF-8")
            f.seek(0)
            f.write(content)
            f.truncate()
        run_cmd(["arch-chroot", "/mnt", "locale-gen"])
        Print.success("Locale is set up")
    except Exception as e:
        Print.error(f"Failed to configuring locale: {e}")

    try:
        Print.info("Configuring hostname...")
        with open("/mnt/etc/hostname", "w") as f:
            f.write(hostname + "\n")
        Print.success("Hostname is set up")
    except Exception as e:
        Print.error(f"Failed to configuring hostname: {e}")

    try:
        Print.info("Configuring hosts...")
        hosts_file = "/mnt/etc/hosts"
        with open(hosts_file, "w") as f:
            f.write("127.0.0.1    localhost\n")
            f.write("::1          localhost\n")
            f.write(f"127.0.0.1    {hostname}.localdomain {hostname}\n")
        Print.success("Hosts is set up")
    except Exception as e:
        Print.error(f"Failed to configuring hosts: {e}")

    try:
        Print.info("Configuring pacman...")
        pacman_conf = "/mnt/etc/pacman.conf"
        with open(pacman_conf, "r+") as f:
            content = f.read()
            content = content.replace("#Color", "Color")
            content = content.replace("#ParallelDownloads = 5", "ParallelDownloads = 10")
            content = content.replace("#[multilib]", "[multilib]")
            content = content.replace("#Include = /etc/pacman.d/mirrorlist", "Include = /etc/pacman.d/mirrorlist")
            f.seek(0)
            f.write(content)
            f.truncate()
        Print.success("Pacman is set up")
    except Exception as e:
        Print.error(f"Failed to configuring pacman: {e}")

    try:
        Print.info("Configuring sudo...")
        sudoers_file = "/mnt/etc/sudoers"
        run_cmd(["chmod", "u+w", sudoers_file])
        with open(sudoers_file, "r+") as f:
            content = f.read()
            content = content.replace("# %wheel ALL=(ALL:ALL) ALL", "%wheel ALL=(ALL:ALL) ALL")
            f.seek(0)
            f.write(content)
            f.truncate()
        run_cmd(["chmod", "u-w", sudoers_file])
        Print.success("Sudo is set up")
    except Exception as e:
        Print.error(f"Failed to configuring sudo: {e}")

    try:
        Print.info("Set root password:")
        run_cmd(["arch-chroot", "/mnt", "passwd"])
        Print.success("Root password is set up")
    except Exception as e:
        Print.error(f"Failed to set root password: {e}")

    print()

def create_user(username):
    try:
        Print.info(f"Creating user '{username}'...")
        run_cmd(["arch-chroot", "/mnt", "useradd", "-m", "-G", "wheel", username])
        Print.info(f"Set password for user '{username}':")
        run_cmd(["arch-chroot", "/mnt", "passwd", username])
        Print.success("Finish create user")
    except Exception as e:
        Print.error(f"Failed to create user: {e}")
    print()

def enable_services(services):
    for service in services:
        try:
            Print.info(f"Enabling '{service}' service...")
            run_cmd(["arch-chroot", "/mnt", "systemctl", "enable", service])
            Print.success(f"Enabling '{service}' finished")
        except Exception as e:
            Print.error(f"Failed to enable service: {e}")
    print()

def finish():
    try:
        Print.info("Finish installation...")
        run_cmd(["umount", "-R", "/mnt"])
        Print.success("Installation complete")
    except Exception as e:
        Print.error(f"Failed to finish install: {e}")
    print()