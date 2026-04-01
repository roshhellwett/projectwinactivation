"""
Network Diagnostics Module
Network testing and diagnostic tools
"""

import socket
import logging
from typing import Tuple, Optional

logger = logging.getLogger(__name__)


def get_ip_config() -> Tuple[bool, str]:
    """
    Get IP configuration

    Returns:
        Tuple of (success, output)
    """
    try:
        import subprocess

        result = subprocess.run(
            "ipconfig /all",
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
            return False, result.stderr or "Failed to get IP config"
    except Exception as e:
        logger.error(f"Failed to get IP config: {e}")
        return False, str(e)


def get_network_adapters() -> Tuple[bool, str]:
    """
    Get network adapters information

    Returns:
        Tuple of (success, output)
    """
    try:
        import subprocess

        result = subprocess.run(
            "netsh interface show interface",
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
            return False, result.stderr or "Failed to get network adapters"
    except Exception as e:
        logger.error(f"Failed to get network adapters: {e}")
        return False, str(e)


def get_connection_status() -> Tuple[bool, str]:
    """
    Get WiFi connection status

    Returns:
        Tuple of (success, output)
    """
    try:
        import subprocess

        result = subprocess.run(
            "netsh wlan show interfaces",
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
            return False, result.stderr or "Failed to get connection status"
    except Exception as e:
        logger.error(f"Failed to get connection status: {e}")
        return False, str(e)


def ping_host(host: str, count: int = 4) -> Tuple[bool, str]:
    """
    Ping a host

    Args:
        host: Hostname or IP address
        count: Number of ping requests

    Returns:
        Tuple of (success, output)
    """
    try:
        import subprocess

        result = subprocess.run(
            f"ping -n {count} {host}",
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
            return False, result.stdout or "Host unreachable"
    except Exception as e:
        logger.error(f"Ping failed: {e}")
        return False, str(e)


def dns_lookup(hostname: str) -> Tuple[bool, str]:
    """
    Perform DNS lookup

    Args:
        hostname: Hostname to lookup

    Returns:
        Tuple of (success, result)
    """
    try:
        ip = socket.gethostbyname(hostname)
        return True, f"{hostname} -> {ip}"
    except socket.gaierror as e:
        return False, f"DNS lookup failed: {e}"
    except Exception as e:
        logger.error(f"DNS lookup failed: {e}")
        return False, str(e)


def flush_dns() -> Tuple[bool, str]:
    """
    Flush DNS resolver cache

    Returns:
        Tuple of (success, message)
    """
    try:
        import subprocess

        result = subprocess.run(
            "ipconfig /flushdns",
            shell=True,
            capture_output=True,
            text=True,
            timeout=10,
            encoding="utf-8",
            errors="replace",
        )

        if result.returncode == 0:
            return True, "DNS cache flushed successfully"
        else:
            return False, result.stderr or "Failed to flush DNS cache"
    except Exception as e:
        logger.error(f"Failed to flush DNS: {e}")
        return False, str(e)


def display_network_diag(console=None) -> None:
    """Display network diagnostics interface"""
    if console:
        from rich.panel import Panel
        from rich.prompt import Prompt, Confirm

        console.print(
            Panel(
                "[bold cyan]Network Diagnostics[/bold cyan]\n\n"
                "Test and diagnose network connectivity.\n"
                "Options:\n"
                "  1. IP Configuration\n"
                "  2. Network Adapters\n"
                "  3. Connection Status\n"
                "  4. Ping Test\n"
                "  5. DNS Lookup\n"
                "  6. Flush DNS Cache",
                title="[bold]Network Diagnostics[/bold]",
                border_style="cyan",
                padding=(1, 2),
            )
        )

        choice = Prompt.ask(
            "\n[yellow]>> Select an option (1-6):[/yellow]", default="1"
        )

        console.print()

        if choice == "1":
            success, output = get_ip_config()
        elif choice == "2":
            success, output = get_network_adapters()
        elif choice == "3":
            success, output = get_connection_status()
        elif choice == "4":
            target = Prompt.ask(
                "\n[yellow]Enter hostname or IP address:[/yellow]", default="8.8.8.8"
            )
            success, output = ping_host(target)
        elif choice == "5":
            host = Prompt.ask(
                "\n[yellow]Enter hostname:[/yellow]", default="google.com"
            )
            success, output = dns_lookup(host)
        elif choice == "6":
            success, output = flush_dns()
        else:
            success, output = get_ip_config()

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
        print("  NETWORK DIAGNOSTICS")
        print("=" * 60)
        print()
        print("  1. IP Configuration")
        print("  2. Network Adapters")
        print("  3. Connection Status")
        print("  4. Ping Test")
        print("  5. DNS Lookup")
        print("  6. Flush DNS Cache")
        print()

        choice = input(">> Select option (1-6) [default=1]: ").strip() or "1"

        print()

        if choice == "1":
            success, output = get_ip_config()
        elif choice == "2":
            success, output = get_network_adapters()
        elif choice == "3":
            success, output = get_connection_status()
        elif choice == "4":
            target = (
                input("Enter hostname or IP [default=8.8.8.8]: ").strip() or "8.8.8.8"
            )
            success, output = ping_host(target)
        elif choice == "5":
            host = (
                input("Enter hostname [default=google.com]: ").strip() or "google.com"
            )
            success, output = dns_lookup(host)
        elif choice == "6":
            success, output = flush_dns()
        else:
            success, output = get_ip_config()

        print(output if success else f"Error: {output}")


def handle_network_diag(console=None) -> None:
    """Main handler for network diagnostics"""
    display_network_diag(console)
