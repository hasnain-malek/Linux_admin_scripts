import os

def check_firewalld_installed():
    if os.system("command -v firewall-cmd &>/dev/null") != 0:
        print("Firewalld is not installed. Installing...")
        os.system("sudo yum install -y firewalld")
        os.system("sudo systemctl start firewalld")
        os.system("sudo systemctl enable firewalld")
        print("Firewalld installed and started.")
    else:
        print("Firewalld is already installed.")

def get_active_zone():
    active_zone = os.popen("sudo firewall-cmd --get-active-zones | head -n 1").read().strip()
    return active_zone

def list_services():
    print("Available services:")
    os.system("sudo firewall-cmd --get-services")

def add_rich_rule(active_zone):
    family = input("Enter IP family (ipv4/ipv6): ").strip()
    source_address = input("Enter source address (IP or subnet): ").strip()
    option = input("Do you want to specify a port or a service name? (port/service): ").strip().lower()
    port = ""
    service_name = ""

    if option == "port":
        port = input("Enter port: ").strip()
        protocol = input("Enter protocol (tcp/udp): ").strip()
    elif option == "service":
        service_name = input("Enter service name: ").strip()
    else:
        print("Invalid option. Please choose either 'port' or 'service'.")
        return

    action = input("Enter action (accept/reject): ").strip()

    rule = f"rule family=\"{family}\" source address=\"{source_address}\""
    if port:
        rule += f" port port=\"{port}\" protocol=\"{protocol}\""
    if service_name:
        rule += f" service name=\"{service_name}\""
    rule += f" {action}"

    command = f"sudo firewall-cmd --zone={active_zone} --add-rich-rule='{rule}' --permanent"
    os.system(command)
    os.system("sudo firewall-cmd --reload")
    print("Rich rule added and firewall reloaded.")

def remove_rich_rule(active_zone):
    family = input("Enter IP family (ipv4/ipv6): ").strip()
    source_address = input("Enter source address (IP or subnet): ").strip()
    option = input("Do you want to specify a port or a service name? (port/service): ").strip().lower()
    port = ""
    service_name = ""

    if option == "port":
        port = input("Enter port: ").strip()
        protocol = input("Enter protocol (tcp/udp): ").strip()
    elif option == "service":
        service_name = input("Enter service name: ").strip()
    else:
        print("Invalid option. Please choose either 'port' or 'service'.")
        return

    action = input("Enter action (accept/reject): ").strip()

    rule = f"rule family=\"{family}\" source address=\"{source_address}\""
    if port:
        rule += f" port port=\"{port}\" protocol=\"{protocol}\""
    if service_name:
        rule += f" service name=\"{service_name}\""
    rule += f" {action}"

    command = f"sudo firewall-cmd --zone={active_zone} --remove-rich-rule='{rule}' --permanent"
    os.system(command)
    os.system("sudo firewall-cmd --reload")
    print("Rich rule removed and firewall reloaded.")

def main():
    check_firewalld_installed()

    active_zone = get_active_zone()
    print(f"Current active zone: {active_zone}")
    change_zone = input("Do you want to change the zone? (yes/no): ").strip().lower()
    if change_zone == 'yes':
        active_zone = input("Enter the zone to set: ").strip()

    while True:
        print("\nFirewallD Rule Management Script")
        print("1. List Available Services")
        print("2. Add a Rich Rule")
        print("3. Remove a Rich Rule")
        print("4. Exit")

        choice = input("Choose an option: ").strip()

        if choice == '1':
            list_services()
        elif choice == '2':
            add_rich_rule(active_zone)
        elif choice == '3':
            remove_rich_rule(active_zone)
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()
