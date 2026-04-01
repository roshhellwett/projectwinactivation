"""
Driver Manager Module
Lists, exports, and manages device drivers
"""

import os
import re
import logging
from typing import List, Dict, Tuple, Optional
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


def list_drivers(verbose: bool = False) -> Tuple[bool, str]:
    """
    List all installed drivers

    Args:
        verbose: Include detailed output

    Returns:
        Tuple of (success, output)
    """
    try:
        import subprocess

        cmd = "pnputil /enum-drivers"
        if verbose:
            cmd += " /v"

        result = subprocess.run(
            cmd,
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
            return False, result.stderr or "Failed to enumerate drivers"
    except Exception as e:
        logger.error(f"Failed to list drivers: {e}")
        return False, str(e)


def get_driver_count() -> int:
    """Get the count of installed driver packages"""
    success, output = list_drivers()
    if success:
        return output.count("Published Name")
    return 0


def export_driver_list(filepath: Optional[str] = None) -> Tuple[bool, str]:
    """
    Export driver list to a file

    Args:
        filepath: Output file path (default: Desktop/DriverList_Export.txt)

    Returns:
        Tuple of (success, message)
    """
    try:
        success, output = list_drivers(verbose=True)

        if not success:
            return False, output

        if filepath is None:
            desktop = Path.home() / "Desktop"
            filepath = str(
                desktop
                / f"DriverList_Export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            )

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write("  DRIVER LIST EXPORT\n")
            f.write(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            f.write(output)

        return True, f"Driver list exported to: {filepath}"
    except Exception as e:
        logger.error(f"Failed to export drivers: {e}")
        return False, str(e)


def get_driver_statistics() -> Dict[str, any]:
    """Get driver statistics"""
    success, output = list_drivers()

    if not success:
        return {"total": 0, "error": output}

    count = output.count("Published Name")

    inbox = output.count("Inbox")
    third_party = count - inbox if inbox > 0 else count

    return {
        "total": count,
        "inbox": inbox,
        "third_party": third_party,
        "output": output[:2000] if len(output) > 2000 else output,
    }


def display_driver_manager(console=None) -> None:
    """Display driver manager interface"""
    if console:
        from rich.panel import Panel
        from rich.table import Table
        from rich.prompt import Prompt, Confirm

        console.print(
            Panel(
                "[bold cyan]Driver Manager[/bold cyan]\n\n"
                "Manage and view installed device drivers.\n"
                "Options:\n"
                "  1. List Installed Drivers\n"
                "  2. Export Driver List\n"
                "  3. Driver Statistics",
                title="[bold]Driver Manager[/bold]",
                border_style="cyan",
                padding=(1, 2),
            )
        )

        choice = Prompt.ask(
            "\n[yellow]>> Select an option (1-3) or press Enter to list drivers:[/yellow]",
            default="1",
        )

        console.print()

        if choice == "2":
            success, message = export_driver_list()
            if success:
                console.print(
                    Panel(
                        f"[green]✓ {message}[/green]",
                        title="[bold green]Success[/bold green]",
                        border_style="green",
                    )
                )
            else:
                console.print(
                    Panel(
                        f"[red]✗ {message}[/red]",
                        title="[bold red]Error[/bold red]",
                        border_style="red",
                    )
                )

        elif choice == "3":
            stats = get_driver_statistics()

            stat_table = Table(
                title="[bold]Driver Statistics[/bold]", show_header=False, box=None
            )
            stat_table.add_column("Property", style="yellow", width=20)
            stat_table.add_column("Value", style="white")

            stat_table.add_row("Total Driver Packages", str(stats.get("total", 0)))
            stat_table.add_row("Inbox Drivers", str(stats.get("inbox", 0)))
            stat_table.add_row("Third-Party Drivers", str(stats.get("third_party", 0)))

            console.print(stat_table)

        else:
            success, output = list_drivers()
            if success:
                console.print(
                    Panel(
                        f"[dim]{output[:4000]}[/dim]",
                        title="[bold]Installed Drivers[/bold]",
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
        print("  DRIVER MANAGER")
        print("=" * 60)
        print()
        print("  1. List Installed Drivers")
        print("  2. Export Driver List")
        print("  3. Driver Statistics")
        print()

        choice = input(">> Select option (1-3) [default=1]: ").strip() or "1"

        print()

        if choice == "2":
            success, message = export_driver_list()
            print(f"  {'✓' if success else '✗'} {message}")
        elif choice == "3":
            stats = get_driver_statistics()
            print(f"  Total Drivers: {stats.get('total', 0)}")
            print(f"  Inbox Drivers: {stats.get('inbox', 0)}")
            print(f"  Third-Party: {stats.get('third_party', 0)}")
        else:
            success, output = list_drivers()
            print(output[:3000] if success else f"Error: {output}")


def handle_driver_manager(console=None) -> None:
    """Main handler for driver manager"""
    display_driver_manager(console)
