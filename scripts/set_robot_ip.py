import argparse
import ctypes
import os
import subprocess
import sys


def is_admin():
    """Check if the script is running with administrative privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print(f"Error checking admin privileges: {e}")
        return False


def set_static_ip(interface_name="Ethernet", ip="192.168.5.10", subnet="255.255.255.0"):
    """Set the specified network interface to a static IP address."""
    print(f"Setting '{interface_name}' to static IP {ip} with subnet {subnet}...")

    # netsh interface ip set address name="Ethernet" static 192.168.5.10 255.255.255.0
    cmd = f'netsh interface ip set address name="{interface_name}" static {ip} {subnet}'

    try:
        result = subprocess.run(
            cmd, shell=True, check=True, capture_output=True, text=True
        )
        print("Successfully set static IP.")
        if result.stdout.strip():
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Failed to set static IP. Error code: {e.returncode}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        if e.stdout:
            print(f"Output: {e.stdout}")


def set_dhcp(interface_name="Ethernet"):
    """Set the specified network interface to use DHCP (automatic IP)."""
    print(f"Setting '{interface_name}' to DHCP...")

    # netsh interface ip set address name="Ethernet" source=dhcp
    cmd = f'netsh interface ip set address name="{interface_name}" source=dhcp'

    try:
        result = subprocess.run(
            cmd, shell=True, check=True, capture_output=True, text=True
        )
        print("Successfully set to DHCP.")
        if result.stdout.strip():
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Failed to set DHCP. Error code: {e.returncode}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        if e.stdout:
            print(f"Output: {e.stdout}")


if __name__ == "__main__":
    # Check for admin rights
    if not is_admin():
        print("Requesting administrative privileges...")
        # Re-run the program with admin rights
        # sys.argv[0] is the script name, sys.argv[1:] are the arguments
        script = os.path.abspath(sys.argv[0])
        params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])

        # ShellExecuteW(hwnd, op, file, params, dir, show)
        # 1 = SW_SHOWNORMAL
        ret = ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, f'"{script}" {params}', None, 1
        )

        if ret <= 32:
            print(f"Failed to elevate privileges. Error code: {ret}")
            input("Press Enter to exit...")
        sys.exit()

    print("Running with administrative privileges.\n")

    parser = argparse.ArgumentParser(
        description="Configure network interface for Dobot connection."
    )
    parser.add_argument(
        "--dhcp",
        action="store_true",
        help="Revert the interface to DHCP (automatic IP)",
    )
    parser.add_argument(
        "--ip",
        type=str,
        default="192.168.5.10",
        help="Static IP address to set (default: 192.168.5.10)",
    )
    parser.add_argument(
        "--subnet",
        type=str,
        default="255.255.255.0",
        help="Subnet mask (default: 255.255.255.0)",
    )
    parser.add_argument(
        "--interface",
        type=str,
        default="Ethernet",
        help="Network interface name (default: Ethernet)",
    )

    args = parser.parse_args()

    if args.dhcp:
        set_dhcp(interface_name=args.interface)
    else:
        set_static_ip(interface_name=args.interface, ip=args.ip, subnet=args.subnet)
        print(
            "\nTip: Run this script with '--dhcp' to revert to automatic IP assignment."
        )

    # Pause so the user can read the output in the new console window
    input("\nPress Enter to exit...")
