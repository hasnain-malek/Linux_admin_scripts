import os
import subprocess
import paramiko
from pathlib import Path
import getpass

# Function to check if OpenSSH client is installed
def check_ssh_installation():
    try:
        subprocess.run(["ssh", "-V"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("OpenSSH client is installed.")
    except subprocess.CalledProcessError:
        print("OpenSSH client is not installed. Please install OpenSSH.")
        exit(1)

# Function to check internet connectivity
def test_internet():
    try:
        subprocess.run(["ping", "-n", "1", "google.com"], check=True)
    except subprocess.CalledProcessError:
        print("No internet connection. Please check your network settings.")
        exit(1)

# Function to gather user input for remote server details
def get_remote_server_details():
    remote_host = input("Enter remote host IP or hostname: ")
    remote_user = input("Enter remote username: ")
    return remote_host, remote_user

# Function to create SSH directory and generate keys
def setup_ssh_keys(ssh_dir):
    key_name = "id_rsa"

    if not ssh_dir.exists():
        ssh_dir.mkdir(parents=True)

    public_key_path = ssh_dir / f"{key_name}.pub"
    private_key_path = ssh_dir / key_name

    if not public_key_path.exists():
        subprocess.run(["ssh-keygen", "-t", "rsa", "-b", "4096", "-f", str(private_key_path), "-N", "", "-q"])
        print("SSH key pair generated.")
    else:
        print("SSH key pair already exists.")

    return public_key_path, private_key_path

# Function to check remote host availability
def test_remote_host(remote_host):
    try:
        subprocess.run(["ping", "-n", "1", remote_host], check=True)
    except subprocess.CalledProcessError:
        print(f"Remote host {remote_host} is down. Please contact your administrator.")
        exit(1)

# Function to setup SSH on remote server
def setup_ssh_on_remote(remote_host, remote_user, public_key_path):
    with open(public_key_path, 'r') as file:
        public_key_content = file.read()

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    while True:
        try:
            password = getpass.getpass(prompt="Enter remote user's password: ")
            ssh.connect(remote_host, username=remote_user, password=password)
            ssh_command = f"""
            mkdir -p ~/.ssh && chmod 700 ~/.ssh &&
            echo '{public_key_content}' >> ~/.ssh/authorized_keys &&
            chmod 600 ~/.ssh/authorized_keys
            """
            stdin, stdout, stderr = ssh.exec_command(ssh_command)
            stdout.channel.recv_exit_status()
            ssh.close()
            print("Public key copied to remote server.")
            break
        except paramiko.ssh_exception.AuthenticationException:
            print("Authentication failed. Please try again.")

# Function to generate SSH config file
def generate_config_file(remote_host, remote_user, ssh_dir):
    config_content = f"""
    Host {remote_host}
        HostName {remote_host}
        User {remote_user}
        IdentityFile {ssh_dir}/id_rsa
        IdentitiesOnly yes
    """
    config_path = ssh_dir / f"{remote_host}.config"
    with open(config_path, 'w') as file:
        file.write(config_content)
    print(f"Configuration file generated: {config_path}")
    return config_path

# Function to generate a .bat file for Windows to open CMD and log in
def generate_bat_file(remote_host, config_path, ssh_dir):
    bat_content = f"""
    @echo off
    start cmd /k "ssh -F {config_path} {remote_host}"
    """
    bat_path = ssh_dir / f"login_{remote_host}.bat"
    with open(bat_path, 'w') as file:
        file.write(bat_content)
    print(f"Batch file generated: {bat_path}")

# Main script flow
if __name__ == "__main__":
    check_ssh_installation()
    test_internet()

    base_ssh_dir_path = input("Enter the base directory where you want to create the .ssh directories: ")
    base_ssh_dir = Path(base_ssh_dir_path)

    remote_host, remote_user = get_remote_server_details()
    test_remote_host(remote_host)

    server_ssh_dir = base_ssh_dir / f".ssh_{remote_host.replace('.', '_')}"
    public_key_path, private_key_path = setup_ssh_keys(server_ssh_dir)
    setup_ssh_on_remote(remote_host, remote_user, public_key_path)

    config_path = generate_config_file(remote_host, remote_user, server_ssh_dir)
    generate_bat_file(remote_host, config_path, server_ssh_dir)

    print("Setup completed successfully.")
