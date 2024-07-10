#!/bin/bash

# Check if the script is run as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root"
    exit 1
fi

# Function to pause for 10 seconds
pause_for_summary() {
    echo "$1"
    sleep 10
}

# Check disk space and list available disks
echo "Available disks:"
lsblk

# Ask user to select the disk
read -p "Enter the disk to use (e.g., sda, sdb): " disk

# Create Physical Volume (PV)
pvcreate /dev/$disk

# Ask user for Volume Group (VG) name
read -p "Enter the name for the Volume Group (VG): " vgname

# Create Volume Group (VG)
vgcreate $vgname /dev/$disk

# Ask user for Logical Volume (LV) name and size
read -p "Enter the name for the Logical Volume (LV): " lvname
read -p "Enter the size for the Logical Volume (LV) (e.g., 10G): " lvsize

# Create Logical Volume (LV)
lvcreate -L $lvsize -n $lvname $vgname

# Determine the filesystem type
if command -v mkfs.ext4 &> /dev/null; then
    fstype="ext4"
elif command -v mkfs.ext3 &> /dev/null; then
    fstype="ext3"
elif command -v mkfs.ext2 &> /dev/null; then
    fstype="ext2"
else
    echo "No supported filesystem type found."
    exit 1
fi

# Create the filesystem on the LV
mkfs -t $fstype /dev/$vgname/$lvname

# Create mount point
mount_point="/mnt/${lvname}_access"
mkdir -p $mount_point

# Ask user if they want to mount it permanently or temporarily
read -p "Do you want to mount the LV permanently or temporarily? (perm/temp): " mount_choice

# Mount the LV
mount /dev/$vgname/$lvname $mount_point

if [ "$mount_choice" == "perm" ]; then
    # Get the UUID of the LV
    uuid=$(blkid -s UUID -o value /dev/$vgname/$lvname)
    
    # Add entry to /etc/fstab
    echo "UUID=$uuid $mount_point $fstype defaults 0 0" >> /etc/fstab
fi

# Display summary
summary="LVM Setup Summary:
Disk: /dev/$disk
VG Name: $vgname
LV Name: $lvname
LV Size: $lvsize
Filesystem: $fstype
Mount Point: $mount_point
Mounted: $(mount | grep $mount_point)"
pause_for_summary "$summary"

echo "LVM setup is complete."
