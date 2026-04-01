"""
Windows Activation Module
Handles Windows activation with proper disclaimer and consent
"""

import sys
import ctypes
import logging
from typing import Tuple

logger = logging.getLogger(__name__)

ACTIVATION_URL = (
    "aHR0cHM6Ly9nZXQuYWN0aXZhdGVkLndpbg=="  # Base64 encoded: https://get.activated.wing
)


def decode_string(encoded: str) -> str:
    """Decode base64 encoded string"""
    import base64

    return base64.b64decode(encoded).decode("utf-8")


def is_admin() -> bool:
    """Check if running with administrator privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def request_admin() -> bool:
    """Request administrator privileges and re-run the script"""
    try:
        executable = sys.executable
        params = " ".join(sys.argv[1:])
        result = ctypes.windll.shell32.ShellExecuteW(
            None, "runas", executable, params, None, 1
        )
        return result > 32
    except Exception as e:
        logger.error(f"Failed to request admin: {e}")
        return False


def get_activation_command() -> str:
    """Get the PowerShell activation command"""
    url = decode_string(ACTIVATION_URL)
    return f'-ExecutionPolicy Bypass -Command "irm {url} | iex"'


def launch_activation() -> Tuple[bool, str]:
    """
    Launch Windows activation process

    Returns:
        Tuple of (success, message)
    """
    if not is_admin():
        return False, "Administrator privileges required for Windows activation"

    try:
        ps_command = get_activation_command()
        result = ctypes.windll.shell32.ShellExecuteW(
            None, "runas", "powershell.exe", ps_command, None, 1
        )

        if result <= 32:
            return False, f"Failed to launch PowerShell. Error code: {result}"

        return True, "PowerShell launched successfully with administrator privileges"

    except Exception as e:
        logger.error(f"Activation launch failed: {e}")
        return False, f"Error: {str(e)}"


def check_activation_status() -> Tuple[bool, str]:
    """
    Check current Windows activation status

    Returns:
        Tuple of (is_activated, status_message)
    """
    try:
        import subprocess

        result = subprocess.run(
            [
                "powershell.exe",
                "-Command",
                "(Get-CimInstance SoftwareLicensingProduct -Filter \"ApplicationID='55c92734-d682-4d71-983e-d6ec3f16059f' AND PartialProductKey IS NOT NULL\" | Where-Object {$_.LicenseStatus -ne 0} | Measure-Object).Count",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )

        count = int(result.stdout.strip()) if result.stdout.strip().isdigit() else 0

        if count > 0:
            return True, "Windows appears to be activated"
        else:
            return False, "Windows does not appear to be activated"

    except Exception as e:
        logger.warning(f"Could not check activation status: {e}")
        return False, "Could not determine activation status"


def show_disclaimer() -> str:
    """
    Return the disclaimer text

    Returns:
        Disclaimer text as string
    """
    return """
=================================================================

*** IMPORTANT DISCLAIMER & WARNING ***

=================================================================

This Windows activation tool is provided for EDUCATIONAL and PERSONAL USE ONLY.

By using this tool, you acknowledge and agree to the following:

  * Only use on systems you own or have a valid license for
  * This tool bypasses standard activation for testing/evaluation purposes
  * Microsoft Windows requires a valid license for legal use
  * The developers are not responsible for misuse of this tool
  * Use at your OWN RISK and at your OWN DISCRETION

=================================================================

LEGAL NOTICE:
This tool is for educational purposes only. For genuine Windows installations,
please obtain a valid license from Microsoft at: https://www.microsoft.com

=================================================================
"""


def get_consent_prompt() -> str:
    """
    Return the consent prompt text

    Returns:
        Consent prompt as string
    """
    return """
Do you understand and agree to the above disclaimer?

  [Y] Yes, I understand and wish to proceed
  [N] No, take me back to the menu
  
