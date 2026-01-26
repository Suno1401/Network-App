import time
import logging
from config import LOGGING, SPEED_THRESHOLDS
from test_dns import test_dns
from test_ping import ping as ping_host
from test_speed import test_speed, network, get_mac_address

def main():
    #ConfigureLogging
    logging.basicConfig(
        filename=LOGGING["filename"],
        level=LOGGING["level"],
        format=LOGGING["format"],
        datefmt=LOGGING["date_format"]
    )
    
    print("\n\n##################")
    print("##   **SUNO** ##")
    print("##################\n")

    print("=== 🧰 NETWORK TEST ===\n")
    logging.info("=" * 50)
    logging.info("Network test started")
    time.sleep(0.5)

    #MYFunction
    dns_results = test_dns()
    ping_results = ping_host()
    ping, down, up = test_speed()
    public_ip, private_ip, local_subnet_mask, cidr = network()
    mac_address = get_mac_address()


    print("\n=== 📊 Summary ===")
    dns_ok = dns_results and any(result.get('success') for result in dns_results)
    ping_ok = ping_results and any(ping_results) if isinstance(ping_results, list) else ping_results
    print(f"DNS OK : {'✅' if dns_ok else '❌'}")
    print(f"Ping OK : {'✅' if ping_ok else '❌'}")
    print(f"Download Speed : {down:.2f} Mbps")
    print(f"Upload Speed : {up:.2f} Mbps")

    print("\n=== 📊 DNS Results ===")

    if dns_results:
        for result in dns_results:
            if result.get('success'):
                print(f"🔹 {result['domain']} → {result['ip']}")
    else:
        print(f"🔹 Resolved IP (DNS) : ❌ DNS error")
    
    print(f"🔹 Ping : {ping:.2f} ms")

    print("\n=== 📊 Info ===")
    print(f"🔹 Public IP : {public_ip}")
    print(f"🔹 Private IP : {private_ip}")
    print(f"🔹 Subnet Mask : {local_subnet_mask}   /{cidr}")
    print(f"🔹 MAC Address : {mac_address}")

    min_speed = SPEED_THRESHOLDS["min_download_mbps"]
    if down < min_speed:
        print(f"⚠️ Low speed — check cabling or Internet box.")
        logging.warning(f"LOW SPEED DETECTED - Download speed < {min_speed} Mbps")
    else:
        print("✅ Network functional.")
        logging.info("Network functional - All tests passed")
    
    logging.info("=" * 50)

if __name__ == "__main__":
    main()