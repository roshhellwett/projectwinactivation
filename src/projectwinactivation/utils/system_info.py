"""
System Information Module
Retrieves and displays comprehensive system information
"""

import platform
import os
import re
import logging
from typing import Dict, List, Tuple, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


def get_computer_name() -> str:
    """Get the computer name"""
    return platform.node()


def get_username() -> str:
    """Get the current username"""
    try:
        return os.getlogin()
    except Exception:
        return os.environ.get("USERNAME", "Unknown")


def get_os_info() -> Dict[str, str]:
    """Get operating system information"""
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
    }


def get_os_name() -> str:
    """Get the full OS name"""
    try:
        import subprocess

        result = subprocess.run(
            [
                "powershell.exe",
                "-Command",
                "(Get-CimInstance Win32_OperatingSystem).Caption",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception as e:
        logger.warning(f"Could not get OS name: {e}")
    return f"{platform.system()} {platform.release()}"


def get_os_build() -> str:
    """Get OS build number"""
    try:
        import subprocess

        result = subprocess.run(
            [
                "powershell.exe",
                "-Command",
                "(Get-CimInstance Win32_OperatingSystem).BuildNumber",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass
    return platform.version()


def get_total_ram() -> float:
    """Get total RAM in GB"""
    try:
        import subprocess

        result = subprocess.run(
            [
                "powershell.exe",
                "-Command",
                "(Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0 and result.stdout.strip():
            return round(float(result.stdout.strip()), 2)
    except Exception as e:
        logger.warning(f"Could not get RAM: {e}")
    return 0.0


def get_boot_time() -> Optional[str]:
    """Get system boot time"""
    try:
        import subprocess

        result = subprocess.run(
            [
                "powershell.exe",
                "-Command",
                "(Get-CimInstance Win32_OperatingSystem).LastBootUpTime | Get-Date -Format 'yyyy-MM-dd HH:mm:ss'",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass
    return None


def get_uptime() -> str:
    """Get system uptime"""
    try:
        import subprocess

        result = subprocess.run(
            [
                "powershell.exe",
                "-Command",
                "((Get-Date) - (Get-CimInstance Win32_OperatingSystem).LastBootUpTime).ToString('d\\.hh\\:mm\\:ss')",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass

    try:
        import time

        boot_time = os.path.getmtime("C:\\Windows")
        uptime_seconds = int(time.time() - boot_time)
        days = uptime_seconds // 86400
        hours = (uptime_seconds % 86400) // 3600
        mins = (uptime_seconds % 3600) // 60
        return f"{days}d {hours}h {mins}m"
    except Exception:
        return "Unknown"


def get_gpu_info() -> List[Dict[str, str]]:
    """Get GPU information"""
    gpus = []
    try:
        import subprocess

        result = subprocess.run(
            [
                "powershell.exe",
                "-Command",
                "Get-CimInstance Win32_VideoController | Select-Object Name, AdapterRAM, DriverVersion | ConvertTo-Json -Compress",
            ],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode == 0 and result.stdout.strip():
            import json

            try:
                data = json.loads(result.stdout.strip())
                if isinstance(data, dict):
                    data = [data]
                for gpu in data:
                    ram = gpu.get("AdapterRAM", 0)
                    if ram:
                        ram = f"{ram / (1024**3):.2f} GB"
                    else:
                        ram = "N/A"
                    gpus.append(
                        {
                            "name": gpu.get("Name", "Unknown"),
                            "memory": ram,
                            "driver": gpu.get("DriverVersion", "Unknown"),
                        }
                    )
            except json.JSONDecodeError:
                pass
    except Exception as e:
        logger.warning(f"Could not get GPU info: {e}")
    return gpus


def get_disk_info() -> List[Dict[str, str]]:
    """Get disk information"""
    disks = []
    try:
        import subprocess

        result = subprocess.run(
            [
                "powershell.exe",
                "-Command",
                "Get-CimInstance Win32_LogicalDisk -Filter 'DriveType=3' | Select-Object DeviceID, Size, FreeSpace | ConvertTo-Json -Compress",
            ],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode == 0 and result.stdout.strip():
            import json

            try:
                data = json.loads(result.stdout.strip())
                if isinstance(data, dict):
                    data = [data]
                for disk in data:
                    total = int(disk.get("Size", 0))
                    free = int(disk.get("FreeSpace", 0))
                    used = total - free
                    pct = (used / total * 100) if total else 0
                    disks.append(
                        {
                            "drive": disk.get("DeviceID", "Unknown"),
                            "total": format_bytes(total),
                            "free": format_bytes(free),
                            "used": format_bytes(used),
                            "percent": f"{pct:.1f}%",
                        }
                    )
            except (json.JSONDecodeError, ValueError):
                pass
    except Exception as e:
        logger.warning(f"Could not get disk info: {e}")
    return disks


def format_bytes(size: int) -> str:
    """Format bytes to human readable format"""
    if size == 0:
        return "0 B"
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"


def get_system_info_dict() -> Dict:
    """Get all system information as a dictionary"""
    return {
        "computer_name": get_computer_name(),
        "username": get_username(),
        "os_name": get_os_name(),
        "os_build": get_os_build(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "total_ram": f"{get_total_ram()} GB",
        "uptime": get_uptime(),
        "boot_time": get_boot_time(),
        "gpu": get_gpu_info(),
        "disks": get_disk_info(),
    }


def display_system_info(console=None) -> None:
    """Display system information with premium formatting"""
    info = get_system_info_dict()

    if console:
        from rich.table import Table
        from rich.panel import Panel
        from rich.text import Text

        console.print(
            Panel(
                "[bold cyan]Gathering system information...[/bold cyan]",
                title="[bold]System Info[/bold]",
                border_style="cyan",
            )
        )

        console.print("\n")

        basic_table = Table(
            title="[bold]Basic Information[/bold]",
            show_header=True,
            header_style="bold cyan",
            box=None,
        )
        basic_table.add_column("Property", style="yellow", width=20)
        basic_table.add_column("Value", style="white")

        basic_table.add_row("Computer Name", info["computer_name"])
        basic_table.add_row("Username", info["username"])
        basic_table.add_row("OS", info["os_name"])
        basic_table.add_row("Build", info["os_build"])
        basic_table.add_row("Version", info["os_version"])
        basic_table.add_row("Architecture", info["architecture"])
        basic_table.add_row(
            "Processor",
            info["processor"][:60] + "..."
            if len(info["processor"]) > 60
            else info["processor"],
        )
        basic_table.add_row("Total RAM", info["total_ram"])
        basic_table.add_row("Uptime", info["uptime"])

        console.print(basic_table)

        if info["disks"]:
            console.print("\n")
            disk_table = Table(
                title="[bold]Disk Information[/bold]",
                show_header=True,
                header_style="bold cyan",
                box=None,
            )
            disk_table.add_column("Drive", style="yellow", width=8)
            disk_table.add_column("Total", style="white", width=12)
            disk_table.add_column("Used", style="red", width=12)
            disk_table.add_column("Free", style="green", width=12)
            disk_table.add_column("Usage", style="magenta", width=8)

            for disk in info["disks"]:
                disk_table.add_row(
                    disk["drive"],
                    disk["total"],
                    disk["used"],
                    disk["free"],
                    disk["percent"],
                )

            console.print(disk_table)

        if info["gpu"]:
            console.print("\n")
            gpu_table = Table(
                title="[bold]GPU Information[/bold]",
                show_header=True,
                header_style="bold cyan",
                box=None,
            )
            gpu_table.add_column("GPU", style="white")
            gpu_table.add_column("Memory", style="yellow", width=12)
            gpu_table.add_column("Driver", style="dim", width=15)

            for gpu in info["gpu"]:
                gpu_table.add_row(gpu["name"], gpu["memory"], gpu["driver"])

            console.print(gpu_table)

    else:
        print("\n" + "=" * 60)
        print("  SYSTEM INFORMATION")
        print("=" * 60)
        print()
        print(f"  Computer Name:  {info['computer_name']}")
        print(f"  Username:       {info['username']}")
        print(f"  OS:             {info['os_name']}")
        print(f"  Build:          {info['os_build']}")
        print(f"  Version:        {info['os_version']}")
        print(f"  Architecture:   {info['architecture']}")
        print(f"  Processor:      {info['processor']}")
        print(f"  Total RAM:      {info['total_ram']}")
        print(f"  Uptime:         {info['uptime']}")
        print()

        if info["disks"]:
            print("  Disk Information:")
            print("  " + "-" * 50)
            for disk in info["disks"]:
                print(
                    f"    {disk['drive']} Total: {disk['total']} | Used: {disk['used']} | Free: {disk['free']} ({disk['percent']})"
                )
            print()

        if info["gpu"]:
            print("  GPU Information:")
            print("  " + "-" * 50)
            for gpu in info["gpu"]:
                print(f"    {gpu['name']} | {gpu['memory']} | Driver: {gpu['driver']}")
            print()


def handle_system_info(console=None) -> None:
    """Main handler for system info module"""
    display_system_info(console)
    if console:
        from rich.prompt import Confirm

        Confirm.ask("\n[dim]Press Enter to continue...[/dim]", default=True)
