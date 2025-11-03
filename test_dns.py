import socket
import time

""" Testing DNS resolution. """


def test_dns(domain= "www.google.com"):
    print(f"🔹 Testing DNS resolution for {domain}...")

    try:
        start_time = time.time()
        ip = socket.gethostbyname(domain)
        response = time.time() - start_time

        print(f"✅ {domain} resolved to {ip} in {response*1000:.2f} ms")
        return {
            "domain": domain,
            "ip": ip,
            "response_time_ms": response*1000,
            "success": True
        }
    except socket.timeout:
        print(f"❌ DNS timeout for {domain}")
    except socket.gaierror:
        print(f"❌ DNS error for {domain}")
    except Exception as e:
        print(f"❌ Unexpected error for {domain}: {str(e)}")