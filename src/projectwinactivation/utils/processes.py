"""
Process Monitor Module
View and manage running processes
"""

import os
import logging
from typing import Tuple, List, Dict
from datetime import datetime

logger = logging.getLogger(__name__)


def format_bytes(size: int) -> str:
    """Format bytes to human readable format"""
    if size == 0:
        return "0 B"
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"


def list_processes() -> Tuple[bool, str]:
    """
    List all running processes

    Returns:
        Tuple of (success, output)
    """
    try:
        import subprocess

        result = subprocess.run(
            "tasklist /fo table /nh",
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
            encoding="utf-8",
            errors="replace",
        )

        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr or "Failed to list processes"
    except Exception as e:
        logger.error(f"Failed to list processes: {e}")
        return False, str(e)


def get_processes_by_memory() -> Tuple[bool, str]:
    """
    Get processes sorted by memory usage

    Returns:
        Tuple of (success, output)
    """
    try:
        import subprocess

        result = subprocess.run(
            "wmic process get ProcessId,WorkingSetSize,Name /format:table",
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
            encoding="utf-8",
            errors="replace",
        )

        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr or "Failed to get processes by memory"
    except Exception as e:
        logger.error(f"Failed to get processes by memory: {e}")
        return False, str(e)


def get_system_uptime() -> Tuple[bool, str]:
    """
    Get system uptime information

    Returns:
        Tuple of (success, output)
    """
    try:
        import subprocess

        result = subprocess.run(
            "systeminfo | findstr /C:'System Boot Time' /C:'Time Zone'",
            shell=True,
            capture_output=True,
            text=True,
            timeout=15,
            encoding="utf-8",
            errors="replace",
        )

        if result.returncode == 0:
            return True, result.stdout
        else:
            return True, "Could not get detailed uptime info"
    except Exception as e:
        logger.error(f"Failed to get system uptime: {e}")
        return False, str(e)


def kill_process(name: str = None, pid: int = None) -> Tuple[bool, str]:
    """
    Terminate a process by name or PID

    Args:
        name: Process name (e.g., "notepad.exe")
        pid: Process ID

    Returns:
        Tuple of (success, message)
    """
    try:
        import subprocess

        if pid:
            cmd = f"taskkill /f /pid {pid}"
        elif name:
            cmd = f"taskkill /f /im {name}"
        else:
            return False, "Either process name or PID must be provided"

        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=15,
            encoding="utf-8",
            errors="replace",
        )

        if result.returncode == 0:
            return True, f"Process terminated successfully"
        else:
            return False, result.stderr or "Failed to terminate process"
    except Exception as e:
        logger.error(f"Failed to kill process: {e}")
        return False, str(e)


def get_quick_system_info() -> Tuple[bool, str]:
    """
    Get quick system information

    Returns:
        Tuple of (success, output)
    """
    try:
        import subprocess

        result = subprocess.run(
            "systeminfo",
            shell=True,
            capture_output=True,
            text=True,
            timeout=60,
            encoding="utf-8",
            errors="replace",
        )

        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr or "Failed to get system info"
    except Exception as e:
        logger.error(f"Failed to get quick system info: {e}")
        return False, str(e)


def display_process_monitor(console=None) -> None:
    """Display process monitor interface"""
    if console:
        from rich.panel import Panel
        from rich.table import Table
        from rich.prompt import Prompt, Confirm

        console.print(
            Panel(
                "[bold cyan]Process Monitor[/bold cyan]\n\n"
                "View and manage running processes.\n"
                "Options:\n"
                "  1. Running Processes\n"
                "  2. Top by Memory\n"
                "  3. System Uptime\n"
                "  4. Quick System Info\n"
                "  5. Kill Process",
                title="[bold]Process Monitor[/bold]",
                border_style="cyan",
                padding=(1, 2),
            )
        )

        choice = Prompt.ask(
            "\n[yellow]>> Select an option (1-5):[/yellow]", default="1"
        )

        console.print()

        if choice == "1":
            success, output = list_processes()
        elif choice == "2":
            success, output = get_processes_by_memory()
        elif choice == "3":
            success, output = get_system_uptime()
        elif choice == "4":
            console.print("[yellow]Gathering system information...[/yellow]")
            success, output = get_quick_system_info()
        elif choice == "5":
            process_input = Prompt.ask("\n[yellow]Enter process name or PID:[/yellow]")

            if process_input.isdigit():
                success, message = kill_process(pid=int(process_input))
            else:
                success, message = kill_process(name=process_input)

            console.print(
                Panel(
                    f"[green]✓ {message}[/green]"
                    if success
                    else f"[red]✗ {message}[/red]",
                    title="[bold]Result[/bold]",
                    border_style="green" if success else "red",
                )
            )
            Confirm.ask("\n[dim]Press Enter to continue...[/dim]", default=True)
            return
        else:
            success, output = list_processes()

        if success:
            if choice == "2":
                console.print(
                    Panel(
                        f"[dim]{output[:4000]}[/dim]",
                        title="[bold]Processes by Memory[/bold]",
                        border_style="cyan",
                    )
                )
            else:
                console.print(
                    Panel(
                        f"[dim]{output[:3000]}[/dim]",
                        title="[bold]Result[/bold]",
                        border_style="cyan",
                    )
                )
        else:
            console.print(
                Panel(
                    f"[red]✗ {output}[/red]",
                    title="[bold red]Error[/bold red]",
                    border_style="red",
                )
            )

        Confirm.ask("\n[dim]Press Enter to continue...[/dim]", default=True)

    else:
        print("\n" + "=" * 60)
        print("  PROCESS MONITOR")
        print("=" * 60)
        print()
        print("  1. Running Processes")
        print("  2. Top by Memory")
        print("  3. System Uptime")
        print("  4. Quick System Info")
        print("  5. Kill Process")
        print()

        choice = input(">> Select option (1-5) [default=1]: ").strip() or "1"

        print()

        if choice == "1":
            success, output = list_processes()
        elif choice == "2":
            success, output = get_processes_by_memory()
        elif choice == "3":
            success, output = get_system_uptime()
        elif choice == "4":
            success, output = get_quick_system_info()
        else:
            success, output = list_processes()

        print(output[:3000] if success else f"Error: {output}")


def handle_process_monitor(console=None) -> None:
    """Main handler for process monitor"""
    display_process_monitor(console)
