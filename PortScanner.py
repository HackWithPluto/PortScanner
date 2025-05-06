import socket
import time
import concurrent.futures
import sys
import os
import platform
import subprocess

# Red color code for text
class Colors:
    RED = '\033[91m'
    RESET = '\033[0m'

# SHUBH ASCII art in red color
shubh_art = r"""
 ____   _      _   _  _____   ___  
|  _ \ | |    | | | ||_   _| / _ \ 
| |_) || |    | | | |  | |  | | | |
|  __/ | |___ | |_| |  | |  | |_| |
|_|    |_____| \___/   |_|   \___/ 
                 By shubham Dongare
"""

def print_shubh_art():
    
    for char in shubh_art:
        sys.stdout.write(Colors.RED + char)
        sys.stdout.flush()
        time.sleep(0.005)
    print(Colors.RESET)

def pause_and_return():
    input("Press Enter to return to the Main Menu...")
    os.system('cls' if os.name == 'nt' else 'clear')

class TCPPortScanner:
    def __init__(self):
        self.open_ports = []
        self.closed_ports = []
        self.filtered_ports = []
        self.scan_stats = {
            'ports_scanned': 0,
            'start_time': 0
        }

    def tcp_connect_scan(self, target, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target, port))
            sock.close()

            if result == 0:
                self.open_ports.append(port)
            else:
                self.closed_ports.append(port)
        except:
            self.filtered_ports.append(port)

    def scan_ports(self, target, ports, threads=100):
        self.scan_stats['start_time'] = time.time()
        self.scan_stats['ports_scanned'] = len(ports)

        print("\nScanning", end="")
        for _ in range(10):
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(0.1)

        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(lambda port: self.tcp_connect_scan(target, port), ports)

    def print_results(self):
        print("\nScan Results:")
        print(f"Open ports: {sorted(self.open_ports)}")
        print(f"Closed ports: {sorted(self.closed_ports)}")
        print(f"Filtered ports: {sorted(self.filtered_ports)}")

        duration = time.time() - self.scan_stats['start_time']
        print(f"Scan completed in {duration:.2f} seconds")
        print(f"Scanned {self.scan_stats['ports_scanned']} ports")

def parse_ports(port_str):
    ports = []
    for part in port_str.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            ports.extend(range(start, end + 1))
        else:
            ports.append(int(part))
    return ports

def check_target_reachability(target):
    param = '-n' if platform.system().lower() == 'windows' else '-c'

    try:
        response = subprocess.call(["ping", param, "1", target], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if response == 0:
            print(f"Target {target} is reachable.")
            return True
        else:
            print(f"Target {target} is not reachable.")
            return False
    except Exception as e:
        print(f"An error occurred while checking reachability: {e}")
        return False

def print_help():
    try:
        with open("README.md", "r") as file:
            print("\nHelp File Contents:\n")
            print(file.read())
    except FileNotFoundError:
        print("help not found.")

def main():
    while True:
        print_shubh_art()
        print("--------Main Menu--------")
        print("1: Scan Ports")
        print("2: Help")
        print("3: Exit")
        choice = input(">>> Enter your choice (1-3): ").strip()

        if choice == '1':
            target = input(">>> Enter the target IP or hostname: ")

            if not check_target_reachability(target):
                print(">>> Exiting... Target is not reachable.")
                pause_and_return()
                continue

            ports_input = input(">>> Enter ports to scan (e.g., 80,443 or 1-1000): ")
            if not ports_input:
                print("No ports entered. Exiting...")
                pause_and_return()
                continue

            try:
                ports = parse_ports(ports_input)
            except ValueError:
                print("Invalid port specification")
                pause_and_return()
                continue

            threads = input(">>> Enter the number of threads (default: 100): ")
            threads = int(threads) if threads else 100

            scanner = TCPPortScanner()
            scanner.scan_ports(target, ports, threads)
            scanner.print_results()
            pause_and_return()

        elif choice == '2':
            print_help()
            pause_and_return()

        elif choice == '3':
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Try again.")
            pause_and_return()

if __name__ == "__main__":
    main()
