"""
Main entry point for projectwinactivation

Allows running the package as a module:
    python -m projectwinactivation start
"""

import sys

if __name__ == "__main__":
    from projectwinactivation import __version__
    from projectwinactivation.cli import app

    if "--version" in sys.argv or "-V" in sys.argv:
        print(f"projectwinactivation version {__version__}")
        sys.exit(0)

    app()
