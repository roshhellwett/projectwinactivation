"""
Disk Cleanup Module
Manage disk space, cleanup temp files, analyze storage
"""

import os
import logging
from typing import Tuple, List, Dict
from pathlib import Path
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


def get_disk_space() -> Tuple[bool, str]:
    """
    Get disk space information

    Returns:
        Tuple of (success, output)
    """
    try:
        import subprocess

        result = subprocess.run(
            "wmic logicaldisk get Caption,Size,FreeSpace,DriveType",
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
            return False, result.stderr or "Failed to get disk space"
    except Exception as e:
        logger.error(f"Failed to get disk space: {e}")
        return False, str(e)


def get_temp_folder_size() -> int:
    """
    Get the size of temporary folders

    Returns:
        Total size in bytes
    """
    temp_paths = [
        os.environ.get("TEMP", ""),
        os.environ.get("TMP", ""),
        "C:\\Windows\\Temp",
    ]

    total_size = 0

    for temp_path in temp_paths:
        if not temp_path or not os.path.exists(temp_path):
            continue

        try:
            for root, dirs, files in os.walk(temp_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        total_size += os.path.getsize(file_path)
                    except (OSError, PermissionError):
                        continue
        except (OSError, PermissionError):
            continue

    return total_size


def cleanup_temp_files(dry_run: bool = False) -> Tuple[int, int, int]:
    """
    Clean up temporary files

    Args:
        dry_run: If True, only count files without deleting

    Returns:
        Tuple of (files_found, files_deleted, bytes_freed)
    """
    temp_paths = [
        os.environ.get("TEMP", ""),
        os.environ.get("TMP", ""),
        "C:\\Windows\\Temp",
    ]

    files_found = 0
    files_deleted = 0
    bytes_freed = 0

    for temp_path in temp_paths:
        if not temp_path or not os.path.exists(temp_path):
            continue

        try:
            for root, dirs, files in os.walk(temp_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    files_found += 1

                    try:
                        file_size = os.path.getsize(file_path)

                        if not dry_run:
                            os.remove(file_path)
                            files_deleted += 1
                            bytes_freed += file_size
                        else:
                            bytes_freed += file_size

                    except (OSError, PermissionError):
                        continue
        except (OSError, PermissionError):
            continue

    return files_found, files_deleted, bytes_freed


def get_drive_info() -> List[Dict[str, str]]:
    """
    Get detailed drive information

    Returns:
        List of drive information dictionaries
    """
    drives = []

    try:
        import subprocess

        result = subprocess.run(
            "wmic logicaldisk get Caption,Size,FreeSpace,DriveType /format:csv",
            shell=True,
            capture_output=True,
            text=True,
            timeout=15,
            encoding="utf-8",
            errors="replace",
        )

        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            for line in lines[1:]:
                parts = line.split(",")
                if len(parts) >= 4:
                    try:
                        drive = parts[1].strip(":")
                        drive_type = int(parts[3]) if parts[3].strip().isdigit() else 0

                        if drive_type == 3:
                            total = int(parts[2]) if parts[2].strip().isdigit() else 0
                            free = int(parts[3]) if parts[3].strip().isdigit() else 0
                            used = total - free
                            pct = (used / total * 100) if total else 0

                            drives.append(
                                {
                                    "drive": f"{drive}:",
                                    "total": format_bytes(total),
                                    "free": format_bytes(free),
                                    "used": format_bytes(used),
                                    "percent": f"{pct:.1f}%",
                                    "total_bytes": total,
                                    "free_bytes": free,
                                }
                            )
                    except (ValueError, IndexError):
                        continue
    except Exception as e:
        logger.error(f"Failed to get drive info: {e}")

    return drives


def display_disk_cleanup(console=None) -> None:
    """Display disk cleanup interface"""
    if console:
        from rich.panel import Panel
        from rich.table import Table
        from rich.prompt import Prompt, Confirm

        console.print(
            Panel(
                "[bold cyan]Disk Cleanup[/bold cyan]\n\n"
                "Manage disk space and clean up temporary files.\n"
                "Options:\n"
                "  1. Disk Space Analysis\n"
                "  2. Temp Files Cleanup\n"
                "  3. Drive Information",
                title="[bold]Disk Cleanup[/bold]",
                border_style="cyan",
                padding=(1, 2),
            )
        )

        choice = Prompt.ask(
            "\n[yellow]>> Select an option (1-3):[/yellow]", default="1"
        )

        console.print()

        if choice == "1":
            success, output = get_disk_space()

            if success:
                drive_info = get_drive_info()

                table = Table(
                    title="[bold]Drive Space Analysis[/bold]",
                    show_header=True,
                    header_style="bold cyan",
                    box=None,
                )
                table.add_column("Drive", style="yellow", width=8)
                table.add_column("Total", style="white", width=12)
                table.add_column("Used", style="red", width=12)
                table.add_column("Free", style="green", width=12)
                table.add_column("Usage", style="magenta", width=8)

                for drive in drive_info:
                    table.add_row(
                        drive["drive"],
                        drive["total"],
                        drive["used"],
                        drive["free"],
                        drive["percent"],
                    )

                console.print(table)

                temp_size = get_temp_folder_size()
                console.print(
                    f"\n  [yellow]Temp folder size:[/yellow] [cyan]{format_bytes(temp_size)}[/cyan]"
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
            console.print("[yellow]Scanning temporary files...[/yellow]\n")

            files_found, _, bytes_found = cleanup_temp_files(dry_run=True)

            console.print(
                f"  Found: [cyan]{files_found}[/cyan] files ([yellow]{format_bytes(bytes_found)}[/yellow])\n"
            )

            confirm = Confirm.ask(
                "[red]⚠️  Are you sure you want to delete these files?[/red]",
                default=False,
            )

            if confirm:
                files_found, files_deleted, bytes_freed = cleanup_temp_files(
                    dry_run=False
                )

                console.print(
                    Panel(
                        f"[green]✓ Cleanup completed![/green]\n\n"
                        f"Files found: {files_found}\n"
                        f"Files deleted: {files_deleted}\n"
                        f"Space freed: [yellow]{format_bytes(bytes_freed)}[/yellow]",
                        title="[bold green]Cleanup Complete[/bold green]",
                        border_style="green",
                    )
                )
            else:
                console.print("[dim]Cleanup cancelled.[/dim]")

        elif choice == "3":
            drive_info = get_drive_info()

            table = Table(
                title="[bold]Drive Information[/bold]",
                show_header=True,
                header_style="bold cyan",
                box=None,
            )
            table.add_column("Drive", style="yellow", width=8)
            table.add_column("Total", style="white", width=12)
            table.add_column("Free", style="green", width=12)
            table.add_column("Usage", style="magenta", width=8)

            for drive in drive_info:
                table.add_row(
                    drive["drive"], drive["total"], drive["free"], drive["percent"]
                )

            console.print(table)

        else:
            success, output = get_disk_space()
            console.print(f"[dim]{output[:2000]}[/dim]")

        Confirm.ask("\n[dim]Press Enter to continue...[/dim]", default=True)

    else:
        print("\n" + "=" * 60)
        print("  DISK CLEANUP")
        print("=" * 60)
        print()
        print("  1. Disk Space Analysis")
        print("  2. Temp Files Cleanup")
        print("  3. Drive Information")
        print()

        choice = input(">> Select option (1-3) [default=1]: ").strip() or "1"

        print()

        if choice == "1":
            success, output = get_disk_space()
            print(output if success else f"Error: {output}")

            temp_size = get_temp_folder_size()
            print(f"\nTemp folder size: {format_bytes(temp_size)}")
        elif choice == "3":
            drive_info = get_drive_info()
            for drive in drive_info:
                print(
                    f"  {drive['drive']} Total: {drive['total']} | Free: {drive['free']} | Usage: {drive['percent']}"
                )


def handle_disk_cleanup(console=None) -> None:
    """Main handler for disk cleanup"""
    display_disk_cleanup(console)
