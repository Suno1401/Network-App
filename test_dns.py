import socket
import time
import logging
from config import DNS_DOMAINS

""" Testing DNS resolution. """


def test_dns(domains=None):
    if domains is None:
        domains = DNS_DOMAINS
    results = []
    for domain in domains:
        results.append(_test_single_domain(domain))
    return results


def _test_single_domain(domain):
    print(f"🔹 Testing DNS resolution for {domain}...")

    try:
        start_time = time.time()
        ip = socket.gethostbyname(domain)
        response = time.time() - start_time

        print(f"✅ {domain} resolved to {ip} in {response*1000:.2f} ms")
        logging.info(f"DNS SUCCESS - {domain} → {ip} ({response*1000:.2f}ms)")
        return {
            "domain": domain,
            "ip": ip,
            "response_time_ms": response*1000,
            "success": True
        }
    except socket.timeout:
        print(f"❌ DNS timeout for {domain}")
        logging.error(f"DNS TIMEOUT - {domain}")
        return {
            "domain": domain,
            "ip": None,
            "response_time_ms": None,
            "success": False
        }
    except socket.gaierror:
        print(f"❌ DNS error for {domain}")
        logging.error(f"DNS ERROR - {domain}")
        return {
            "domain": domain,
            "ip": None,
            "response_time_ms": None,
            "success": False
        }
    except Exception as e:
        print(f"❌ Unexpected error for {domain}: {str(e)}")
        logging.error(f"DNS EXCEPTION - {domain}: {str(e)}")
        return {
            "domain": domain,
            "ip": None,
            "response_time_ms": None,
            "success": False
        }