"""
CLI Module for projectwinactivation
Main command-line interface with premium menu system
"""

import sys
import os
import logging
import time
import subprocess
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn

from projectwinactivation import __version__
from projectwinactivation.assets.banners import MAIN_BANNER, EXIT_BANNER

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = typer.Typer(
    help="projectwinactivation - Powerful Windows utility toolkit",
    add_completion=False,
    invoke_without_command=True,
)
console = Console()


@app.callback()
def callback():
    """Show the main menu when no command is specified"""
    pass


def print_banner(animate: bool = False) -> None:
    """Print the main banner with optional animation"""
    if animate:
        for line in MAIN_BANNER.split("\n"):
            console.print(f"[bold cyan]{line}[/bold cyan]")
            time.sleep(0.02)
    else:
        console.print(f"[bold cyan]{MAIN_BANNER}[/bold cyan]")


def print_version() -> None:
    """Print version information"""
    console.print(
        Panel(
            "[bold cyan]projectwinactivation[/bold cyan] version "
            + __version__
            + "\n\n"
            "[dim]Powerful Windows utility toolkit[/dim]\n\n"
            "[yellow]Features:[/yellow]\n"
            "  * Windows Activation\n"
            "  * System Information\n"
            "  * Driver Management\n"
            "  * Service Management\n"
            "  * Startup Management\n"
            "  * Disk Cleanup\n"
            "  * Network Diagnostics\n"
            "  * Windows Update\n"
            "  * Product Key Finder\n"
            "  * Firewall Management\n"
            "  * Process Monitoring\n\n"
            "[dim]--------------------------------------------------[/dim]\n"
            "[dim]Copyright 2026 Zenith Open Source Projects[/dim]\n"
            "[dim]Developer: roshhellwett[/dim]",
            title="[bold cyan]projectwinactivation[/bold cyan]",
            border_style="cyan",
            padding=(1, 2),
        )
    )


def print_main_menu() -> str:
    """Display the main menu and get user choice"""
    console.clear()

    console.print(f"[bold cyan]{MAIN_BANNER}[/bold cyan]")

    console.print(
        Panel(
            "[yellow]============================================================[/yellow]\n\n"
            "[bold]Select an option:[/bold]\n\n"
            "[green]  1.[/green]  Windows Activation     - Activate Windows OS\n"
            "[green]  2.[/green]  System Info            - View system information\n"
            "[green]  3.[/green]  Driver Manager         - Manage device drivers\n"
            "[green]  4.[/green]  Service Manager        - Windows services control\n"
            "[green]  5.[/green]  Startup Manager         - Startup programs management\n"
            "[green]  6.[/green]  Disk Cleanup            - Disk space management\n"
            "[green]  7.[/green]  Network Diagnostics     - Network testing tools\n"
            "[green]  8.[/green]  Windows Update         - Update status & history\n"
            "[green]  9.[/green]  Product Key Finder     - Retrieve Windows key\n"
            "[green] 10.[/green]  Firewall Manager        - Firewall rules control\n"
            "[green] 11.[/green]  Process Monitor         - Running processes view\n"
            "[green] 12.[/green]  Update                  - Check for updates\n"
            "[green] 13.[/green]  Help                   - Show help & commands\n"
            "[green] 14.[/green]  Exit                   - Exit application\n\n"
            "[yellow]============================================================[/yellow]\n\n"
            "[dim]Copyright 2026 Zenith Open Source Projects | Developer: roshhellwett[/dim]",
            title="[bold cyan]Main Menu[/bold cyan]",
            border_style="cyan",
            padding=(1, 2),
        )
    )

    choice = Prompt.ask(
        "\n[bold yellow]>> Enter your choice (1-14):[/bold yellow]", default="1"
    )

    return choice.strip()


def show_main_menu() -> str:
    """Show main menu and return choice"""
    return print_main_menu()


def handle_activation() -> None:
    """Handle Windows Activation option"""
    from projectwinactivation.utils.activation import handle_activation

    handle_activation(console)


def handle_system_info() -> None:
    """Handle System Info option"""
    from projectwinactivation.utils.system_info import handle_system_info

    handle_system_info(console)


def handle_driver_manager() -> None:
    """Handle Driver Manager option"""
    from projectwinactivation.utils.drivers import handle_driver_manager

    handle_driver_manager(console)


def handle_service_manager() -> None:
    """Handle Service Manager option"""
    from projectwinactivation.utils.services import handle_service_manager

    handle_service_manager(console)


