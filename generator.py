import requests
import urllib.parse
import re
import os

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

# Save SOCKS5 URLs to a text file in the result folder
output_path = os.path.join(output_dir, 'mullvad_socks5_urls.txt')
try:
    with open(output_path, 'w') as f:
        for url in socks5_urls:
            f.write(url + "\n")
except IOError as e:
    print(f"Error writing output file: {e}")
    exit(1)
