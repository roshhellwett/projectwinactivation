"""
ASCII Art Banners for projectwinactivation
Premium stylized banners for premium user experience
"""

MAIN_BANNER = """
+----------------------------------------------------------------------+
|                                                                      |
|   ##   ##   ##  ######   ######  ##   ##   ##  ######   ######       |
|   ##   ##  ####  ##  ##  ##  ##  ###  ##  ####  ##  ##  ##          |
|   ## # ## ## ##  ######  ######  ## # ## ## ##  ######  ##          |
|   ####### ######  ##  ##  ##  ##  ##  #### ######  ##  ##           |
|   ## # ##   ####  ######  ######  ##   ##   ####  ######            |
|                                                                      |
|              #######   ######   #######   ######   #######            |
|              ##   ##  ##       ##       ##   ##  ##   ##            |
|              #######  ######  ######   ##   ##  #######             |
|              ##  ##   ##       ##       ##   ##  ##  ##              |
|              ##   ##   ######   ######   #####   ##   ##            |
|                                                                      |
+----------------------------------------------------------------------+
"""

EXIT_BANNER = """
+----------------------------------------------------------------------+
|                                                                      |
|   ##   ##   #######   #######  ##   ##   #######                    |
|   ##   ##  ##     ##  ##       ### ###  ##     ##                   |
|   ##   ##  ##     ##  ##       ## # ##  ##     ##                    |
|   ########  ##     ##  ######  ##   ##  ##     ##                    |
|   ##   ##   ##     ##       ##  ##   ##  ##     ##                   |
|   ##   ##    #######   ######  ##   ##   #######                     |
|                                                                      |
+----------------------------------------------------------------------+
"""

SUCCESS_BANNER = """
+----------------------------------------------------------------------+
|                     [ SUCCESS ]                                       |
+----------------------------------------------------------------------+
"""

WARNING_BANNER = """
+----------------------------------------------------------------------+
|                     [ WARNING ]                                       |
+----------------------------------------------------------------------+
"""

ERROR_BANNER = """
+----------------------------------------------------------------------+
|                     [ ERROR ]                                         |
+----------------------------------------------------------------------+
"""

MENU_ITEMS = [
    ("Windows Activation", "Activate Windows OS"),
    ("System Info", "View system information"),
    ("Driver Manager", "Manage device drivers"),
    ("Service Manager", "Windows services control"),
    ("Startup Manager", "Startup programs management"),
    ("Disk Cleanup", "Disk space management"),
    ("Network Diagnostics", "Network testing tools"),
    ("Windows Update", "Update status & history"),
    ("Product Key Finder", "Retrieve Windows key"),
    ("Firewall Manager", "Firewall rules control"),
    ("Process Monitor", "Running processes view"),
    ("Update", "Check for updates"),
    ("Help", "Show help & commands"),
    ("Exit", "Exit application"),
]


def get_banner_lines() -> list:
    """Get main banner as list of lines for animated display"""
    return MAIN_BANNER.strip().split("\n")


def get_exit_lines() -> list:
    """Get exit banner as list of lines"""
    return EXIT_BANNER.strip().split("\n")
