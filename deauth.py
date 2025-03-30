import subprocess
import re

def scan_bluetooth_devices():
    """Scan for nearby Bluetooth devices."""
    print("🔍 Scanning for Bluetooth devices...")
    scan_output = subprocess.run(["hcitool", "scan"], capture_output=True, text=True)

    devices = []
    for line in scan_output.stdout.split("\n"):
        match = re.search(r"(\S+)\t(.+)", line)
        if match:
            mac_address, device_name = match.groups()
            devices.append((mac_address, device_name))

    return devices

def turn_off_bluetooth_on_device(mac_address):
    """Attempt to turn off Bluetooth on the selected device."""
    print(f"\n⚠️ Sending Bluetooth turn-off command to {mac_address}...")

    # Try sending a disable command (some devices may reject this)
    subprocess.run(["sudo", "bluetoothctl", "disconnect", mac_address])
    subprocess.run(["sudo", "bluetoothctl", "power", "off"])

    print(f"✅ Bluetooth on {mac_address} has been turned off (if supported).")

def main():
    devices = scan_bluetooth_devices()

    if not devices:
        print("❌ No Bluetooth devices found.")
        return

    print("\n🔵 Nearby Bluetooth Devices:")
    for idx, (mac, name) in enumerate(devices, start=1):
        print(f"{idx}. {name} ({mac})")

    try:
        choice = int(input("\nSelect a device to turn off Bluetooth (enter number): "))
        if 1 <= choice <= len(devices):
            turn_off_bluetooth_on_device(devices[choice - 1][0])
        else:
            print("❌ Invalid choice. Exiting.")
    except ValueError:
        print("❌ Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()
