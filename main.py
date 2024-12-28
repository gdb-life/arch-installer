import argparse
import json
from utils.commands import run_cmd
from utils.logger import Print
from utils.debug import Debug
from modules import disk, check, packages, setup

def load_config(file_path):
    with open("configs/" + file_path + ".json", "r") as f:
        return json.load(f)

def customize_config(config):
    config["disk"] = Print.input(f"Disk [{config.get('disk', '/dev/sda')}]: ") or config["disk"]
    config["hostname"] = Print.input(f"Hostname [{config.get('hostname', 'archlinux')}]: ") or config["hostname"]
    config["username"] = Print.input(f"Username [{config.get('username', 'user')}]: ") or config["username"]
    config["locale"] = Print.input(f"Locale [{config.get('locale', 'en_US')}]: ") or config["locale"]

    packages = Print.input(f"Add packages [{', '.join(config.get('packages', []))}]: ")
    if packages:
        config["packages"].extend(packages.split(","))

    services = Print.input(f"Enable services [{', '.join(config.get('enable_services', []))}]: ")
    if services:
        config["enable_services"].extend(services.split(","))

    return config

def print_config_data(config_data):
    Print.data("Disk:     ", config_data["disk"])
    Print.data("Hostname: ", config_data["hostname"])
    Print.data("Username: ", config_data["username"])
    Print.data("Packages: ", ", ".join(config_data["packages"]))
    Print.data("Locale:   ", config_data["locale"])
    Print.data("Services: ", ", ".join(config_data["enable_services"]))

def main():
    parser = argparse.ArgumentParser(description="Arch Installer: auto isntall Arch Linux")
    parser.add_argument("config", nargs="?", help="Name of the configuration file (without .json)")
    parser.add_argument("-c", "--custom", action="store_true", help="customize configuration")
    parser.add_argument("-p", "--print", action="store_true", help="print configuration")
    parser.add_argument("-d", "--debug", action="store_true", help="show debug information")
    parser.add_argument("-r", "--reboot", action="store_true", help="reboot after installation")
    args = parser.parse_args()

    if args.debug:
        Debug.DEBUG = True

    config_data = load_config("standart")

    if args.config:
        config_data = load_config(args.config)

    if args.custom:
        config_data = customize_config(config_data)

    if args.print:
        print_config_data(config_data)
        exit(0)

    check.check_dependencies()
    Print.info("The following updates will be made on the image")
    check.update_pacman_keys()
    check.update_pacman_mirrors()

    disk.markup_disk(config_data["disk"])
    disk.format_partitions(config_data["disk"])
    disk.mount_partitions(config_data["disk"])

    packages.install_packages(config_data["packages"])

    setup.install_grub(config_data["disk"])
    setup.configure_system(config_data["hostname"], config_data["locale"])
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