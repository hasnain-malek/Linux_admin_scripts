# Secure HTTPS Server Script

## Overview

This script sets up a secure HTTPS server using a self-signed certificate. It allows the user to choose the port and directory to serve, configures the firewall to allow the chosen port, and stops the server after a specified duration (default 300 seconds). The server can also be stopped manually with `CTRL+C`.

## Features

- Generates a self-signed SSL certificate if not already present.
- Allows the user to choose the serving port and directory.
- Configures `firewalld` to allow the chosen port.
- Runs the server in the background, freeing the terminal for other tasks.
- Automatically stops the server after the specified duration and closes the firewall port.
- Provides a `curl` command for users to easily download files from the server.
- Supports tab-completion for directory paths.

## Requirements

- Python 3
- `firewalld` (installed and running)

## Installation

1. **Install Python 3** (if not already installed):
    ```bash
    sudo apt update
    sudo apt install python3
    ```

2. **Install `firewalld`** (if not already installed):
    ```bash
    sudo apt update
    sudo apt install firewalld
    sudo systemctl start firewalld
    sudo systemctl enable firewalld
    ```

## Script Usage

1. **Download the Script**

   Save the following script as `secure_https_server.py`.

2. **Run the Script**

    ```bash
    sudo python3 secure_https_server.py
    ```

3. **Follow the Prompts**
    - Enter the port number to run the HTTPS server.
    - Enter the directory to serve.
    - Enter the duration to run the server (in seconds, max 300, default 300).

4. **Access the Server**
    - The script will display a `curl` command to access the server from a remote PC.
    - Example:
      ```bash
      curl -k -O https://<server-ip>:<port>/<filename>
      ```

### Example Usage

```bash
sudo python3 secure_https_server.py
