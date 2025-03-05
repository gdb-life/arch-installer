from utils.logger import Print
from utils.commands import run_cmd

def signature_boundaries(begin, size):
    if "G" in begin:
        begin = int(begin[:-1]) * 1024
    elif "M" in begin:
        begin = int(begin[:-1])
    elif "K" in begin:
        begin = int(begin[:-1]) / 1024

    if "G" in size:
        size = int(size[:-1]) * 1024
    elif "M" in size:
        size = int(size[:-1])
    elif "K" in size:
        size = int(size[:-1]) / 1024

    if isinstance(begin, str) and "%" in begin:
        return f"{begin} {size}MiB"
    if isinstance(size, str) and "%" in size:
        return f"{begin}MiB {size}"
    
    return f"{begin}MiB {size+begin+1}MiB"

def markup_disk(disk, partitions):
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
        partition_begin = "0%"
        part_number = 1
        for partition_name, partition_data in partitions.items():
            if "vg" in partition_name:
                for lv_name, lv_data in partition_data.items():                        
                    part, size, _ = lv_data

                    if lv_name == "partition":
                        boundaries = signature_boundaries(partition_begin, size)
                        run_cmd(f"parted {disk} mkpart primary ext4 {boundaries}")

                        vg = partition_name
                        run_cmd(f"parted {disk} set {part_number} lvm on")
                    
                        run_cmd(f"pvcreate {part}")
                        run_cmd(f"vgcreate {vg} {part}")
                        partition_begin = size
                        continue

                    if "%" in size:
                        run_cmd(f"lvcreate -l {size}FREE {vg} -n {lv_name}")
                        continue
                    run_cmd(f"lvcreate -L {size} {vg} -n {lv_name}")
                continue
            part, size, format = partition_data
            boundaries = signature_boundaries(partition_begin, size)
            run_cmd(f"parted {disk} mkpart primary {format} {boundaries}")
            if "boot" in partition_name:    
                run_cmd(f"parted {disk} set {part_number} boot on")
            partition_begin = size
            part_number += 1
    elif markup == "":
        pass
    else:
        Print.error("Invalid input")
        exit(1)
    
    Print.success("Partitioning complete")
    print()

def format_partitions(partitions, dualboot):
    Print.info("Formatting disks...")
    for partition_name, partition_data in partitions.items():
        if "vg" in partition_name:
            for lv_name, lv_data in partition_data.items():
                if lv_name == "partition":
                    continue
                part, _, format = lv_data
                if format == "linux-swap":
                    run_cmd(f"mkswap {part}")
                    continue
                if format == "btrfs":
                    run_cmd(f"mkfs.{format} -f {part}")
                    continue
                run_cmd(f"mkfs.{format} {part}")
            continue

        part, _, format = partition_data

        if "boot" in partition_name:
            if not dualboot:
                if format == "fat32":
                    run_cmd(f"mkfs.fat -F 32 {part}")
                else:
                    run_cmd(f"mkfs.{format} {part}")
            continue
        
        if "linux-swap" in format:
            run_cmd(f"mkswap {part}")
            continue

        if "btrfs" in format:
            run_cmd(f"mkfs.{format} -f {part}")
            continue

        run_cmd(f"mkfs.{format} {part}")
    Print.success("Formating complete")
    print()

def mount_partitions(partitions):
    Print.info("Mounting disks...")
    for partition_name, partition_data in partitions.items():
        if "vg" in partition_name:
            for lv_name, lv_data in partition_data.items():
                if lv_name == "partition":
                    continue
                part, _, format = lv_data
                if "linux-swap" in format:
                    run_cmd(f"swapon {part}")
                    continue
                run_cmd(f"mount {part} /mnt")
            continue

        part, _, format = partition_data

        Print.debug("Before checking boot portition")
        input()
        if "boot" in partition_name:
            run_cmd(f"mount --mkdir {part} /mnt/boot/efi")  # write checkbox for this (not working)
            Print.debug("mounting /dev/boot /mnt/boot/efi")
            input()
            continue
        
        if "linux-swap" in format:
            run_cmd(f"swapon {part}")
            continue

        run_cmd(f"mount {part} /mnt")
    Print.success("Mount complete")
    print()