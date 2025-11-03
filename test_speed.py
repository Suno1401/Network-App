import speedtest
import subprocess
import socket
import platform

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
            if "Subnet Mask" in line and is_windows:
                subnet_mask = line.split(":")[-1].strip()
                break
            elif "netmask" in line and not is_windows:
                parts = line.split()
                try:
                    netmask_index = parts.index('netmask')
                    local_netmask = parts[netmask_index + 1]
                    break
                except ValueError:
                    continue
            
    except Exception as e:
        print(f"Error retrieving local network info: {e}")

    # Returns public IP, and the relevant local netmask/subnet mask based on OS
    return public_ip, subnet_mask if is_windows else local_netmask

