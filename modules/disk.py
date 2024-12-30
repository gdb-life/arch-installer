from utils.logger import Print
from utils.commands import run_cmd

def signature_boundaries(begin, size):
    if "GiB" in begin:
        begin = int(begin[:-3]) * 1024
    elif "MiB" in begin:
        begin = int(begin[:-3])
    elif "KiB" in begin:
        begin = int(begin[:-3]) / 1024
    elif "%" in begin:
        return f"{begin} {size}"

    if "GiB" in size:
        size = int(size[:-3]) * 1024
    elif "MiB" in size:
        size = int(size[:-3])
    elif "KiB" in size:
        size = int(size[:-3]) / 1024
    elif "%" in size:
        return f"{begin}MiB {size}"
    
    return f"{begin}MiB {size+begin}MiB"

def markup_disk(disk, partitions_size, partitions_format):
    Print.info("Disk partitioning...")
    signatures = Print.input("Delete old signatures? (yes/no) ").lower() == "yes"
    if signatures:
        run_cmd(f"wipefs --all {disk}")
    markup = Print.input("Mark up a disk with? (cfdisk/fdisk/auto) ").lower()
    if markup == "cfdisk":
        run_cmd(f"cfdisk {disk}")
    elif markup == "fdisk":
        run_cmd(f"fdisk {disk}")
    elif markup == "auto":
        run_cmd(f"parted {disk} mklabel gpt")

        boot_boundaries = signature_boundaries("0MiB", partitions_size['boot'])
        run_cmd(f"parted {disk} mkpart primary {partitions_format['boot']} {boot_boundaries}")
        run_cmd(f"parted {disk} set 1 esp on")

        swap_boundaries = signature_boundaries(partitions_size['boot'], partitions_size['swap'])
        run_cmd(f"parted {disk} mkpart primary {partitions_format['swap']} {swap_boundaries}")

        home_boundaries = signature_boundaries(partitions_size['swap'], partitions_size['home'])
        run_cmd(f"parted {disk} mkpart primary {partitions_format['home']} {home_boundaries}")
    else:
        Print.error("Invalid input")
        exit(1)
    
    Print.success("Partitioning complete")
    print()

def format_partitions(partitions, partitions_format, dualboot):
    Print.info("Formatting disks...")
    if not dualboot:
        if partitions_format['boot'].lower() == "fat32":
            run_cmd(f"mkfs.fat -F 32 {partitions['boot']}")
        else:
            run_cmd(f"mkfs.{partitions_format['boot']} {partitions['boot']}")
    run_cmd(f"mkswap {partitions['swap']}")
    run_cmd(f"swapon {partitions['swap']}")
    if partitions_format['home'].lower() == "btrfs":
        run_cmd(f"mkfs.{partitions_format['home']} -f {partitions['home']}")
    else:
        run_cmd(f"mkfs.{partitions_format['home']} {partitions['home']}")
    Print.success("Formating complete")
    print()

def mount_partitions(partitions):
    Print.info("Mounting disks...")
    run_cmd(f"mount {partitions['home']} /mnt")
    run_cmd(f"mount --mkdir {partitions['boot']} /mnt/boot/efi")
    Print.success("Mount complete")
    print()