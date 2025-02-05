from utils.logger import Print
from utils.commands import run_cmd

def install_grub(disk, dualboot):
    Print.info("Installing GRUB...")
    if not dualboot:
        grub_packages = ["grub", "efibootmgr"]
    else:
        grub_packages = ["grub", "efibootmgr", "os-prober"]
    run_cmd("arch-chroot /mnt pacman -S --noconfirm " + " ".join(grub_packages))
    run_cmd(f"arch-chroot /mnt grub-install {disk}")
    if dualboot:
        locale_file = "/mnt/etc/default/grub"
        with open(locale_file, "r+") as f:
            content = f.read()
            content = content.replace("#GRUB_DISABLE_OS_PROBER=false", "GRUB_DISABLE_OS_PROBER=false")
            f.seek(0)
            f.write(content)
            f.truncate()
        run_cmd("arch-chroot /mnt os-prober")
    run_cmd("arch-chroot /mnt grub-mkconfig -o /boot/grub/grub.cfg")
    Print.success("Installing GRUB complete")
    print()


def configure_system(hostname, locale):
    Print.info("Configuring locale...")
    locale_file = "/mnt/etc/locale.gen"
    with open(locale_file, "r+") as f:
        content = f.read()
        content = content.replace(f"# {locale}.UTF-8 UTF-8", f"{locale}.UTF-8 UTF-8")
        f.seek(0)
        f.write(content)
        f.truncate()
    run_cmd("arch-chroot /mnt locale-gen")
    Print.success("Locale is set up")

    Print.info("Configuring hostname...")
    with open("/mnt/etc/hostname", "w") as f:
        f.write(hostname + "\n")
    Print.success("Hostname is set up")
 
    Print.info("Configuring hosts...")
    hosts_file = "/mnt/etc/hosts"
    with open(hosts_file, "w") as f:
        f.write("127.0.0.1    localhost\n")
        f.write("::1          localhost\n")
        f.write(f"127.0.0.1    {hostname}.localdomain {hostname}\n")
    Print.success("Hosts is set up")

    Print.info("Configuring pacman...")
    pacman_conf = "/mnt/etc/pacman.conf"
    with open(pacman_conf, "r+") as f:
        content = f.read()
        content = content.replace("#Color", "Color")
        content = content.replace("#ParallelDownloads = 5", "ParallelDownloads = 10\nIloveCandy")
        content = content.replace("#[multilib]", "[multilib]")
        content = content.replace("#Include = /etc/pacman.d/mirrorlist", "Include = /etc/pacman.d/mirrorlist")
        f.seek(0)
        f.write(content)
        f.truncate()
    Print.success("Pacman is set up")

    Print.info("Configuring sudo...")
    sudoers_file = "/mnt/etc/sudoers"
    run_cmd(f"chmod u+w {sudoers_file}")
    with open(sudoers_file, "r+") as f:
        content = f.read()
        content = content.replace("# %wheel ALL=(ALL:ALL) ALL", "%wheel ALL=(ALL:ALL) ALL")
        f.seek(0)
        f.write(content)
        f.truncate()
    run_cmd(f"chmod u-w {sudoers_file}")
    Print.success("Sudo is set up")

    # Print.info("Set root password:")
    # run_cmd("arch-chroot /mnt passwd")
    # Print.success("Root password is set up")

    print()

def timezone(timezone):
    run_cmd(f"timedatectl set-timezone {timezone}")
    run_cmd(f"timedatectl set-ntp 1")
    run_cmd(f"timedatectl set-local-rtc 1")

def create_user(username):
    Print.info(f"Creating user '{username}'...")
    run_cmd(f"arch-chroot /mnt useradd -m -G wheel {username}")
    Print.info(f"Set password for user '{username}':")
    run_cmd(f"arch-chroot /mnt passwd {username}")
    Print.success("Finish create user")
    print()

def enable_services(services):
    for service in services:
        Print.info(f"Enabling '{service}' service...")
        run_cmd(f"arch-chroot /mnt systemctl enable {service}")
        Print.success(f"Enabling '{service}' finished")
    print()

def update_user_pacman_keys():
    keys = Print.input("Update user pacman keys? (yes/no) ").lower() == "yes"
    if keys:
        Print.info("Update user pacman keys...")
        run_cmd("arch-chroot /mnt sudo pacman-key --refresh-keys")
        Print.success("Pacman keys updated\n")  
    print()

def update_user_pacman_mirrors():
    mirrors = Print.input("Update user pacman mirrors? (yes/no) ").lower() == "yes"
    if mirrors:
        Print.info("Update user pacman mirrors...")
        run_cmd("arch-chroot /mnt sudo pacman -S --noconfirm reflector")
        run_cmd("arch-chroot /mnt sudo reflector --verbose -l 15 -p https --sort rate --save /etc/pacman.d/mirrorlist")
        run_cmd("arch-chroot /mnt sudo pacman -Sy --noconfirm")
        Print.success("Pacman mirrors updated\n")
    print()

def finish():
    Print.info("Finish installation...")
    run_cmd("umount -R /mnt")
    run_cmd("swapoff -a")
    Print.success("Installation complete")
    print()