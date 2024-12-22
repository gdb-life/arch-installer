from utils.utils import Print, run_cmd

def partition_disks(disk):
    Print.info("Disk partitioning...")
    cfdisk = Print.input("Mark up a disk manually? (yes/no) ").lower() == "yes"

    if cfdisk:
        try:
            run_cmd(["cfdisk", disk])
            Print.success("Partitioning complete")
        except Exception as e:
            Print.error(f"Failed to mark up a disk: {e}")
    else:
        Print.info("Manually mark up skipped")
        try:
            run_cmd(["parted", disk, "mklabel", "gpt"])
            run_cmd(["parted", disk, "mkpart", "primary", "fat32", "0%", "1GiB"])
            run_cmd(["parted", disk, "set", "1", "esp", "on"])
            run_cmd(["parted", disk, "mkpart", "primary", "linux-swap", "1GiB", "9GiB"])
            run_cmd(["parted", disk, "mkpart", "primary", "btrfs", "9GiB", "100%"])
            Print.success("Partitioning complete")
        except Exception as e:
            Print.error(f"Failed to mark up a disk: {e}")

    try:
        run_cmd(["mkfs.fat", "-F32", f"{disk}1"])
        run_cmd(["mkswap", f"{disk}2"])
        run_cmd(["swapon", f"{disk}2"])
        run_cmd(["mkfs.btrfs", "-f", f"{disk}3"])
        Print.success("Formating complete")
    except Exception as e:
        Print.error(f"Failed to formating disk: {e}")

    print()

def mount_disks(disk):
    Print.info("Mounting disks...")

    try:
        run_cmd(["mount", f"{disk}3", "/mnt"])
        run_cmd(["mount", "--mkdir", f"{disk}1", "/mnt/boot/efi"])
        Print.success("Mount complete")
    except Exception as e:
        Print.error(f"Failed to mount disk: {e}")
        
    print()