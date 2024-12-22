# Arch Installer

Arch Installer is a Python-based utility for automating the installation of Arch Linux. The tool provides options for full installation or installation without configuring disk layouts, while allowing user customization of configuration parameters.
!!! This project is not yet designed to be installed on other devices.

## Requirements

- Python 3.8+
- Arch Linux ISO or a suitable environment

## Installation

1. Clone the repository:
```bash
git clone https://github.com/gdbLife/arch.git
cd arch-installer
```
2. Install
```bash
python main.py --customize --config my
```

### Debug Mode

Enable detailed logging with the `--debug` flag:
```bash
python main.py --config minimal --debug
```

## Configuration

You can customize installation parameters using JSON files (e.g., `standard.json`, `minimal.json`). For example:

```json
{
  "disk": "/dev/sda",
  "hostname": "arch-system",
  "username": "user",
  "locale": "en_US.UTF-8"
}
```

## Project Structure

- `main.py`: Entry point for the application.
- `utils/`: Utility functions (e.g., `run_cmd`).
- `modules/`: Core functionalities (e.g., disk management, setup).

## Development

### Testing in Docker

To test the installer without affecting your system, use Docker:
```bash
docker build -t arch-installer .
docker run -it --privileged arch-installer
```
```bash
python main.py --docker
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
