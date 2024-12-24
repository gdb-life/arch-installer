# Arch Installer

Arch Installer is a Python-based utility for automating the installation of Arch Linux. The tool provides options for full installation or installation without configuring disk layouts, while allowing user customization of configuration parameters.

## Disclaimer

This project is not yet designed to be installed on other devices.

## Requirements

- Python 3.8+
- Arch Linux ISO or a suitable environment

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/gdb-life/arch.git
   cd arch-installer
   ```

2. Run the installer with customization and configuration:
   ```bash
   ./install --customize --config standart
   ```

### Debug Mode

Enable detailed logging with the `--debug` flag:
   ```bash
   ./install --config minimal --debug
   ```

## Configuration

You can customize installation parameters using JSON files (e.g., `standard.json`, `minimal.json`). For example:

```json
{
  "disk": "/dev/sda",
  "hostname": "arch",
  "username": "user",
  "locale": "en_US.UTF-8"
}
```

## Project Structure

- `main.py`: Entry point for the application.
- `utils/`: Utility functions (e.g., `run_cmd`).
- `modules/`: Core functionalities (e.g., disk management, setup).
- `configs/`: JSON configuration files for installation setups.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
