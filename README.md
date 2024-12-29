# Arch Installer

A Python-based utility for automating Arch Linux installation. This tool streamlines the installation process while providing flexibility for customization through configuration files.

## Features

- Full automated installation
- Configurable disk partitioning
- Package selection and configuration
- System setup automation
- Debug mode for detailed logging

## Requirements

- Python 3.8+
- Arch Linux live environment
- Internet connection
- UEFI mode
- gpt partition table

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/gdb-life/arch-installer.git
   cd arch-installer
   ```

2. Basic installation with standard config:
   ```bash
   ./install standart 
   ```

3. Installation with customization:
   ```bash
   ./install standart --custom
   ```

4. Create and save a custom configuration:
   ```bash
   ./install --custom --write myconfig
   ```
   This will create a new configuration file at `configs/myconfig.json`

Enable detailed logging with the `--debug` flag:
   ```bash
   ./install standart --debug
   ```

## Configuration

You can customize installation parameters using JSON files (e.g., `standard.json`, `minimal.json`). Create your own configuration by using the `--custom` and `--write` flags together, which will guide you through the configuration process and save the result to a new JSON file.

## Project Structure

- `main.py`: Entry point for the application.
- `utils/`: Utility functions (e.g., `run_cmd`, `Print`).
- `modules/`: Core functionalities (e.g., disk management, setup).
- `configs/`: JSON configuration files for installation setups.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
