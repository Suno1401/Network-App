import time
from test_dns import test_dns
from test_ping import ping as ping_host
from test_speed import test_speed , network , mask_to_cidr

def main():
    print("\n\n##################")
    print("##   **SUNO** ##")
    print("##################\n")

    print("=== 🧰 NETWORK TEST ===\n")
    time.sleep(0.5)

    # Function calls
    dns_result = test_dns() 
    ping_ok = ping_host()
    ping, down, up = test_speed()
    public_ip, local_ip, subnet_mask = network()

    subnet_mask = mask_to_cidr(subnet_mask)


    print("\n=== 📊 Summary ===")
    print(f"DNS OK : {'✅' if dns_result else '❌'}")
    print(f"Ping OK : {'✅' if ping_ok else '❌'}")
    print(f"Download Speed : {down:.2f} Mbps")
    print(f"Upload Speed : {up:.2f} Mbps")
    
    print("\n=== 📊 Info ===")
    print(f"🔹 Local Network : {local_ip} /{subnet_mask}")
    print(f"🔹 Public IP : {public_ip}")
    print(f"🔹 Resolved IP (DNS) : {dns_result['ip'] if dns_result and dns_result.get('ip') else '❌ DNS error'}")
    print(f"🔹 Ping : {ping:.2f} ms")

    if down < 10:
        print("⚠️ Low speed — check cabling or Internet box.")
    else:
        print("✅ Network functional.")

if __name__ == "__main__":
    main()