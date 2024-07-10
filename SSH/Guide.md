# SSH Setup Script

## Description

The SSH Setup Script automates the process of setting up SSH key-based authentication between a local Windows machine and a remote Linux server. It handles the generation of SSH keys, their transfer to the remote server, creation of SSH configuration files, and the generation of a Windows batch file for easy remote server login via SSH.

## Requirements

- **Operating System:** Windows
- **Software:** Python 3.x, Paramiko library
- **Access:** Administrative rights (for installing Python packages if not already installed)
- **Network:** Internet connectivity for package installation and remote server connectivity

## Script Flow

1. **Check SSH Installation:** Verifies if OpenSSH client is installed on the local machine.
2. **Test Internet Connectivity:** Ensures the local machine has internet access for package installation and remote server connectivity.
3. **Base Directory Selection:** Prompts the user to specify a base directory where `.ssh` directories will be created for each remote server.
4. **Input Remote Server Details:** Gathers IP/hostname and username for the remote server.
5. **Check Remote Host Availability:** Pings the remote server to verify its availability.
6. **Setup SSH Keys:** Generates SSH key pair (`id_rsa` and `id_rsa.pub`) if not already present in the specified `.ssh` directory. Ensures proper permissions.
7. **Setup SSH on Remote Server:** Copies the generated public key to the remote server's `authorized_keys` file for SSH authentication.
8. **Generate SSH Config File:** Creates an SSH configuration file (`config`) in the `.ssh` directory, specifying the remote server's details and SSH key location.
9. **Generate Windows Batch File:** Creates a `.bat` file for easy SSH login to the remote server via Command Prompt, using the SSH configuration file.

## Usage

1. **Install Python:** Ensure Python 3.x is installed on your Windows machine.
2. **Install Paramiko:** Run `pip install paramiko` to install the Paramiko library if not already installed.
3. **Download Script:** Save the `ssh_setup.py` script on your local machine.
4. **Run Script:**
   - Open Command Prompt.
   - Navigate to the directory containing `ssh_setup.py`.
   - Run the script using Python:
     ```bash
     python ssh_setup.py
     ```
5. **Follow Prompts:** Enter the required details as prompted by the script.
6. **Use Generated `.bat` File:** After script completion, use the generated `.bat` file to open a Command Prompt window and login to the remote server via SSH with a single click.
