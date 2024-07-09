# Setup LVM Script

This script automates the setup of Logical Volume Management (LVM) on Linux.

## Features

- Creates a Physical Volume (PV), Volume Group (VG), and Logical Volume (LV).
- Formats the LV with a specified filesystem type.
- Mounts the LV temporarily or permanently based on user choice.
- Adds entry to `/etc/fstab` for permanent mounts.

## Usage

1. Clone the repository.
2. Make the script executable: `chmod +x setup_lvm.sh`.
3. Run the script with root privileges: `sudo ./setup_lvm.sh`.

## Notes

- Ensure you have the necessary filesystem tools (`e2fsprogs` for ext4, etc.) installed.
- Follow the prompts to select disks, specify names, sizes, and mount options.

