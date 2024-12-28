import json
from utils.logger import Print
from utils.debug import Debug
from modules import disk, check, packages, setup

def load_config(file_path):
    with open("configs/" + file_path + ".json", "r") as f:
        return json.load(f)

def test_installation():
    Print.info("Running in test mode...")

    config_data = load_config("standart")
    Print.info(f"Loaded test config: {config_data}")

    disk.format_partitions(config_data["disk"])
    disk.mount_partitions(config_data["disk"])

    packages.install_packages(config_data["packages"])

    setup.configure_system(config_data["hostname"], config_data["locale"])
    setup.finish()

    Print.success("\nInstallation complete\n")

if __name__ == "__main__":
    test_installation()
