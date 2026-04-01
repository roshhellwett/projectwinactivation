"""
Test suite for projectwinactivation
Tests each utility module
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from projectwinactivation.utils import (
    is_windows,
    is_admin,
    run_command,
    format_bytes,
    safe_input,
    get_temp_dir,
)


class TestBaseUtils:
    """Test base utilities"""

    def test_is_windows(self):
        """Test Windows detection"""
        result = is_windows()
        assert isinstance(result, bool)

    def test_is_admin(self):
        """Test admin privileges check"""
        result = is_admin()
        assert isinstance(result, bool)

    def test_run_command_success(self):
        """Test successful command execution"""
        success, output = run_command("echo test", timeout=5)
        assert isinstance(success, bool)
        assert isinstance(output, str)

    def test_run_command_failure(self):
        """Test failed command execution"""
        success, output = run_command("invalid_command_xyz_123", timeout=5)
        assert isinstance(success, bool)

    def test_format_bytes(self):
        """Test byte formatting"""
        assert "B" in format_bytes(0)
        assert "B" in format_bytes(100)
        assert "KB" in format_bytes(2048)
        assert "MB" in format_bytes(2 * 1024 * 1024)
        assert "GB" in format_bytes(2 * 1024 * 1024 * 1024)

    def test_get_temp_dir(self):
        """Test temp directory creation"""
        temp_dir = get_temp_dir()
        assert temp_dir.exists()
        assert "projectwinactivation" in str(temp_dir)


class TestActivation:
    """Test activation module"""

    def test_activation_import(self):
        """Test activation module imports"""
        from projectwinactivation.utils.activation import (
            decode_string,
            is_admin,
            get_activation_command,
            show_disclaimer,
        )

        assert callable(decode_string)
        assert callable(is_admin)
        assert callable(get_activation_command)
        assert callable(show_disclaimer)

    def test_decode_string(self):
        """Test base64 decoding"""
        from projectwinactivation.utils.activation import decode_string

        result = decode_string("aHR0cHM6Ly9nZXQuYWN0aXZhdGVkLndpbg==")
        assert "get.activated" in result
        assert "https" in result

    def test_get_activation_command(self):
        """Test activation command generation"""
        from projectwinactivation.utils.activation import get_activation_command

        cmd = get_activation_command()
        assert "get.activated" in cmd
        assert "irm" in cmd
        assert "iex" in cmd


class TestSystemInfo:
    """Test system info module"""

    def test_system_info_import(self):
        """Test system info imports"""
        from projectwinactivation.utils.system_info import (
            get_computer_name,
            get_username,
            get_os_info,
            get_total_ram,
            format_bytes,
        )

        assert callable(get_computer_name)
        assert callable(get_username)
        assert callable(get_os_info)
        assert callable(get_total_ram)

    def test_get_computer_name(self):
        """Test computer name retrieval"""
        from projectwinactivation.utils.system_info import get_computer_name

        name = get_computer_name()
        assert isinstance(name, str)
        assert len(name) > 0

    def test_get_os_info(self):
        """Test OS info retrieval"""
        from projectwinactivation.utils.system_info import get_os_info

        info = get_os_info()
        assert isinstance(info, dict)
        assert "system" in info
        assert "release" in info


class TestDrivers:
    """Test drivers module"""

    def test_drivers_import(self):
        """Test drivers module imports"""
        from projectwinactivation.utils.drivers import (
            list_drivers,
            get_driver_count,
            export_driver_list,
        )

        assert callable(list_drivers)
        assert callable(get_driver_count)
        assert callable(export_driver_list)

    def test_list_drivers(self):
        """Test driver listing"""
        from projectwinactivation.utils.drivers import list_drivers

        success, output = list_drivers()
        assert isinstance(success, bool)
        assert isinstance(output, str)


class TestServices:
    """Test services module"""

    def test_services_import(self):
        """Test services module imports"""
        from projectwinactivation.utils.services import (
            list_services,
            get_service_details,
            start_service,
            stop_service,
        )

        assert callable(list_services)
        assert callable(get_service_details)
        assert callable(start_service)
        assert callable(stop_service)

    def test_list_services(self):
        """Test service listing"""
        from projectwinactivation.utils.services import list_services

        success, output = list_services()
        assert isinstance(success, bool)
        assert isinstance(output, str)


class TestNetwork:
    """Test network module"""

    def test_network_import(self):
        """Test network module imports"""
        from projectwinactivation.utils.network import (
            get_ip_config,
            ping_host,
            dns_lookup,
            flush_dns,
        )

        assert callable(get_ip_config)
        assert callable(ping_host)
        assert callable(dns_lookup)
        assert callable(flush_dns)

    def test_dns_lookup(self):
        """Test DNS lookup"""
        from projectwinactivation.utils.network import dns_lookup

        success, result = dns_lookup("google.com")
        assert isinstance(success, bool)
        assert isinstance(result, str)
        if success:
            assert "google.com" in result


class TestProcesses:
    """Test processes module"""

    def test_processes_import(self):
        """Test processes module imports"""
        from projectwinactivation.utils.processes import (
            list_processes,
            get_system_uptime,
            format_bytes,
        )

        assert callable(list_processes)
        assert callable(get_system_uptime)

    def test_list_processes(self):
        """Test process listing"""
        from projectwinactivation.utils.processes import list_processes

        success, output = list_processes()
        assert isinstance(success, bool)
        assert isinstance(output, str)


class TestDisk:
    """Test disk module"""

    def test_disk_import(self):
        """Test disk module imports"""
        from projectwinactivation.utils.disk import (
            get_disk_space,
            get_temp_folder_size,
            format_bytes,
        )

        assert callable(get_disk_space)
        assert callable(get_temp_folder_size)

    def test_get_temp_folder_size(self):
        """Test temp folder size calculation"""
        from projectwinactivation.utils.disk import get_temp_folder_size

        size = get_temp_folder_size()
        assert isinstance(size, int)
        assert size >= 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
