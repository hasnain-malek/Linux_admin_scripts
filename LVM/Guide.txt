# Auto LVM Setup Script

## Description

The Auto LVM Setup Script automates the setup of Logical Volume Management (LVM) on a Linux system. It facilitates the creation of Physical Volumes (PV), Volume Groups (VG), Logical Volumes (LV), formatting of LVs, and optionally mounting them either temporarily or permanently.

## Requirements

- **Operating System:** Linux
- **Access:** Root or sudo privileges
- **Storage:** Additional unallocated space for LVM
- **Software:** Basic Linux utilities (`fdisk`, `pvcreate`, `vgcreate`, `lvcreate`, `mkfs`, `mount`)

## Script Flow

1. **Disk Selection:** Lists available disks and prompts for selection to create Physical Volumes (PVs).
2. **PV Creation:** Initializes selected disks as Physical Volumes (PVs) for LVM.
3. **Volume Group (VG) Creation:** Prompts for creating a Volume Group (VG) using available PVs.
4. **Logical Volume (LV) Creation:** Guides through creating Logical Volumes (LVs) within the VG.
5. **Formatting and Mounting:** Offers options to format LVs and mount them temporarily or permanently.
6. **Automated or Manual Mounting:** Allows choosing between automatic or manual mounting of LVs.

## Usage

1. **Download Script:** Save the `auto_lvm_setup.sh` script on your Linux machine.
2. **Grant Permissions:** Ensure the script is executable: `chmod +x auto_lvm_setup.sh`.
3. **Run Script:**
   - Open Terminal.
   - Navigate to the directory containing `auto_lvm_setup.sh`.
   - Execute the script with root or sudo privileges:
     ```bash
     sudo ./auto_lvm_setup.sh
     ```
4. **Follow Prompts:** Respond to the script prompts to configure LVM according to your requirements.
5. **Review and Confirm:** Review the changes proposed by the script before proceeding.
6. **Complete Setup:** Once the script completes, verify the setup by checking LVs and mounts.

---

This Markdown content outlines the purpose, requirements, flow, and usage instructions for your Auto LVM Setup Script. Adjust any details as per your specific script implementation and preferences.
