![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-0078D6?style=flat&logo=windows)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Version](https://img.shields.io/badge/version-1.0.1-orange.svg)

# PROJECT WIN ACTIVATION

comprehensive Windows utility toolkit that provides essential system management tools through an intuitive interactive menu interface. Whether you need to check system information, manage drivers, clean disk space, or diagnose network issues, this toolkit has you covered.

![SAMPLE](https://github.com/roshhellwett/projectwinactivation/blob/68ced43768519df5b91fd6119449b68fd38c6c92/sample/sample.png)

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

© 2026 [Zenith Open Source Projects](https://zenithopensourceprojects.vercel.app/). All Rights Reserved. Zenith is a Open Source Project Idea's by @roshhellwett
