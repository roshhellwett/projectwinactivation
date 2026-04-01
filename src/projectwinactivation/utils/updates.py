"""
Windows Update Module
Check Windows update status and history
"""

import logging
from typing import Tuple, Optional
import subprocess

logger = logging.getLogger(__name__)


def check_update_status() -> Tuple[bool, str]:
    """
    Check Windows update status

    Returns:
        Tuple of (success, output)
    """
    try:
        result = subprocess.run(
            'systeminfo | findstr /C:"Update"',
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
            return True, "Could not retrieve update status via systeminfo"
    except Exception as e:
        logger.error(f"Failed to check update status: {e}")
        return False, str(e)


def get_update_history() -> Tuple[bool, str]:
    """
    Get Windows update history

    Returns:
        Tuple of (success, output)
    """
    try:
        result = subprocess.run(
            "wmic qfe list /format:table",
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
            return False, result.stderr or "Failed to get update history"
    except Exception as e:
        logger.error(f"Failed to get update history: {e}")
        return False, str(e)


def get_update_service_status() -> Tuple[bool, str]:
    """
    Get Windows Update service status

    Returns:
        Tuple of (success, output)
    """
    try:
        result = subprocess.run(
            "sc query wuauserv",
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
            return False, result.stderr or "Failed to get update service status"
    except Exception as e:
        logger.error(f"Failed to get update service status: {e}")
        return False, str(e)


def open_windows_update() -> Tuple[bool, str]:
    """
    Open Windows Update settings

    Returns:
        Tuple of (success, message)
    """
    try:
        import os

        os.system("start ms-settings:windowsupdate")
        return True, "Windows Update opened"
    except Exception as e:
        logger.error(f"Failed to open Windows Update: {e}")
        return False, str(e)


def check_pending_updates() -> Tuple[bool, str]:
    """
    Check for pending updates

    Returns:
        Tuple of (success, output)
    """
    try:
        ps_script = """
$Session = New-Object -ComObject Microsoft.Update.Session
$Searcher = $Session.CreateUpdateSearcher()
try {
    $Updates = $Searcher.Search("IsInstalled=0").Updates
    if ($Updates.Count -eq 0) {
        Write-Output "No pending updates found."
    } else {
        Write-Output "Pending updates: $($Updates.Count)"
        $Updates | ForEach-Object { Write-Output "  - $($_.Title)" }
    }
} catch {
    Write-Output "Error checking updates: $_"
}
"""
        result = subprocess.run(
            ["powershell.exe", "-Command", ps_script],
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
            return False, result.stderr or "Failed to check pending updates"
    except Exception as e:
        logger.error(f"Failed to check pending updates: {e}")
        return False, str(e)


def display_windows_update(console=None) -> None:
    """Display Windows Update interface"""
    if console:
        from rich.panel import Panel
        from rich.prompt import Prompt, Confirm

        console.print(
            Panel(
                "[bold cyan]Windows Update[/bold cyan]\n\n"
                "Check Windows update status and history.\n"
                "Options:\n"
                "  1. Check Update Status\n"
                "  2. View Update History\n"
                "  3. Update Service Status\n"
                "  4. Check Pending Updates\n"
                "  5. Open Windows Update Settings",
                title="[bold]Windows Update[/bold]",
                border_style="cyan",
                padding=(1, 2),
            )
        )

        choice = Prompt.ask(
            "\n[yellow]>> Select an option (1-5):[/yellow]", default="1"
        )

        console.print()

        if choice == "1":
            success, output = check_update_status()
        elif choice == "2":
            success, output = get_update_history()
        elif choice == "3":
            success, output = get_update_service_status()
        elif choice == "4":
            success, output = check_pending_updates()
        elif choice == "5":
            success, message = open_windows_update()
            console.print(
                Panel(
                    f"[green]✓ {message}[/green]\n\n"
                    "Windows Update settings should now be open.",
                    title="[bold green]Settings Opened[/bold green]",
                    border_style="green",
                )
            )
            Confirm.ask("\n[dim]Press Enter to continue...[/dim]", default=True)
            return
        else:
            success, output = check_update_status()

        if success:
            console.print(
                Panel(
                    f"[dim]{output[:4000]}[/dim]",
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
        print("  WINDOWS UPDATE")
        print("=" * 60)
        print()
        print("  1. Check Update Status")
        print("  2. View Update History")
        print("  3. Update Service Status")
        print("  4. Open Windows Update Settings")
        print()

        choice = input(">> Select option (1-4) [default=1]: ").strip() or "1"

        print()

        if choice == "1":
            success, output = check_update_status()
        elif choice == "2":
            success, output = get_update_history()
        elif choice == "3":
            success, output = get_update_service_status()
        else:
            success, output = check_update_status()

        print(output[:3000] if success else f"Error: {output}")


def handle_windows_update(console=None) -> None:
    """Main handler for Windows Update"""
    display_windows_update(console)
