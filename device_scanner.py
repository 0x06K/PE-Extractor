from scapy.all import ARP, Ether, srp
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def send_arp_request(ip):
    """Function to send ARP request for a single IP address."""
    arp_request = ARP(pdst=ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp_request

    # Send the packet and get the response
    result = srp(packet, timeout=2, verbose=False)[0]

    # Collect the devices that responded
    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})
    return devices

def arp_scan(ip_range):
    """Scan the specified IP range using multithreading."""
    # Split the IP range into its components
    ip_parts = ip_range.split('.')
    if len(ip_parts) < 2:
        raise ValueError("Invalid IP range. Please provide a valid range in the format x.x.x.x/y.")
    
    # Get the first two octets
    ip_base = f"{ip_parts[0]}.{ip_parts[1]}"
    
    # Create a list of IP addresses for the last two octets (0-255)
    ip_addresses = [f"{ip_base}.{i}.{j}" for i in range(0, 256) for j in range(0, 256)]

    devices = []
    with ThreadPoolExecutor(max_workers=50) as executor:  # Increased the number of threads
        futures = {executor.submit(send_arp_request, ip): ip for ip in ip_addresses}

        # Use tqdm to show progress
        for future in tqdm(as_completed(futures), total=len(futures), desc="Scanning devices"):
            result = future.result()
            devices.extend(result)

    return devices

if __name__ == "__main__":
    ip_range = "172.27.0.0/16"  # Change this to your network's range
    connected_devices = arp_scan(ip_range)

    print("Connected devices:")
    for device in connected_devices:
        print(f"IP: {device['ip']} | MAC: {device['mac']}")
