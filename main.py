import argparse
import json
from modules.utils import Print
from modules import config, disk, check, packages, setup

def load_config(file_path):
    with open("configs/" + file_path + ".json", "r") as f:
        return json.load(f)

def customize_config(config):
    config["disk"] = Print.input(f"Disk [{config.get('disk', '/dev/sda')}]: ") or config["disk"]
    config["hostname"] = Print.input(f"Hostname [{config.get('hostname', 'archlinux')}]: ") or config["hostname"]
    config["username"] = Print.input(f"Username [{config.get('username', 'user')}]: ") or config["username"]

    packages = Print.input(f"Add packages (comma-separated) [{', '.join(config.get('packages', []))}]: ")
    if packages:
        config["packages"].extend(packages.split(","))

    services = Print.input(f"Enable services (comma-separated) [{', '.join(config.get('enable_services', []))}]: ")
    if services:
        config["enable_services"].extend(services.split(","))

    return config

def print_config_data(config_data):
    Print.info(f"Disk: {config_data["disk"]}")
    Print.info(f"Hostname: {config_data["hostname"]}")
    Print.info(f"Username: {config_data["username"]}")
    Print.info(f"Packages: {config_data["packages"]}")
    Print.info(f"Services: {config_data["enable_services"]}")
    print()

# config.DEBUG = Print.input("Print debug information? (yes/no) ").lower() == "yes"
# if not config.DEBUG:
#     Print.info("Debug skipped")

parser = argparse.ArgumentParser(description="Arch Installer: auto isntall Arch Linux")
parser.add_argument("--config", type=str, help="Path to configuration file")
parser.add_argument("--customize", action="store_true", help="Customize configuration")
parser.add_argument("--debug", action="store_true", help="Show debug information")
parser.add_argument("--docker", action="store_true", help="Argument for testing in docker")
args = parser.parse_args()

if args.config:
    config_data = load_config(args.config)
    print_config_data(config_data)

    if args.debug:
        config.DEBUG = True
    
    if args.customize:
        config_data = customize_config(config_data)
else:
    Print.error("No configuration file provided. Use --config to specify a configuration")
    exit(1)

disk.partition_disks(config_data["disk"])
disk.mount_disks(config_data["disk"])

check.pacman_keys()
check.pacman_mirrors()

packages.install_packages(config_data["packages"])

if not args.docker:
    setup.install_grub(config_data["disk"])
setup.configure_system(config_data["hostname"])
setup.create_user(config_data["username"])
setup.enable_services(config_data["enable_services"])
setup.finish()
    