"""
Base utilities for projectwinactivation
Shared functions and constants used across modules
"""

import sys
import os
import logging
from typing import Tuple, Optional, Callable, Any
from pathlib import Path

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def is_windows() -> bool:
    """Check if running on Windows"""
    return sys.platform.startswith("win") or os.name == "nt"


def is_admin() -> bool:
    """Check if running with administrator privileges"""
    if not is_windows():
        return False
    try:
        import ctypes

        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def require_admin(func: Callable) -> Callable:
    """Decorator to require admin privileges for a function"""

    def wrapper(*args, **kwargs):
        if not is_admin():
            raise PermissionError("This operation requires administrator privileges")
        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper


def run_command(cmd: str, timeout: int = 30, capture: bool = True) -> Tuple[bool, str]:
    """
    Execute a system command safely

    Args:
        cmd: Command to execute
        timeout: Timeout in seconds
        capture: Whether to capture output

    Returns:
        Tuple of (success, output)
    """
    import subprocess

    try:
        if capture:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                encoding="utf-8",
                errors="replace",
            )
            return result.returncode == 0, result.stdout
        else:
            result = subprocess.run(cmd, shell=True, timeout=timeout)
            return result.returncode == 0, ""
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except Exception as e:
        logger.error(f"Command execution failed: {e}")
        return False, str(e)


def format_bytes(size: float) -> str:
    """Format bytes to human readable format"""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"


def safe_input(prompt: str = "", default: str = "", allow_empty: bool = True) -> str:
    """Safe input handling for non-interactive mode"""
    if not sys.stdin.isatty():
        return default
    try:
        result = input(prompt).strip()
        if not result and not allow_empty:
            return default
        return result
    except (EOFError, KeyboardInterrupt):
        return default


def get_temp_dir() -> Path:
    """Get temporary directory for the package"""
    import tempfile

    temp = Path(tempfile.gettempdir()) / "projectwinactivation"
    temp.mkdir(parents=True, exist_ok=True)
    return temp


def clear_screen():
    """Clear the terminal screen"""
    os.system("cls" if is_windows() else "clear")


class WindowsOnlyError(Exception):
    """Raised when operation is attempted on non-Windows platform"""

    pass


class AdminRequiredError(Exception):
    """Raised when operation requires admin privileges"""

    pass
