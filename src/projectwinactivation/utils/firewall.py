"""
Firewall Manager Module
View and manage Windows Firewall rules
"""

import logging
from typing import Tuple, Optional, List, Dict

logger = logging.getLogger(__name__)


def get_firewall_status() -> Tuple[bool, str]:
    """
    Get Windows Firewall status for all profiles

    Returns:
        Tuple of (success, output)
    """
    try:
        import subprocess

        result = subprocess.run(
            "netsh advfirewall show allprofiles",
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
            return False, result.stderr or "Failed to get firewall status"
    except Exception as e:
        logger.error(f"Failed to get firewall status: {e}")
        return False, str(e)


def get_inbound_rules() -> Tuple[bool, str]:
    """
    Get inbound firewall rules

    Returns:
        Tuple of (success, output)
    """
    try:
        import subprocess

        result = subprocess.run(
            "netsh advfirewall firewall show rule name=all dir=in",
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
            return False, result.stderr or "Failed to get inbound rules"
    except Exception as e:
        logger.error(f"Failed to get inbound rules: {e}")
        return False, str(e)


def get_outbound_rules() -> Tuple[bool, str]:
    """
    Get outbound firewall rules

    Returns:
        Tuple of (success, output)
    """
    try:
        import subprocess

        result = subprocess.run(
            "netsh advfirewall firewall show rule name=all dir=out",
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
            return False, result.stderr or "Failed to get outbound rules"
    except Exception as e:
        logger.error(f"Failed to get outbound rules: {e}")
        return False, str(e)


def search_firewall_rules(search_term: str) -> Tuple[bool, str]:
    """
    Search firewall rules by name

    Args:
        search_term: Term to search for

    Returns:
        Tuple of (success, output)
    """
    try:
        import subprocess

        result = subprocess.run(
            f'netsh advfirewall firewall show rule name=all | findstr /i "{search_term}"',
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
            encoding="utf-8",
            errors="replace",
        )

        if result.returncode == 0:
            return (
                True,
                result.stdout if result.stdout.strip() else "No matching rules found",
            )
        else:
            return True, "No matching rules found"
    except Exception as e:
        logger.error(f"Failed to search firewall rules: {e}")
        return False, str(e)


def get_rule_summary() -> List[Dict[str, int]]:
    """
    Get summary of firewall rules

    Returns:
        List of dictionaries with rule counts by profile
    """
    try:
        import subprocess

        result = subprocess.run(
            "netsh advfirewall show allprofiles state verbose",
            shell=True,
            capture_output=True,
            text=True,
            timeout=15,
            encoding="utf-8",
            errors="replace",
        )

        summary = []

        if result.returncode == 0:
            output = result.stdout
            profiles = {"Domain": False, "Private": False, "Public": False}

            current_profile = None

            for line in output.split("\n"):
                line = line.strip()

                if "Domain Profile" in line:
                    current_profile = "Domain"
                elif "Private Profile" in line:
                    current_profile = "Private"
                elif "Public Profile" in line:
                    current_profile = "Public"
                elif "State" in line and current_profile:
                    if "ON" in line or "ONLINE" in line:
                        profiles[current_profile] = True

            for profile, enabled in profiles.items():
                summary.append(
                    {
                        "profile": profile,
                        "enabled": enabled,
                        "state": "ON" if enabled else "OFF",
                    }
                )

        return summary
    except Exception as e:
        logger.error(f"Failed to get rule summary: {e}")
        return []


def display_firewall_manager(console=None) -> None:
    """Display firewall manager interface"""
    if console:
        from rich.panel import Panel
        from rich.table import Table
        from rich.prompt import Prompt, Confirm

        console.print(
            Panel(
                "[bold cyan]Firewall Manager[/bold cyan]\n\n"
                "View Windows Firewall status and rules.\n"
                "Options:\n"
                "  1. Firewall Status\n"
                "  2. Inbound Rules\n"
                "  3. Outbound Rules\n"
                "  4. Search Rules",
                title="[bold]Firewall Manager[/bold]",
                border_style="cyan",
                padding=(1, 2),
            )
        )

        choice = Prompt.ask(
            "\n[yellow]>> Select an option (1-4):[/yellow]", default="1"
        )

        console.print()

        if choice == "1":
            success, output = get_firewall_status()

            if success:
                summary = get_rule_summary()

                if summary:
                    table = Table(
                        title="[bold]Firewall Profiles[/bold]",
                        show_header=True,
                        header_style="bold cyan",
                        box=None,
                    )
                    table.add_column("Profile", style="yellow", width=15)
                    table.add_column("Status", style="white", width=10)

                    for item in summary:
                        status_color = "green" if item["enabled"] else "red"
                        table.add_row(
                            item["profile"],
                            f"[{status_color}]{item['state']}[/{status_color}]",
                        )

                    console.print(table)
                    console.print()

                console.print(
                    Panel(
                        f"[dim]{output[:3000]}[/dim]",
                        title="[bold]Detailed Status[/bold]",
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

        elif choice == "2":
            success, output = get_inbound_rules()
        elif choice == "3":
            success, output = get_outbound_rules()
        elif choice == "4":
            search_term = Prompt.ask("\n[yellow]Enter search term:[/yellow]")
            success, output = search_firewall_rules(search_term)
        else:
            success, output = get_firewall_status()

        if choice in ("2", "3", "4"):
            if success:
                console.print(
                    Panel(
                        f"[dim]{output[:4000]}[/dim]",
                        title="[bold]Rules[/bold]",
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
        print("  FIREWALL MANAGER")
        print("=" * 60)
        print()
        print("  1. Firewall Status")
        print("  2. Inbound Rules")
        print("  3. Outbound Rules")
        print("  4. Search Rules")
        print()

        choice = input(">> Select option (1-4) [default=1]: ").strip() or "1"

        print()

        if choice == "1":
            success, output = get_firewall_status()
        elif choice == "2":
            success, output = get_inbound_rules()
        elif choice == "3":
            success, output = get_outbound_rules()
        elif choice == "4":
            search_term = input("Enter search term: ").strip()
            success, output = search_firewall_rules(search_term)
        else:
            success, output = get_firewall_status()

        print(output[:3000] if success else f"Error: {output}")


def handle_firewall_manager(console=None) -> None:
    """Main handler for firewall manager"""
    display_firewall_manager(console)
