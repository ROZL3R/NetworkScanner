import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor
import time

def display_banner():
    banner = """
    ╔═╗┌─┐┬─┐┌┬┐  ╔═╗┌─┐┌─┐┌┐┌┌┐┌┌─┐┬─┐
    ╠═╝│ │├┬┘ │   ╚═╗│  ├─┤││││││├┤ ├┬┘
    ╩  └─┘┴└─ ┴   ╚═╝└─┘┴ ┴┘└┘┘└┘└─┘┴└─
    """
    print(banner)

def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            return s.connect_ex((ip, port)) == 0
    except:
        return False

def scan_host(ip, start_port, end_port):
    print(f"\nScanning {ip}...")
    
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [
            executor.submit(scan_port, ip, port)
            for port in range(start_port, end_port + 1)
        ]
        
        for port, future in enumerate(futures, start=start_port):
            if future.result():
                print(f"Port {port} is open")

if __name__ == "__main__":
    display_banner()
    
    try:
        network = input("Enter network (e.g., 192.168.1.0/24): ")
        start_port = int(input("Start port: "))
        end_port = int(input("End port: "))
        
        net = ipaddress.ip_network(network, strict=False)
        for ip in net.hosts():
            scan_host(str(ip), start_port, end_port)
            
    except KeyboardInterrupt:
        print("Scan stopped by user")
    except Exception as e:
        print(f"Error: {e}")