>> Enter your choice (Y/N): """


def handle_activation(console=None) -> Tuple[bool, str]:
    """
    Main handler for Windows activation

    This function:
    1. Checks for admin privileges
    2. Shows disclaimer
    3. Gets user consent
    4. Launches activation

    Args:
        console: Rich console instance (optional)

    Returns:
        Tuple of (success, message)
    """
    if console:
        from rich.panel import Panel
        from rich.prompt import Confirm

        console.print(
            Panel(
                "[yellow]============================================================[/yellow]\n\n"
                "[bold red]*** IMPORTANT DISCLAIMER & WARNING ***[/bold red]\n\n"
                "[yellow]============================================================[/yellow]\n\n"
                "[cyan]This Windows activation tool is provided for [bold]EDUCATIONAL[/bold] and "
                "[bold]PERSONAL USE ONLY[/bold].\n\n[/cyan]"
                "By using this tool, you acknowledge and agree to the following:\n\n"
                "  * [red]Only use[/red] on systems you own or have a valid license for\n"
                "  * [red]This tool[/red] bypasses standard activation for testing/evaluation\n"
                "  * [red]Microsoft Windows[/red] requires a valid license for legal use\n"
                "  * [red]The developers[/red] are not responsible for misuse\n"
                "  * [red]Use[/red] at your OWN RISK and at your OWN DISCRETION\n\n"
                "[yellow]============================================================[/yellow]\n\n"
                "[italic]For genuine Windows installations, please obtain a valid license from Microsoft.[/italic]\n\n"
                "[yellow]============================================================[/yellow]",
                title="[bold red]DISCLAIMER[/bold red]",
                border_style="red",
                padding=(1, 2),
            )
        )

        consent = Confirm.ask(
            "\n[bold yellow]>> Do you understand and agree to the above disclaimer?[/bold yellow]\n    Type [bold green]Y[/bold green] to proceed or [bold red]N[/bold red] to cancel: ",
            default=False,
        )

        if not consent:
            return False, "Activation cancelled by user. Returning to menu..."

        if not is_admin():
            console.print(
                "\n[yellow]WARNING: Administrator privileges required.[/yellow]"
            )
            console.print("[dim]Attempting to elevate...[/dim]")

            if request_admin():
                return True, "Elevated privileges granted. Running activation..."
            else:
                return (
                    False,
                    "Failed to obtain administrator privileges. Please run as Administrator.",
                )

        console.print("\n[cyan]Launching Windows activation...[/cyan]")
        console.print(
            "[dim]This will open PowerShell with administrator privileges.[/dim]\n"
        )

        success, message = launch_activation()

        if success:
            console.print(
                Panel(
                    "[green][OK] PowerShell launched successfully![/green]\n\n"
                    "The activation script is now running in a new PowerShell window.\n"
                    "Follow the instructions in that window to complete activation.\n\n"
                    "[yellow]Note:[/yellow] If activation fails, try running this tool again as Administrator.",
                    title="[bold green]ACTIVATION INITIATED[/bold green]",
                    border_style="green",
                    padding=(1, 2),
                )
            )
        else:
            console.print(
                Panel(
                    f"[red][ERROR] Activation failed![/red]\n\n"
                    f"Error: {message}\n\n"
                    "Please try running as Administrator or check your system configuration.",
                    title="[bold red]ACTIVATION ERROR[/bold red]",
                    border_style="red",
                    padding=(1, 2),
                )
            )

        return success, message

    else:
        print(show_disclaimer())
        print(get_consent_prompt())

        try:
            consent = input().strip().lower()
        except (EOFError, KeyboardInterrupt):
            return False, "Cancelled by user"

        if consent != "y":
            return False, "Activation cancelled by user"

        if not is_admin():
            print("\nAdministrator privileges required.")
            print("Attempting to elevate...")

            if request_admin():
                return True, "Elevated privileges granted"
            else:
                return False, "Failed to obtain administrator privileges"

        return launch_activation()
