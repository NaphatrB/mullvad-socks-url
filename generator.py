import requests
import urllib.parse
import re
import os

# Load API URL from environment variable
api_url = os.getenv("MULLVAD_API_URL")
if not api_url:
    print("Error: MULLVAD_API_URL environment variable not set.")
    exit(1)

# Ensure the result folder exists
output_dir = 'result'
os.makedirs(output_dir, exist_ok=True)

# Fetch Mullvad WireGuard relays
try:
    r = requests.get(api_url, timeout=10).json()
except requests.RequestException as e:
    print(f"Error fetching Mullvad API: {e}")
    exit(1)

# Create SOCKS5 URLs using socks_name and custom name
socks5_urls = []

# Regular expression to extract numeric part from hostname (e.g., '001' from 'al-tia-wg-001')
number_pattern = re.compile(r'\d+$')

for host in r:
    if host['socks_name'] and host['active']:
        total_proxies += 1
        match = number_pattern.search(host['hostname'])
        number = match.group(0) if match else host['hostname']
        custom_name = f"{host['country_name']} {host['city_name']} {number}"
        custom_name_encoded = urllib.parse.quote(custom_name)
        socks5_url = f"socks5://{host['socks_name']}:1080/#{custom_name_encoded}"
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
