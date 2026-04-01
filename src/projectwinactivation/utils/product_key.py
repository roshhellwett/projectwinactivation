"""
Product Key Finder Module
Retrieve Windows product key from registry
"""

import logging
import re
from typing import Tuple, Optional

logger = logging.getLogger(__name__)


def decode_product_key(key_bytes: bytes) -> str:
    """
    Decode Windows product key from registry bytes

    Args:
        key_bytes: Raw key bytes from registry

    Returns:
        Decoded product key string
    """
    try:
        offset = 52
        chars = "BCDFGHJKMPQRTVWXY2346789"

        key = list(key_bytes)

        for i in range(24, -1, -1):
            cursor = 0
            for j in range(14, -1, -1):
                cursor = cursor * 256 ^ key[j + offset]
                key[j + offset] = cursor // 24
                cursor = cursor % 24

            chars_list = list(chars)
            key[24 + i] = ord(chars_list[cursor])

        result = "".join(chr(c) for c in key[24:])

        formatted_key = "-".join([result[i : i + 5] for i in range(0, 25, 5)])

        return formatted_key.upper()
    except Exception as e:
        logger.error(f"Failed to decode product key: {e}")
        return "Could not decode product key"


def get_product_key() -> Tuple[bool, str]:
    """
    Get Windows product key from registry

    Returns:
        Tuple of (success, product_key_or_error_message)
    """
    try:
        import subprocess

        result = subprocess.run(
            'reg query "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion" /v DigitalProductId',
            shell=True,
            capture_output=True,
            text=True,
            timeout=10,
            encoding="utf-8",
            errors="replace",
        )

        if result.returncode != 0:
            result = subprocess.run(
                'reg query "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion" /v DigitalProductId',
                shell=True,
                capture_output=True,
                text=True,
                timeout=10,
                encoding="utf-8",
                errors="replace",
            )

        if result.returncode == 0:
            match = re.search(
                r"DigitalProductId\s+REG_SZ\s+([A-F0-9]+)", result.stdout, re.IGNORECASE
            )

            if match:
                hex_string = match.group(1)
                key_bytes = bytes.fromhex(hex_string)
                product_key = decode_product_key(key_bytes)
                return True, product_key
            else:
                match = re.search(
                    r"DigitalProductId\s+REG_BINARY\s+([A-F0-9\s]+)",
                    result.stdout,
                    re.IGNORECASE,
                )

                if match:
                    hex_string = match.group(1).replace(" ", "")
                    key_bytes = bytes.fromhex(hex_string)
                    product_key = decode_product_key(key_bytes)
                    return True, product_key
                else:
                    return False, "Could not find DigitalProductId in registry output"
        else:
            return False, "Could not access registry for product key"
    except Exception as e:
        logger.error(f"Failed to get product key: {e}")
        return False, str(e)


def get_os_edition() -> Tuple[bool, str]:
    """
    Get Windows edition name

    Returns:
        Tuple of (success, edition_name)
    """
    try:
        import subprocess

        result = subprocess.run(
            'reg query "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion" /v ProductName',
            shell=True,
            capture_output=True,
            text=True,
            timeout=10,
            encoding="utf-8",
            errors="replace",
        )

        if result.returncode == 0:
            match = re.search(r"ProductName\s+REG_SZ\s+(.+)", result.stdout)
            if match:
                return True, match.group(1).strip()

        result = subprocess.run(
            'powershell.exe -Command "(Get-WmiObject -Class Win32_OperatingSystem).Caption"',
            shell=True,
            capture_output=True,
            text=True,
            timeout=10,
            encoding="utf-8",
            errors="replace",
        )

        if result.returncode == 0:
            return True, result.stdout.strip()

        return False, "Could not determine OS edition"
    except Exception as e:
        logger.error(f"Failed to get OS edition: {e}")
        return False, str(e)


def get_license_status() -> Tuple[bool, str]:
    """
    Get Windows license status

    Returns:
        Tuple of (success, status_message)
    """
    try:
        import subprocess

        result = subprocess.run(
            "powershell.exe -Command \"(Get-CimInstance SoftwareLicensingProduct -Filter 'ApplicationID=\\'55c92734-d682-4d71-983e-d6ec3f16059f\\' AND PartialProductKey IS NOT NULL' | Select-Object -First 1).LicenseStatus\"",
            shell=True,
            capture_output=True,
            text=True,
            timeout=15,
            encoding="utf-8",
            errors="replace",
        )

        if result.returncode == 0:
            status_map = {
                "0": "Unlicensed",
                "1": "Licensed",
                "2": "OOBGrace",
                "3": "OOTGrace",
                "4": "NonGenuineGrace",
                "5": "Notification",
                "6": "ExtendedGrace",
            }

            status = result.stdout.strip()
            return True, status_map.get(status, f"Unknown ({status})")

        return False, "Could not determine license status"
    except Exception as e:
        logger.error(f"Failed to get license status: {e}")
        return False, str(e)


def display_product_key_finder(console=None) -> None:
    """Display product key finder interface"""
    if console:
        from rich.panel import Panel
        from rich.table import Table
        from rich.prompt import Confirm

        console.print(
            Panel(
                "[bold cyan]Product Key Finder[/bold cyan]\n\n"
                "Retrieve your Windows product key and license information.\n"
                "This tool extracts the product key stored in your system registry.",
                title="[bold]Product Key Finder[/bold]",
                border_style="cyan",
                padding=(1, 2),
            )
        )

        console.print()

        key_success, product_key = get_product_key()
        edition_success, edition = get_os_edition()
        license_success, license_status = get_license_status()

        table = Table(
            title="[bold]Windows License Information[/bold]",
            show_header=False,
            box=None,
        )
        table.add_column("Property", style="yellow", width=20)
        table.add_column("Value", style="white")

        if edition_success:
            table.add_row("Edition", edition)

        if license_success:
            status_color = "green" if "Licensed" in license_status else "red"
            table.add_row(
                "License Status", f"[{status_color}]{license_status}[/{status_color}]"
            )

        if key_success:
            table.add_row("Product Key", f"[bold cyan]{product_key}[/bold cyan]")
        else:
            table.add_row("Product Key", f"[red]{product_key}[/red]")

        console.print(table)

        console.print()
        console.print("[dim]Note: This key can be used for reinstalling Windows.[/dim]")
        console.print("[dim]Store it securely and never share it with others.[/dim]")

        Confirm.ask("\n[dim]Press Enter to continue...[/dim]", default=True)

    else:
        print("\n" + "=" * 60)
        print("  PRODUCT KEY FINDER")
        print("=" * 60)
        print()

        key_success, product_key = get_product_key()
        edition_success, edition = get_os_edition()
        license_success, license_status = get_license_status()

        if edition_success:
            print(f"  Edition: {edition}")

        if license_success:
            print(f"  License Status: {license_status}")

        if key_success:
            print(f"\n  Product Key: {product_key}")
        else:
            print(f"\n  Product Key: {product_key}")

        print()


def handle_product_key_finder(console=None) -> None:
    """Main handler for product key finder"""
    display_product_key_finder(console)
