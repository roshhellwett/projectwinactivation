"""
Startup Manager Module
Manage Windows startup programs
"""

import logging
from typing import Tuple, List, Dict

logger = logging.getLogger(__name__)


def list_startup_programs(scope: str = "both") -> Tuple[bool, str]:
    """
    List startup programs

    Args:
        scope: Which startup locations to check (user, system, both)

    Returns:
        Tuple of (success, output)
    """
    try:
        import subprocess

        output_lines = []

        if scope in ("user", "both"):
            result = subprocess.run(
                'reg query "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" 2>nul',
                shell=True,
                capture_output=True,
                text=True,
                timeout=10,
                encoding="utf-8",
                errors="replace",
            )
            if result.stdout.strip():
                output_lines.append("=== CURRENT USER STARTUP ===")
                output_lines.append(result.stdout.strip())

        if scope in ("system", "both"):
            result = subprocess.run(
                'reg query "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" 2>nul',
                shell=True,
                capture_output=True,
                text=True,
                timeout=10,
                encoding="utf-8",
                errors="replace",
            )
            if result.stdout.strip():
                output_lines.append("=== SYSTEM-WIDE STARTUP ===")
                output_lines.append(result.stdout.strip())

        if output_lines:
            return True, "\n".join(output_lines)
        else:
            return True, "No startup programs found"
    except Exception as e:
        logger.error(f"Failed to list startup programs: {e}")
        return False, str(e)


def add_startup_program(name: str, path: str, scope: str = "user") -> Tuple[bool, str]:
    """
    Add a program to startup

    Args:
        name: Name of the startup entry
        path: Path to the program
        scope: user or system

    Returns:
        Tuple of (success, message)
    """
    try:
        import subprocess

        if scope == "user":
            cmd = f'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "{name}" /d "{path}" /f'
        else:
            cmd = f'reg add "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "{name}" /d "{path}" /f'

        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10,
            encoding="utf-8",
            errors="replace",
        )

        if result.returncode == 0:
            return True, f"Startup entry '{name}' added successfully"
        else:
            return False, result.stderr or f"Failed to add startup entry '{name}'"
    except Exception as e:
        logger.error(f"Failed to add startup program: {e}")
        return False, str(e)


def remove_startup_program(name: str, scope: str = "user") -> Tuple[bool, str]:
    """
    Remove a program from startup

    Args:
        name: Name of the startup entry to remove
        scope: user or system

    Returns:
        Tuple of (success, message)
    """
    try:
        import subprocess

        if scope == "user":
            cmd = f'reg delete "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "{name}" /f'
        else:
            cmd = f'reg delete "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "{name}" /f'

        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10,
            encoding="utf-8",
            errors="replace",
        )

        if result.returncode == 0:
            return True, f"Startup entry '{name}' removed successfully"
        else:
            return False, result.stderr or f"Failed to remove startup entry '{name}'"
    except Exception as e:
        logger.error(f"Failed to remove startup program: {e}")
        return False, str(e)


def list_scheduled_tasks() -> Tuple[bool, str]:
    """
    List scheduled tasks

    Returns:
        Tuple of (success, output)
    """
    try:
        import subprocess

        result = subprocess.run(
            "schtasks /query /fo LIST /v",
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
            return False, result.stderr or "Failed to list scheduled tasks"
    except Exception as e:
        logger.error(f"Failed to list scheduled tasks: {e}")
        return False, str(e)


def display_startup_manager(console=None) -> None:
    """Display startup manager interface"""
    if console:
        from rich.panel import Panel
        from rich.table import Table
        from rich.prompt import Prompt, Confirm

        console.print(
            Panel(
                "[bold cyan]Startup Manager[/bold cyan]\n\n"
                "Manage programs that run at Windows startup.\n"
                "Options:\n"
                "  1. List Startup Programs\n"
                "  2. Enable Startup Program\n"
                "  3. Disable Startup Program\n"
                "  4. List Scheduled Tasks",
                title="[bold]Startup Manager[/bold]",
                border_style="cyan",
                padding=(1, 2),
            )
        )

        choice = Prompt.ask(
            "\n[yellow]>> Select an option (1-4):[/yellow]", default="1"
        )

        console.print()

        if choice == "1":
            success, output = list_startup_programs()
        elif choice == "2":
            name = Prompt.ask("\n[yellow]Enter program name:[/yellow]")
            path = Prompt.ask("[yellow]Enter program path:[/yellow]")
            scope = Prompt.ask(
                "[yellow]Scope (user/system) [default=user]:[/yellow]", default="user"
            )
            success, message = add_startup_program(name, path, scope)
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
        elif choice == "3":
            name = Prompt.ask("\n[yellow]Enter program name to remove:[/yellow]")
            scope = Prompt.ask(
                "[yellow]Scope (user/system) [default=user]:[/yellow]", default="user"
            )
            success, message = remove_startup_program(name, scope)
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
        elif choice == "4":
            success, output = list_scheduled_tasks()
        else:
            success, output = list_startup_programs()

        if success:
            console.print(
                Panel(
                    f"[dim]{output[:3000]}[/dim]",
                    title="[bold]Startup Programs[/bold]",
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
        print("  STARTUP MANAGER")
        print("=" * 60)
        print()
        print("  1. List Startup Programs")
        print("  2. Enable Startup Program")
        print("  3. Disable Startup Program")
        print("  4. List Scheduled Tasks")
        print()

        choice = input(">> Select option (1-4) [default=1]: ").strip() or "1"

        print()

        if choice == "1":
            success, output = list_startup_programs()
        elif choice == "4":
            success, output = list_scheduled_tasks()
        else:
            return

        print(output[:3000] if success else f"Error: {output}")


def handle_startup_manager(console=None) -> None:
    """Main handler for startup manager"""
    display_startup_manager(console)
