# projectwinactivation

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-0078D6?style=flat&logo=windows)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Version](https://img.shields.io/badge/version-1.0.0-orange.svg)

**A powerful Windows utility toolkit for system management, diagnostics, and optimization.**

</div>

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage Guide](#usage-guide)
- [Menu Options](#menu-options)
- [System Requirements](#system-requirements)
- [License](#license)
- [Contributing](#contributing)
- [Security](#security)
- [Support](#support)

---

## Overview

**projectwinactivation** is a comprehensive Windows utility toolkit that provides essential system management tools through an intuitive interactive menu interface. Whether you need to check system information, manage drivers, clean disk space, or diagnose network issues, this toolkit has you covered.

### Key Highlights

- **All-in-One Solution** — 11 essential Windows utilities in a single package
- **User-Friendly Interface** — Interactive menu with numbered options
- **Premium CLI Experience** — Beautiful terminal output with rich formatting
- **No Dependencies Hassle** — Works out of the box with minimal setup
- **Regular Updates** — Active maintenance and improvements

---

## Features

| # | Feature | Description |
|:-:|---------|-------------|
| 1 | **Windows Activation** | Activate Windows OS with proper disclaimer and consent |
| 2 | **System Info** | View comprehensive system information |
| 3 | **Driver Manager** | List and manage device drivers |
| 4 | **Service Manager** | Windows services control |
| 5 | **Startup Manager** | Manage startup programs |
| 6 | **Disk Cleanup** | Clean temp files and analyze disk space |
| 7 | **Network Diagnostics** | IP config, ping, DNS lookup |
| 8 | **Windows Update** | Check update status and history |
| 9 | **Product Key Finder** | Retrieve Windows product key |
| 10 | **Firewall Manager** | View firewall rules |
| 11 | **Process Monitor** | View and manage running processes |

---

## Quick Start

### One-Line Installation

```bash
pip install projectwinactivation
```

### Run the Toolkit

```bash
python -m projectwinactivation start
```

**That's it!** An interactive menu will appear with all available options.

---

## Installation

### Method 1: Install from PyPI (Recommended)

```bash
pip install projectwinactivation
```

### Method 2: Install from Source

```bash
# Clone the repository
git clone https://github.com/zenithopensourceprojects/projectwinactivation.git
cd projectwinactivation

# Install the package
pip install .
```

---

## Usage Guide

### Starting the Application

After installation, you can start the toolkit using any of these methods:

```bash
# Method 1: Using Python module (recommended)
python -m projectwinactivation start

# Method 2: Using installed command (if PATH is configured)
projectwinactivation start

# Method 3: Direct execution
python -m projectwinactivation
```

### Interactive Menu Navigation

1. **Launch the application** — The main menu displays all 14 options
2. **Enter your choice** — Type a number (1-14) and press Enter
3. **Follow prompts** — Each utility guides you with clear instructions
4. **Return to menu** — Press Enter after completing any action

### Command-Line Options

| Command | Description |
|---------|-------------|
| `python -m projectwinactivation start` | Launch interactive menu |
| `python -m projectwinactivation --help` | Show help message |
| `python -m projectwinactivation --version` | Show version info |
| `python -m projectwinactivation version` | Show version info (alternate) |
| `python -m projectwinactivation info` | Show detailed toolkit information |

---

## Menu Options

### 1. Windows Activation
Activates Windows using the official activation script. Shows a clear disclaimer and requires user consent before proceeding.

```
Disclaimer:
- For educational and personal use only
- Use only on systems you own or have license for
- Use at your own risk
```

### 2. System Info
Displays comprehensive system information including:
- Computer name and username
- Operating system details and build number
- Architecture and processor information
- Total RAM
- GPU information
- Disk space usage

### 3. Driver Manager
- List all installed drivers
- Export driver list to file
- View driver statistics

### 4. Service Manager
- View all Windows services
- Filter by state (running/stopped)
- Start or stop services

### 5. Startup Manager
- List startup programs
- Add or remove startup entries
- View scheduled tasks

### 6. Disk Cleanup
- Analyze disk space usage
- Clean temporary files
- View detailed drive information

### 7. Network Diagnostics
- Display IP configuration
- View network adapters
- Check WiFi connection status
- Ping tests to any host
- DNS lookup
- Flush DNS cache

### 8. Windows Update
- Check update status
- View update history
- Check service status
- Check for pending updates
- Open Windows Update settings

### 9. Product Key Finder
- Retrieve your Windows product key
- View license status
- Display OS edition information

### 10. Firewall Manager
- View firewall status for all profiles
- View inbound rules
- View outbound rules
- Search firewall rules

### 11. Process Monitor
- List all running processes
- View processes sorted by memory usage
- Check system uptime
- View quick system information
- Terminate processes

### 12. Update
Checks for package updates from PyPI and guides you through the upgrade process.

### 13. Help
Displays all available commands and usage instructions.

### 14. Exit
Gracefully exits the application with a thank you message.

---

## System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| **Operating System** | Windows 10 | Windows 11 |
| **Python Version** | 3.10 | 3.11 or 3.12 |
| **Administrator Rights** | Required for some features | Yes |
| **Internet Connection** | Optional | Required for activation |

### Features Requiring Administrator Privileges

Some features require elevated permissions:
- Windows Activation
- Service Management (start/stop)
- Startup Program Management
- Firewall Rules Viewing
- Process Termination

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `typer` | >=0.12 | CLI framework |
| `rich` | >=13.0 | Rich terminal output |

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for full details.

---

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](contributing.md) for detailed information on:
- Development setup
- Coding standards
- Pull request process
- Code review criteria

---

## Security

Please read our [Security Policy](security.md) for important information about security practices.

### Important Notes

- Some features require administrator privileges — use responsibly
- Windows Activation tool is for educational purposes only
- Always use activation tools on systems you own or have license for
- The developers are not responsible for misuse of this software

---

## Support

| Channel | Link |
|----------|------|
| **Issues** | [GitHub Issues](https://github.com/zenithopensourceprojects/projectwinactivation/issues) |
| **Documentation** | Use `python -m projectwinactivation --help` |
| **Email** | roshhellwett@icloud.com |

---

<div align="center">

**Made with care by [Zenith Open Source Projects](https://zenithopensourceprojects.vercel.app/)**

**Developer:** [roshhellwett](https://github.com/roshhellwett)

**Copyright © 2026** | All Rights Reserved

</div>
