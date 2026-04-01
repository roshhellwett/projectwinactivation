"""
Service Manager Module
View and manage Windows services
"""

import logging
from typing import List, Dict, Tuple, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


def list_services(state: str = "all") -> Tuple[bool, str]:
    """
    List Windows services

    Args:
        state: Service state filter (all, running, stopped)

    Returns:
        Tuple of (success, output)
    """
    try:
        import subprocess

        state_map = {
            "all": "state= all",
            "running": "state= running",
            "stopped": "state= stopped",
        }

        cmd = f"sc query {state_map.get(state, state_map['all'])}"

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
            return False, result.stderr or "Failed to query services"
    except Exception as e:
        logger.error(f"Failed to list services: {e}")
        return False, str(e)


def get_service_details(service_name: str) -> Tuple[bool, str]:
    """
    Get detailed information about a specific service

    Args:
        service_name: Name of the service

    Returns:
        Tuple of (success, output)
    """
    try:
        import subprocess

        cmd = f'sc query "{service_name}"'

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
            return True, result.stdout
        else:
            return False, result.stderr or f"Service '{service_name}' not found"
    except Exception as e:
        logger.error(f"Failed to get service details: {e}")
        return False, str(e)


def start_service(service_name: str) -> Tuple[bool, str]:
    """
    Start a Windows service

    Args:
        service_name: Name of the service

    Returns:
        Tuple of (success, message)
    """
    try:
        import subprocess

        cmd = f'net start "{service_name}"'

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
            return True, f"Service '{service_name}' started successfully"
        else:
            return False, result.stderr or f"Failed to start service '{service_name}'"
    except Exception as e:
        logger.error(f"Failed to start service: {e}")
        return False, str(e)


def stop_service(service_name: str) -> Tuple[bool, str]:
    """
    Stop a Windows service

    Args:
        service_name: Name of the service

    Returns:
        Tuple of (success, message)
    """
    try:
        import subprocess

        cmd = f'net stop "{service_name}"'

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
            return True, f"Service '{service_name}' stopped successfully"
        else:
            return False, result.stderr or f"Failed to stop service '{service_name}'"
    except Exception as e:
        logger.error(f"Failed to stop service: {e}")
        return False, str(e)


def restart_service(service_name: str) -> Tuple[bool, str]:
    """
    Restart a Windows service

    Args:
        service_name: Name of the service

    Returns:
        Tuple of (success, message)
    """
    stop_success, stop_msg = stop_service(service_name)
    if not stop_success:
        return False, f"Could not stop service: {stop_msg}"

    return start_service(service_name)


def display_service_manager(console=None) -> None:
    """Display service manager interface"""
    if console:
        from rich.panel import Panel
        from rich.table import Table
        from rich.prompt import Prompt, Confirm

        console.print(
            Panel(
                "[bold cyan]Service Manager[/bold cyan]\n\n"
                "View and manage Windows services.\n"
                "Options:\n"
                "  1. List All Services\n"
                "  2. List Running Services\n"
                "  3. List Stopped Services\n"
                "  4. Start a Service\n"
                "  5. Stop a Service",
                title="[bold]Service Manager[/bold]",
                border_style="cyan",
                padding=(1, 2),
            )
        )

        choice = Prompt.ask(
            "\n[yellow]>> Select an option (1-5):[/yellow]", default="1"
        )

        console.print()

        if choice == "1":
            success, output = list_services("all")
        elif choice == "2":
            success, output = list_services("running")
        elif choice == "3":
            success, output = list_services("stopped")
        elif choice == "4":
            service_name = Prompt.ask("\n[yellow]Enter service name to start:[/yellow]")
            success, message = start_service(service_name)
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
        elif choice == "5":
            service_name = Prompt.ask("\n[yellow]Enter service name to stop:[/yellow]")
            success, message = stop_service(service_name)
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
            success, output = list_services("all")

        if success:
            console.print(
                Panel(
                    f"[dim]{output[:5000]}[/dim]",
                    title="[bold]Services[/bold]",
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
        print("  SERVICE MANAGER")
        print("=" * 60)
        print()
        print("  1. List All Services")
        print("  2. List Running Services")
        print("  3. List Stopped Services")
        print("  4. Start a Service")
        print("  5. Stop a Service")
        print()

        choice = input(">> Select option (1-5) [default=1]: ").strip() or "1"

        print()

        if choice == "1":
            success, output = list_services("all")
        elif choice == "2":
            success, output = list_services("running")
        elif choice == "3":
            success, output = list_services("stopped")
        elif choice == "4":
            service_name = input("Enter service name to start: ").strip()
            success, message = start_service(service_name)
            print(f"  {'✓' if success else '✗'} {message}")
            return
        elif choice == "5":
            service_name = input("Enter service name to stop: ").strip()
            success, message = stop_service(service_name)
            print(f"  {'✓' if success else '✗'} {message}")
            return
        else:
            success, output = list_services("all")

        print(output[:4000] if success else f"Error: {output}")


def handle_service_manager(console=None) -> None:
    """Main handler for service manager"""
    display_service_manager(console)
