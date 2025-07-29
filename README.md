# Mullvad SOCKS5 URL Generator

This Python script fetches active WireGuard relays from the Mullvad API and generates a list of SOCKS5 URLs in the format `socks5://socks_name:1080/#country_name%20city_name%20number`. It uses the `socks_name` field as the server address and constructs a custom node name from `country_name`, `city_name`, and the numeric part of `hostname` (e.g., `001` from `al-tia-wg-001`).

## Features
- Fetches active Mullvad WireGuard relays from `https://api.mullvad.net/www/relays/wireguard/`.
- Generates URLs with `socks_name` as the server and `country_name city_name number` as the node name (e.g., `socks5://al-tia-wg-socks5-001-wireguard:1080/#Albania%20Tirana%20001`).
- Saves output to `mullvad_socks5_urls.txt`.

## Requirements
- Python 3.6 or later
- Dependencies listed in `requirements.txt`: