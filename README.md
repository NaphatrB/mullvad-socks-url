# Mullvad SOCKS5 URL Generator

This Python script fetches online SOCKS proxies from the Mullvad API and generates a list of SOCKS5 URLs in the format `socks5://hostname:1080/#country_name%20city_name%20number`. It uses the `hostname` field as the server address and constructs a custom node name from `country_name`, `city_name`, and the numeric part of `hostname` (e.g., `003` from `al-tia-wg-socks5-003`).

## Features
- Fetches online Mullvad SOCKS proxies from `https://api.mullvad.net/network/v1-beta1/socks-proxies`, filtering by `online: true`.
- Generates URLs with `hostname` as the server and `country_name city_name number` as the node name (e.g., `socks5://al-tia-wg-socks5-001.relays.mullvad.net:1080/#Albania%20Tirana%20001`).
- Saves output to `mullvad_socks5_urls.txt`.

## Requirements
- Python 3.6 or later
- Dependencies listed in `requirements.txt`: