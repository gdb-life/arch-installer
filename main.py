import argparse
import json
from utils.commands import run_cmd
from utils.logger import Print
from utils.debug import Debug
from modules import disk, check, packages, setup

def load_config(file_name):
    with open("configs/" + file_name + ".json", "r") as f:
        return json.load(f)
    
def save_config(file_name, config):
    if not file_name:
        file_name = Print.input("Enter the name for the configuration file: ")
    with open(f"configs/{file_name}.json", "w") as f:
        json.dump(config, f, indent=4)

def customize_config(config):
    config["disk"] = Print.input(f"Disk [{config.get('disk', '/dev/sda')}]: ") or config["disk"]
    run_cmd(f"lsblk -f {config['disk']}")
    config["dualboot"] = Print.input(f"Dualboot [{config.get('dualboot', False)}]: ") or config["dualboot"]
    
    partitions = {}
    while True:
        part_name = Print.input("Enter partition name (leave empty to finish) [boot, vg, home]: ")
        if not part_name:
            break
        
        # is_lvm = Print.input(f"Is {part_name} an LVM volume group? (yes/no): ").lower() == "yes"
        
        if "vg" in part_name:
            partitions[part_name] = {}
            partitions[part_name]["partition"] = [
                Print.input(f"{part_name} physical volume path [/dev/sda2]: "),
                Print.input(f"{part_name} size [1G, 100%]: "),
                "lvm"
            ]
            while True:
                lv_name = Print.input("Enter logical volume name (leave empty to finish) [lv-swap, lv-home]: ")
                if not lv_name:
                    break
                partitions[part_name][lv_name] = [
                    Print.input(f"{lv_name} path [/dev/vg/lv]: "),
                    Print.input(f"{lv_name} size [1G, 100%]: "),
                    Print.input(f"{lv_name} filesystem type [fat32, linux-swap, ext4]: ")
                ]
        else:
            partitions[part_name] = [
                Print.input(f"{part_name} path [/dev/sda1]: "),
                Print.input(f"{part_name} size [1G, 100%]: "),
                Print.input(f"{part_name} filesystem type [fat32, linux-swap, ext4]: ")
            ]
    
    config["partitions"] = partitions
    config["hostname"]  = Print.input(f"Hostname [{config.get('hostname', 'archlinux')}]: ") or config["hostname"]
    config["username"]  = Print.input(f"Username [{config.get('username', 'user')}]: ") or config["username"]
    config["locale"]    = Print.input(f"Locale [{config.get('locale', 'en_US.UTF-8')}]: ") or config["locale"]
    config["timezone"]  = Print.input(f"Timezone [{config.get('timezone', 'UTC')}]: ") or config["timezone"]
    
    packages = Print.input(f"Add packages [{', '.join(config.get('packages', []))}]: ")
    if packages:
        config["packages"].extend(packages.split(","))
    
    services = Print.input(f"Add services [{', '.join(config.get('enable_services', []))}]: ")
    if services:
        config["enable_services"].extend(services.split(","))
    
    return config

def print_config_data(config_data):
    Print.data("Disk: ", config_data["disk"])
    Print.data("Dualboot: ", config_data["dualboot"])
    for part_name, part_data in config_data["partitions"].items():
        if "vg" in part_name:
            Print.data(f"{part_name.capitalize()}: ", ", ".join(part_data["partition"]))
            for lv_name, lv_data in part_data.items():
                if lv_name == "partition":
                    continue
                Print.data(f"    {lv_name.capitalize()}: ", ", ".join(lv_data))
            continue
        Print.data(f"{part_name.capitalize()}: ", ", ".join(part_data))
    Print.data("Hostname: ", config_data["hostname"])
    Print.data("Username: ", config_data["username"])
    Print.data("Packages: ", ", ".join(config_data["packages"]))
    Print.data("Locale:   ", config_data["locale"])
    Print.data("Timezone: ", config_data["timezone"])
    Print.data("Services: ", ", ".join(config_data["enable_services"]))

def main():
    parser = argparse.ArgumentParser(description="Arch Installer: auto isntall Arch Linux")
    parser.add_argument("config", nargs="?", help="Name of the configuration file (without .json)")
    parser.add_argument("-c", "--custom", action="store_true", help="customize configuration")
    parser.add_argument("-p", "--print", action="store_true", help="print configuration")
    parser.add_argument("-w", "--write", nargs="?", const="default", help="write configuration to file with optional name")
    parser.add_argument("-d", "--debug", action="store_true", help="show debug information")
    parser.add_argument("-r", "--reboot", action="store_true", help="reboot after installation")
    parser.add_argument("-db", "--dualboot", action="store_true", help="enable dualboot mode (don't format boot partition, install GRUB tools for second OS)")
    args = parser.parse_args()

    if args.debug:
        Debug.DEBUG = True

    config_data = load_config("standart")

    if args.config:
        config_data = load_config(args.config)

    if args.custom:
        config_data = customize_config(config_data)

    if args.write:
        save_config(args.write if args.write != None else "default", config_data)
        Print.success(f"Configuration saved to configs/{args.write}.json")
        exit(0)

    if args.print:
        print_config_data(config_data)
        exit(0)

    if args.dualboot:
        config_data["dualboot"] = True

    check.dependencies()

    disk.markup_disk(config_data["disk"], config_data["partitions"])
    disk.format_partitions(config_data["partitions"], config_data["dualboot"])
    disk.mount_partitions(config_data["partitions"])

    packages.install_packages(config_data["packages"])

    setup.install_grub(config_data["disk"], config_data["dualboot"])
    setup.configure_system(config_data["hostname"], config_data["locale"])
    setup.timezone(config_data["timezone"])
    setup.create_user(config_data["username"])
    setup.enable_services(config_data["enable_services"])
    
    setup.update_user_pacman_keys()
    setup.update_user_pacman_mirrors()
    setup.finish()

    Print.success("Installation complete\n")

    if args.reboot:
        Print.info("Rebooting...")
        run_cmd("reboot")

if __name__ == "__main__":
    main()