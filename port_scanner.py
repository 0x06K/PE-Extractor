import socket
from threading import Semaphore, Thread  # Ensure Thread is imported here
from tqdm import tqdm
import time
import resource  # For adjusting file descriptor limits
from colorama import init, Fore



class PortScanner:
    def __init__(self, target="127.0.0.1", max_threads=500):  # Reduced default max_threads
        self.target = target
        self.tcp_ports = []
        self.udp_ports = []
        self.max_threads = max_threads
        
        # Set system limits for file descriptors
        try:
            soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
            resource.setrlimit(resource.RLIMIT_NOFILE, (max(soft, 4096), hard))
            max_threads = min(max_threads, soft // 2)
        except Exception as e:
            print(f"{Fore.YELLOW}[!] Warning: Could not adjust system limits: {e}")
            max_threads = 256  # Fall back to a conservative value
            
        self.semaphore = Semaphore(max_threads)
        print(f"{Fore.CYAN}[*] Running with {max_threads} maximum concurrent threads")
    def scan_common_ports(self):
        common_ports = {
            21: 'FTP',
            22: 'SSH',
            23: 'Telnet',
            25: 'SMTP',
            53: 'DNS',
            80: 'HTTP',
            110: 'POP3',
            123: 'NTP',
            143: 'IMAP',
            443: 'HTTPS',
            445: 'SMB',
            993: 'IMAP SSL',
            995: 'POP3 SSL',
            3306: 'MySQL',
            3389: 'RDP',
            5900: 'VNC',
            8080: 'HTTP Proxy'
        }
        
        ports = list(common_ports.keys())
        print(f"{Fore.CYAN}[*] Scanning common ports...")

        self.scan_ports(ports)

    def scan_custom_ports(self):
        while True:
            try:
                ports_input = input(f"{Fore.GREEN}Enter comma-separated list of ports to scan {Fore.YELLOW}(e.g., 80,443,8080){Fore.WHITE}: ")
                ports = [int(port.strip()) for port in ports_input.split(',')]
                if all(1 <= port <= 65535 for port in ports):
                    print(f"{Fore.CYAN}[*] Scanning specific ports provided by the user...")
                    self.scan_ports(ports)
                    return
                else:
                    print(f"{Fore.RED}[!] All ports must be between 1 and 65535!")
            except ValueError:
                print(f"{Fore.RED}[!] Please enter valid port numbers!")    
            

    def display_open_ports(self):
        print("\n\n")
        if len(self.tcp_ports) == 0:
            print(f"{Fore.GREEN}[+] {Fore.WHITE}No open TCP ports found.")
        
        for port, service in self.tcp_ports:
            print(f"{Fore.GREEN}[+] {Fore.WHITE}TCP port {Fore.CYAN}{port} {Fore.WHITE}({Fore.YELLOW}{service}{Fore.WHITE}) is open.")
            self.tcp_ports.clear()
        if len(self.udp_ports) == 0:
            print(f"{Fore.GREEN}[+] {Fore.WHITE}No open UDP ports found.\n\n")
        for port, service in self.udp_ports:
            print(f"{Fore.GREEN}[+] {Fore.WHITE}UDP port {Fore.CYAN}{port} {Fore.WHITE}({Fore.YELLOW}{service}{Fore.WHITE}) is open.")
            self.udp_ports.clear()
        

    def scan_tcp(self, port):
        sock = None
        if port < 1 or port > 65535:
            print(f"{Fore.RED}[!] Invalid port number: {port}. It must be between 1 and 65535.")
            return

        with self.semaphore:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((self.target, port))
                if result == 0:
                    service = self.get_service_name(port, "tcp")
                    self.tcp_ports.append((port, service))
            except socket.error as e:
                if e.errno == 24:  # Too many open files
                    time.sleep(0.1)  # Add a small delay
                    try:
                        if sock:
                            sock.close()
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(1)
                        result = sock.connect_ex((self.target, port))
                        if result == 0:
                            service = self.get_service_name(port, "tcp")
                            self.tcp_ports.append((port, service))
                    except Exception as retry_e:
                        print(f"{Fore.RED}[!] Error on retry for TCP port {port}: {retry_e}")
                else:
                    print(f"{Fore.RED}[!] Error scanning TCP port {port}: {e}")
            finally:
                if sock:
                    try:
                        sock.close()
                    except:
                        pass

    def scan_udp(self, port):
        sock = None
        if port < 1 or port > 65535:
            print(f"{Fore.RED}[!] Invalid port number: {port}. It must be between 1 and 65535.")
            return

        with self.semaphore:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(1)
                sock.sendto(b'', (self.target, port))
                sock.recvfrom(1024)
                service = self.get_service_name(port, "udp")
                self.udp_ports.append((port, service))
            except socket.timeout:
                pass
            except socket.error as e:
                if e.errno == 24:  # Too many open files
                    time.sleep(0.1)
                    try:
                        if sock:
                            sock.close()
                        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        sock.settimeout(1)
                        sock.sendto(b'', (self.target, port))
                        sock.recvfrom(1024)
                        service = self.get_service_name(port, "udp")
                        self.udp_ports.append((port, service))
                    except Exception:
                        pass
            finally:
                if sock:
                    try:
                        sock.close()
                    except:
                        pass

    def get_service_name(self, port, protocol):
        try:
            return socket.getservbyport(port, protocol)
        except:
            return "Unknown"

    def start_scan(self):
        while True:
            try:
                print(f"\n{Fore.CYAN}{'='*40}")
                print(f"{Fore.YELLOW}Enter Port Range")
                print(f"{Fore.CYAN}{'='*40}")
                
                start_port = input(f"{Fore.GREEN}Enter starting port {Fore.YELLOW}(1-65535){Fore.WHITE}: ")
                end_port = input(f"{Fore.GREEN}Enter ending port {Fore.YELLOW}(1-65535){Fore.WHITE}: ")
                
                start_port = int(start_port)
                end_port = int(end_port)
                
                if 1 <= start_port <= 65535 and 1 <= end_port <= 65535:
                    if start_port <= end_port:
                        ports = range(start_port, end_port + 1)
                        # Scan both TCP and UDP ports
                        self.scan_ports(ports)
                        return
                    else:
                        print(f"{Fore.RED}[!] Starting port must be less than or equal to ending port!")
                else:
                    print(f"{Fore.RED}[!] Ports must be between 1 and 65535!")
            except ValueError:
                print(f"{Fore.RED}[!] Please enter valid port numbers!")


    def scan_ports(self, ports):
        print(f"{Fore.CYAN}[*] Starting TCP scan...")
        tcp_threads = []

        with tqdm(total=len(ports), desc=f"{Fore.GREEN}Scanning TCP ports", bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.GREEN, Fore.RESET)) as pbar:
            for port in ports:
                thread = Thread(target=self.scan_tcp, args=(port,))
                thread.start()
                tcp_threads.append(thread)
                pbar.update(1)

        for thread in tcp_threads:
            thread.join()

        print(f"{Fore.CYAN}[*] TCP scan completed!")

        print(f"{Fore.CYAN}[*] Starting UDP scan...")
        udp_threads = []

        with tqdm(total=len(ports), desc=f"{Fore.GREEN}Scanning UDP ports", bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.GREEN, Fore.RESET)) as pbar:
            for port in ports:
                thread = Thread(target=self.scan_udp, args=(port,))
                thread.start()
                udp_threads.append(thread)
                pbar.update(1)

        for thread in udp_threads:
            thread.join()

        print(f"{Fore.CYAN}[*] UDP scan completed!")