def handle_startup_manager() -> None:
    """Handle Startup Manager option"""
    from projectwinactivation.utils.startup import handle_startup_manager

    handle_startup_manager(console)


def handle_disk_cleanup() -> None:
    """Handle Disk Cleanup option"""
    from projectwinactivation.utils.disk import handle_disk_cleanup

    handle_disk_cleanup(console)


def handle_network_diag() -> None:
    """Handle Network Diagnostics option"""
    from projectwinactivation.utils.network import handle_network_diag

    handle_network_diag(console)


def handle_windows_update() -> None:
    """Handle Windows Update option"""
    from projectwinactivation.utils.updates import handle_windows_update

    handle_windows_update(console)


def handle_product_key_finder() -> None:
    """Handle Product Key Finder option"""
    from projectwinactivation.utils.product_key import handle_product_key_finder

    handle_product_key_finder(console)


def handle_firewall_manager() -> None:
    """Handle Firewall Manager option"""
    from projectwinactivation.utils.firewall import handle_firewall_manager

    handle_firewall_manager(console)


def handle_process_monitor() -> None:
    """Handle Process Monitor option"""
    from projectwinactivation.utils.processes import handle_process_monitor

    handle_process_monitor(console)


def handle_update() -> None:
    """Handle Update option - check for package updates"""
    console.print(
        Panel(
            "[bold cyan]Checking for updates...[/bold cyan]",
            title="[bold]Update Check[/bold]",
            border_style="cyan",
        )
    )

    try:
        result = subprocess.run(
            ["pip", "index", "versions", "projectwinactivation"],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            available_versions = []
            for line in lines:
                if "Available versions:" in line:
                    available_versions = (
                        line.replace("Available versions:", "").strip().split(", ")
                    )
                    break

            current_result = subprocess.run(
                ["pip", "show", "projectwinactivation"],
                capture_output=True,
                text=True,
                timeout=30,
            )

            current_version = "Unknown"
            for line in current_result.stdout.split("\n"):
                if line.startswith("Version:"):
                    current_version = line.replace("Version:", "").strip()
                    break

            latest_version = available_versions[-1] if available_versions else "Unknown"

            console.print()

            if current_version != latest_version and latest_version != "Unknown":
                console.print(
                    Panel(
                        "[yellow]Current version:[/yellow] " + current_version + "\n"
                        "[green]Latest version:[/green] " + latest_version + "\n\n"
                        "[bold yellow]A new version is available![/bold yellow]\n\n"
                        "To update, run: [cyan]pip install --upgrade projectwinactivation[/cyan]",
                        title="[bold yellow]Update Available[/bold yellow]",
                        border_style="yellow",
                    )
                )
            else:
                console.print(
                    Panel(
                        "[green]You're up to date![/green]\n\n"
                        "Current version: [cyan]" + current_version + "[/cyan]",
                        title="[bold green]No Updates[/bold green]",
                        border_style="green",
                    )
                )
        else:
            console.print(
                Panel(
                    "[yellow]Could not check for updates.[/yellow]\n\n"
                    "This may happen if the package is not yet published to PyPI.",
                    title="[bold yellow]Update Check Failed[/bold yellow]",
                    border_style="yellow",
                )
            )

    except FileNotFoundError:
        console.print(
            Panel(
                "[red]pip not found. Please ensure pip is installed.[/red]",
                title="[bold red]Error[/bold red]",
                border_style="red",
            )
        )
    except Exception as e:
        logger.error(f"Update check error: {e}")
        console.print(
            Panel(
                "[red]Error checking for updates: " + str(e) + "[/red]",
                title="[bold red]Error[/bold red]",
                border_style="red",
            )
        )

    Confirm.ask("\n[dim]Press Enter to continue...[/dim]", default=True)


def handle_help() -> None:
    """Handle Help option"""
    console.print(
        Panel(
            "[bold cyan]Help & Commands[/bold cyan]\n\n"
            "[yellow]Quick Commands:[/yellow]\n"
            "  [green]python -m projectwinactivation start[/green]    Start interactive menu\n"
            "  [green]python -m projectwinactivation --help[/green]  Show help\n"
            "  [green]python -m projectwinactivation --version[/green] Show version\n\n"
            "[yellow]Menu Options:[/yellow]\n"
            "  [cyan]  1[/cyan]  Windows Activation     - Activate Windows OS\n"
            "  [cyan]  2[/cyan]  System Info            - View system information\n"
            "  [cyan]  3[/cyan]  Driver Manager         - Manage device drivers\n"
            "  [cyan]  4[/cyan]  Service Manager        - Windows services control\n"
            "  [cyan]  5[/cyan]  Startup Manager         - Startup programs\n"
            "  [cyan]  6[/cyan]  Disk Cleanup            - Clean temporary files\n"
            "  [cyan]  7[/cyan]  Network Diagnostics     - Test network connectivity\n"
            "  [cyan]  8[/cyan]  Windows Update         - Check update status\n"
            "  [cyan]  9[/cyan]  Product Key Finder     - Get Windows product key\n"
            "  [cyan] 10[/cyan]  Firewall Manager        - View firewall rules\n"
            "  [cyan] 11[/cyan]  Process Monitor         - View running processes\n"
            "  [cyan] 12[/cyan]  Update                  - Check for package updates\n"
            "  [cyan] 13[/cyan]  Help                   - Show this help\n"
            "  [cyan] 14[/cyan]  Exit                   - Exit application\n\n"
            "[yellow]Notes:[/yellow]\n"
            "  [dim]* Some features require administrator privileges[/dim]\n"
            "  [dim]* Use the activation tool responsibly and only on systems you own[/dim]\n"
            "  [dim]* Press Ctrl+C anytime to exit[/dim]\n\n"
            "[dim]--------------------------------------------------[/dim]\n"
            "[dim]Copyright 2026 Zenith Open Source Projects | Developer: roshhellwett[/dim]",
            title="[bold cyan]Help & Commands[/bold cyan]",
            border_style="cyan",
            padding=(1, 2),
        )
    )

    Confirm.ask("\n[dim]Press Enter to continue...[/dim]", default=True)


def handle_exit() -> None:
    """Handle Exit option"""
    console.clear()

    console.print(f"[bold green]{EXIT_BANNER}[/bold green]")

    console.print(
        Panel(
            "[bold green]Thank you for using projectwinactivation![/bold green]\n\n"
            "[dim]We hope this toolkit was helpful for your Windows management needs.[/dim]\n\n"
            "[yellow]Stay productive and keep your systems optimized![/yellow]\n\n"
            "[dim]--------------------------------------------------[/dim]\n"
            "[dim]Copyright 2026 Zenith Open Source Projects | Developer: roshhellwett[/dim]",
            title="[bold green]Goodbye![/bold green]",
            border_style="green",
            padding=(1, 2),
        )
    )


def main_menu_loop() -> None:
    """Main menu loop - runs until user exits"""
    while True:
        try:
            choice = show_main_menu()

            if choice == "1":
                handle_activation()
            elif choice == "2":
                handle_system_info()
            elif choice == "3":
                handle_driver_manager()
            elif choice == "4":
                handle_service_manager()
            elif choice == "5":
                handle_startup_manager()
            elif choice == "6":
                handle_disk_cleanup()
            elif choice == "7":
                handle_network_diag()
            elif choice == "8":
                handle_windows_update()
            elif choice == "9":
                handle_product_key_finder()
            elif choice == "10":
                handle_firewall_manager()
            elif choice == "11":
                handle_process_monitor()
            elif choice == "12":
                handle_update()
            elif choice == "13":
                handle_help()
            elif choice == "14":
                handle_exit()
                break
            else:
                console.print(
                    Panel(
                        "[red]Invalid choice '"
                        + choice
                        + "'. Please enter a number between 1-14.[/red]",
                        title="[bold red]Invalid Input[/bold red]",
                        border_style="red",
                    )
                )
                time.sleep(1.5)

        except KeyboardInterrupt:
            console.print("\n")
            handle_exit()
            break
        except Exception as e:
            logger.error(f"Menu error: {e}")
            console.print(
                Panel(
                    "[red]An unexpected error occurred: " + str(e) + "[/red]\n\n"
                    "[dim]Please try again or restart the application.[/dim]",
                    title="[bold red]Error[/bold red]",
                    border_style="red",
                )
            )
            time.sleep(2)


@app.command()
def start():
    """Start interactive menu mode"""
    main_menu_loop()


@app.command()
def version():
    """Show version information"""
    print_version()


@app.command()
def info():
    """Show detailed information about the toolkit"""
    print_version()


if __name__ == "__main__":
    app()
