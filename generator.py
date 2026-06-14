import requests
import urllib.parse
import re
import os
import socket

API_URL = "https://api.mullvad.net/network/v1-beta1/socks-proxies"

# Ensure the result folder exists
output_dir = 'result'
os.makedirs(output_dir, exist_ok=True)

# Fetch Mullvad SOCKS proxies
try:
    r = requests.get(API_URL, timeout=10).json()
except requests.RequestException as e:
    print(f"Error fetching Mullvad API: {e}")
    exit(1)

# Create SOCKS5 URLs using hostname and custom name
socks5_urls = []
socks5_ip_urls = []
domains = []
ips = []

# Regular expression to extract numeric part from hostname (e.g., '003' from 'al-tia-wg-socks5-003')
number_pattern = re.compile(r'\d+')

for host in r:
    if host.get('online'):
        hostname = host['hostname']
        numbers = number_pattern.findall(hostname)
        number = numbers[-1] if numbers else hostname
        custom_name = f"{host['location']['country']} {host['location']['city']} {number}"
        custom_name_encoded = urllib.parse.quote(custom_name)
        socks5_url = f"socks5://{hostname}:1080/#{custom_name_encoded}"
        socks5_urls.append(socks5_url)
        domains.append(hostname)

        # Resolve hostname to IP
        try:
            ip = socket.gethostbyname(hostname)
            ips.append(ip)
            socks5_ip_urls.append(f"socks5://{ip}:1080/#{custom_name_encoded}")
        except socket.gaierror:
            pass

# Save SOCKS5 URLs to a text file in the result folder
output_path = os.path.join(output_dir, 'mullvad_socks5_urls.txt')
try:
    with open(output_path, 'w') as f:
        for url in socks5_urls:
            f.write(url + "\n")
except IOError as e:
    print(f"Error writing output file: {e}")
    exit(1)

# Save domains to a text file in the result folder
domains_path = os.path.join(output_dir, 'mullvad_socks5_domains.txt')
try:
    with open(domains_path, 'w') as f:
        for domain in domains:
            f.write(domain + "\n")
except IOError as e:
    print(f"Error writing domains file: {e}")
    exit(1)

# Save resolved IPs to a text file in the result folder
ips_path = os.path.join(output_dir, 'mullvad_socks5_ips.txt')
try:
    with open(ips_path, 'w') as f:
        for ip in ips:
            f.write(ip + "\n")
except IOError as e:
    print(f"Error writing IPs file: {e}")
    exit(1)

# Save SOCKS5 IP URLs to a text file in the result folder
ip_urls_path = os.path.join(output_dir, 'mullvad_socks5_ip_urls.txt')
try:
    with open(ip_urls_path, 'w') as f:
        for url in socks5_ip_urls:
            f.write(url + "\n")
except IOError as e:
    print(f"Error writing IP URLs file: {e}")
    exit(1)
