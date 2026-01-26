import speedtest
import subprocess
import platform
import uuid

# --- Conversion Function ---

def hex_to_dotted_decimal(hex_mask):
    """
    Converts hexadecimal subnet mask (e.g., '0xffffff00') to dotted-decimal notation.
    Returns the dotted-decimal format (e.g., '255.255.255.0') or the original if conversion fails.
    """
    if not hex_mask.startswith('0x'):
        return hex_mask
    
    try:
        hex_value = hex_mask.replace('0x', '')
        octets = [hex_value[i:i+2] for i in range(0, len(hex_value), 2)]
        decimal_str = ".".join([str(int(o, 16)) for o in octets])
        return decimal_str
    except Exception:
        return hex_mask


def get_mac_address():
    """
    Retrieves the MAC address of the primary network interface.
    Returns the MAC address as a string (e.g., '00:1a:2b:3c:4d:5e') or 'Unknown'.
    """
    try:
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        return ':'.join([mac[i:i+2] for i in range(0, 12, 2)])
    except Exception:
        return "Unknown"


def mask_to_cidr(raw_mask):
    """
    Converts a subnet mask (hex or dotted-decimal) to CIDR notation.
    Returns the CIDR prefix (e.g., '24') or the original mask if conversion fails.
    """

    if raw_mask.startswith('0x'):
        try:
            hex_value = raw_mask.replace('0x', '')
            octets = [hex_value[i:i+2] for i in range(0, len(hex_value), 2)]
            decimal_str = ".".join([str(int(o, 16)) for o in octets])
        except Exception:
            return raw_mask
    else:
        decimal_str = raw_mask

    try:
        octets = decimal_str.split('.')
        if len(octets) != 4:
            return raw_mask 
            
        binary_str = ''.join(format(int(octet), '08b') for octet in octets)
        cidr_prefix = str(binary_str.count('1'))
        
        return cidr_prefix
    
    except Exception:
        return raw_mask

# --- Main Network Function ---

def test_speed():
    """Tests download/upload speed."""
    print("🔹 Testing Internet speed...")
    st = speedtest.Speedtest()
    st.get_best_server()
    download = st.download() / 1_000_000  # bits → Mbit/s
    upload = st.upload() / 1_000_000
    ping = st.results.ping
    server_name = st.results.server['name']
    server_country = st.results.server['country']
    print(f"🌍 Connected to {server_name}, {server_country}")
    print(f"✅ Ping: {ping:.2f} ms | ↓ {download:.2f} Mbps | ↑ {upload:.2f} Mbps")
    return ping, download, upload

def network():
    """Retrieves the public IP and local subnet mask."""
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        public_ip = st.results.client['ip']
    except Exception as e:
        print(f"Warning: Could not get public IP via speedtest: {e}")
        public_ip = "Unknown"

    subnet_mask = "Unknown"
    local_netmask = "Unknown"
    is_windows = platform.system().lower() == "windows"

    local_ip = "Unknown"
    try:
        command = ["ipconfig"] if is_windows else ["ifconfig"]
        
        result = subprocess.run(
            command,
            capture_output=True, text=True, check=False
        )
        
        output = result.stdout
        
        for line in output.splitlines():
            if "Subnet Mask" in line and is_windows:
                subnet_mask = line.split(":")[-1].strip()
            elif "netmask" in line and not is_windows:
                parts = line.split()
                try:
                    netmask_index = parts.index('netmask')
                    local_netmask = parts[netmask_index + 1]
                except ValueError:
                    continue
            
            if "inet" in line and "127.0.0.1" not in line and "inet6" not in line:
                parts = line.split()
                try:
                    if not is_windows and 'inet' in parts:
                        inet_index = parts.index('inet') + 1
                        local_ip = parts[inet_index]
                        
                        # Handle old ifconfig format
                        if local_ip.startswith("addr:"):
                            local_ip = local_ip.split("addr:")[1]

                    elif is_windows and "IPv4 Address" in line:
                        local_ip = line.split(":")[-1].strip()

                except ValueError:
                    continue
    
            
    except Exception as e:
        print(f"Error retrieving local network info: {e}")

    # Convert hex netmask to dotted-decimal format if needed
    if is_windows:
        netmask = subnet_mask
    else:
        netmask = hex_to_dotted_decimal(local_netmask)

    cidr = mask_to_cidr(netmask)

    # Returns public IP, local IP, and netmask
    return public_ip, local_ip, netmask, cidr

