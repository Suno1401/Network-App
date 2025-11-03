import speedtest
import subprocess
import platform

# --- Conversion Function ---

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
    print(f"✅ Ping: {ping:.2f} ms | ↓ {download:.2f} Mbps | ↑ {upload:.2f} Mbps")
    return ping, download, upload

def network():
    """Retrieves the public IP and local subnet mask."""
    st = speedtest.Speedtest()
    public_ip = st.results.client['ip']

    subnet_mask = "Unknown"
    local_netmask = "Unknown"
    is_windows = platform.system().lower() == "windows"

    try:
        command = ["ipconfig"] if is_windows else ["ifconfig"]
        
        result = subprocess.run(
            command,
            capture_output=True, text=True, check=False
        )
        
        output = result.stdout
        
        for line in output.splitlines():
            # 1. Capture Subnet Mask (Windows/Linux)
            if "Subnet Mask" in line and is_windows:
                subnet_mask = line.split(":")[-1].strip()
            elif "netmask" in line and not is_windows:
                parts = line.split()
                try:
                    netmask_index = parts.index('netmask')
                    local_netmask = parts[netmask_index + 1]
                except ValueError:
                    continue
            
            # 2. Capture Local IP Address
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

    # Returns public IP, and the relevant local netmask/subnet mask based on OS
    return public_ip, local_ip, subnet_mask if is_windows else local_netmask

