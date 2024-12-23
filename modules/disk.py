from utils.logger import Print
from utils.commands import run_cmd

def markup(disk):
    Print.info("Disk partitioning...")
    cfdisk = Print.input("Mark up a disk manually? (yes/no) ").lower() == "yes"
    if cfdisk:
        run_cmd(f"cfdisk {disk}")
    else:
        Print.info("Manually mark up skipped")
        run_cmd(f"parted {disk} mklabel gpt")
        run_cmd(f"parted {disk} mkpart primary fat32 0% 1GiB")
        run_cmd(f"parted {disk} set 1 esp on")
        run_cmd(f"parted {disk} mkpart primary linux-swap 1GiB 9GiB")
        run_cmd(f"parted {disk} mkpart primary btrfs 9GiB 100%")
    Print.success("Partitioning complete")
    print()

def format(disk):
    Print.info("Formatting disks...")
    run_cmd(f"mkfs.fat -F32 {disk}1")
    run_cmd(f"mkswap {disk}2")
    run_cmd(f"swapon {disk}2")
    run_cmd(f"mkfs.btrfs -f {disk}3")
    Print.success("Formating complete")
    print()

def mount(disk):
    Print.info("Mounting disks...")
    run_cmd(f"mount {disk}3 /mnt")
    run_cmd(f"mount --mkdir {disk}1 /mnt/boot/efi")
    Print.success("Mount complete")
    print()