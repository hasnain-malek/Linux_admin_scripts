import os
import ssl
import http.server
import socketserver
import subprocess
import threading
import time
import readline
import signal

class GracefulShutdown:
    stop_now = False

def generate_self_signed_cert(cert_file, key_file):
    if not os.path.exists(cert_file) or not os.path.exists(key_file):
        print("Generating self-signed SSL certificate...")
        subprocess.run([
            "openssl", "req", "-new", "-x509", "-days", "365", "-nodes",
            "-out", cert_file, "-keyout", key_file,
            "-subj", "/CN=localhost"
        ], check=True)
        print("Certificate generated.")
    else:
        print("SSL certificate already exists. Skipping generation.")

def detect_package_manager():
    if os.path.exists("/usr/bin/apt"):
        return "apt"
    elif os.path.exists("/usr/bin/yum"):
        return "yum"
    return None

def install_firewalld(package_manager):
    if package_manager == "apt":
        print("Installing firewalld using apt...")
        subprocess.run(["sudo", "apt", "update"], check=True)
        subprocess.run(["sudo", "apt", "install", "-y", "firewalld"], check=True)
    elif package_manager == "yum":
        print("Installing firewalld using yum...")
        subprocess.run(["sudo", "yum", "install", "-y", "firewalld"], check=True)
    else:
        print("Unsupported package manager. Please install firewalld manually.")
        exit(1)
    
    subprocess.run(["sudo", "systemctl", "start", "firewalld"], check=True)
    subprocess.run(["sudo", "systemctl", "enable", "firewalld"], check=True)
    print("firewalld installed and started.")

def check_firewall(port):
    result = subprocess.run(["sudo", "firewall-cmd", "--list-ports"], capture_output=True, text=True)
    if f"{port}/tcp" not in result.stdout:
        print(f"Allowing port {port} through firewalld...")
        subprocess.run(["sudo", "firewall-cmd", "--add-port", f"{port}/tcp", "--permanent"], check=True)
        subprocess.run(["sudo", "firewall-cmd", "--reload"], check=True)
        print(f"Port {port} is now allowed through firewalld.")
    else:
        print(f"Port {port} is already allowed through firewalld. Skipping.")

def disable_firewall(port):
    print(f"Disabling port {port} in firewalld...")
    subprocess.run(["sudo", "firewall-cmd", "--remove-port", f"{port}/tcp", "--permanent"], check=True)
    subprocess.run(["sudo", "firewall-cmd", "--reload"], check=True)
    print(f"Port {port} is now disabled in firewalld.")

def start_https_server(directory, port, cert_file, key_file, duration):
    os.chdir(directory)

    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile=cert_file, keyfile=key_file)
    httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)

    def server_thread():
        print(f"Serving HTTPS on port {port} from {directory} for {duration} seconds")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            httpd.server_close()

    server_thread = threading.Thread(target=server_thread)
    server_thread.start()

    def shutdown_server():
        time.sleep(duration)
        if not GracefulShutdown.stop_now:
            print(f"Time's up! Stopping the server after {duration} seconds")
            httpd.shutdown()
            disable_firewall(port)
            print(f"Server stopped and port {port} closed")

    shutdown_thread = threading.Thread(target=shutdown_server)
    shutdown_thread.start()

    def signal_handler(sig, frame):
        GracefulShutdown.stop_now = True
        print("\nStopping the server (initiated by user)...")
        httpd.shutdown()
        disable_firewall(port)
        print(f"Server stopped and port {port} closed")

    signal.signal(signal.SIGINT, signal_handler)

    return port, directory, duration, cert_file, key_file

def complete_path(text, state):
    line = readline.get_line_buffer().split()
    if not line:
        return [text][state]
    return [x for x in os.listdir(line[0] if len(line) > 0 else '.') if x.startswith(text)][state]

if __name__ == "__main__":
    readline.set_completer_delims('\t')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete_path)

    cert_file = "/etc/ssl/certs/server.pem"
    key_file = "/etc/ssl/private/server.key"

    generate_self_signed_cert(cert_file, key_file)

    port = int(input("Enter the port to run the HTTPS server: "))
    directory = input("Enter the directory to serve: ")
    duration_input = input("Enter the duration to run the server (in seconds, max 300, default 300): ")
    duration = 300 if duration_input == "" else min(int(duration_input), 300)

    try:
        subprocess.run(["firewall-cmd", "--version"], check=True)
        print("firewalld is already installed.")
    except subprocess.CalledProcessError:
        package_manager = detect_package_manager()
        if package_manager:
            print(f"Detected package manager: {package_manager}")
            install_firewalld(package_manager)
        else:
            print("No supported package manager detected. Ensure firewalld is installed manually.")
            exit(1)
    
    check_firewall(port)

    port, directory, duration, cert_file, key_file = start_https_server(directory, port, cert_file, key_file, duration)

    server_ip = subprocess.getoutput('hostname -I').strip()
    curl_command = f"curl -k -O https://{server_ip}:{port}/<filename>"

    readme_content = f"""
Server Start Information:
-------------------------
SSL Certificate: {cert_file}
SSL Key: {key_file}
Port: {port}
Directory: {directory}
Duration: {duration} seconds

To download a file, use the following command:
{curl_command}
    """

    with open("server_readme.txt", "w") as readme_file:
        readme_file.write(readme_content)
    print(readme_content)

    print(f"\nServer running in the background. To stop it manually, press CTRL+C.")

