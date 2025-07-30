import requests
import urllib.parse
import re
import os

# Ensure the result folder exists
output_dir = 'result'
os.makedirs(output_dir, exist_ok=True)

# Fetch Mullvad WireGuard relays
try:
    r = requests.get('https://api.mullvad.net/www/relays/wireguard/', timeout=10).json()
except requests.RequestException as e:
    print(f"Error fetching Mullvad API: {e}")
    exit(1)

# Create SOCKS5 URLs using socks_name and custom name
socks5_urls = []
total_proxies = 0

# Regular expression to extract the numeric part from hostname (e.g., '001' from 'al-tia-wg-001')
number_pattern = re.compile(r'\d+$')

for host in r:
    if host['socks_name'] is not None and host['active']:
        total_proxies += 1
        # Extract numeric part from hostname
        match = number_pattern.search(host['hostname'])
        number = match.group(0) if match else host['hostname']  # Fallback to full hostname if no number found
        # Create custom name: country_name city_name number
        custom_name = f"{host['country_name']} {host['city_name']} {number}"
        # Create SOCKS5 URL with custom name as fragment
        custom_name_encoded = urllib.parse.quote(custom_name)  # Encode spaces and special characters
        socks5_url = f"socks5://{host['socks_name']}:1080/#{custom_name_encoded}"
        socks5_urls.append(socks5_url)

print(f"Total active proxies: {total_proxies}")

# Save SOCKS5 URLs to a text file in the result folder
output_path = os.path.join(output_dir, 'mullvad_socks5_urls.txt')
try:
    with open(output_path, 'w') as f:
        for url in socks5_urls:
            f.write(url + "\n")
    print(f"Saved SOCKS5 URLs to {output_path}")
except IOError as e:
    print(f"Error saving {output_path}: {e}")
    exit(1)

# Print SOCKS5 URLs for verification
print("\nGenerated SOCKS5 URLs:")
for url in socks5_urls:
    print(url)
