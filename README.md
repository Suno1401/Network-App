# 🌐 SUNO - Network Diagnostic Tool

A comprehensive Python application to test and diagnose the health of your network connection.

## 📋 Description

**SUNO** is a network diagnostic tool that performs several tests to verify the health of your Internet connection:
- ✅ **DNS Test** - Verifies domain name resolution
- ✅ **Ping Test** - Verifies connectivity to multiple servers
- ✅ **Speed Test** - Measures download/upload speeds
- ✅ **Network Information** - Displays your public IP, private IP, subnet mask, and MAC address

## 🚀 Features

| Feature | Description |
|---|---|
| **DNS Test** | Tests DNS resolution for Google, GitHub, and Cloudflare |
| **Ping Test** | Pings to Google DNS (8.8.8.8) and Cloudflare (1.1.1.1) |
| **Speed Test** | Measures download/upload speeds and latency |
| **Network Info** | Displays public IP, private IP, subnet mask, and MAC address |
| **Logging** | Records all results in `network_app.log` |
| **Configurable Thresholds** | Set minimum acceptable speeds |

## 📁 Project Structure

```
Network-App/
├── app.py              # Main entry point
├── config.py           # Configuration (domains, hosts, thresholds)
├── test_dns.py         # DNS tests
├── test_ping.py        # Ping tests
├── test_speed.py       # Speed tests and network info
├── network_app.log     # Log file (generated)
├── README.md           # This file
└── LICENSE             # License
```

## 🔧 Installation

### Requirements
- Python 3.7+
- Internet access

### Install Dependencies

```bash
pip install speedtest-cli
```

## ▶️ Usage

Run the main application:

```bash
python app.py
```

### Example Output

```
##################
##   **SUNO** ##
##################

=== 🧰 NETWORK TEST ===

=== 📊 Summary ===
DNS OK : ✅
Ping OK : ✅
Download Speed : 45.32 Mbps
Upload Speed : 12.54 Mbps

=== 📊 DNS Results ===
🔹 www.google.com → 142.250.185.46

=== 📊 Info ===
🔹 Public IP : 203.0.113.42
🔹 Private IP : 192.168.1.100
🔹 Subnet Mask : 255.255.255.0 /24
🔹 MAC Address : a1:b2:c3:d4:e5:f6

✅ Network functional.
```

## ⚙️ Configuration

Edit `config.py` to customize:

### DNS Domains to Test
```python
DNS_DOMAINS = [
    "www.google.com",
    "www.github.com",
    "www.cloudflare.com"
]
```

### Ping Hosts
```python
PING_HOSTS = [
    "8.8.8.8",      # Google DNS
    "1.1.1.1",      # Cloudflare DNS 
]
```

### Speed Thresholds (in Mbps)
```python
SPEED_THRESHOLDS = {
    "min_download_mbps": 10,  # Minimum download speed
    "min_upload_mbps": 5,     # Minimum upload speed
}
```

### Log Level
Options: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
```python
LOGGING = {
    "level": "INFO",  # Change here
}
```

## 📊 Logging Results

Results are recorded in `network_app.log`:
```
[2026-01-26 14:32:15] INFO - =================================================
[2026-01-26 14:32:15] INFO - Network test started
[2026-01-26 14:32:25] INFO - DNS SUCCESS - www.google.com
[2026-01-26 14:32:30] INFO - PING SUCCESS - 8.8.8.8
```

## 📝 Modules

### `test_dns.py`
- `test_dns(domains=None)` - Tests DNS resolution
- Returns a list of dictionaries with success/resolved IP

### `test_ping.py`
- `ping(hosts=None)` - Performs ping tests
- `_ping_single_host(host)` - Pings a single host
- Returns success boolean

### `test_speed.py`
- `test_speed()` - Measures Internet speed
- `network()` - Gets public IP, private IP, subnet mask
- `get_mac_address()` - Gets MAC address
- `mask_to_cidr(raw_mask)` - Converts mask to CIDR notation
- `hex_to_dotted_decimal(hex_mask)` - Converts hex format to dotted-decimal

### `app.py`
- `main()` - Orchestrates tests and displays results

## 🐛 Troubleshooting

### "Warning: Could not get public IP via speedtest"
- Check your Internet connection
- Speed tests require a stable connection

### MAC Address shows "Unknown"
- This is normal on some virtual machines
- Use `ifconfig` (Mac/Linux) or `ipconfig` (Windows) to verify

### Slow Tests
- Speed test can take 1-2 minutes
- Avoid downloading/uploading while test is running

## 📄 License

See the [LICENSE](LICENSE) file

## 👨‍💻 Author

Created by Allan

---

**Need help?** Check `network_app.log` for more details on errors.
