import os
import platform
import logging
from config import PING_HOSTS

'''Ping Google DNS to check connectivity.'''

def ping(hosts=None):
    if hosts is None:
        hosts = PING_HOSTS
    results = []
    for host in hosts:
        results.append(_ping_single_host(host))
    return results


def _ping_single_host(host="8.8.8.8"):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "4", host]
    response = os.system(" ".join(command))
    success = response == 0
    if success:
        print(f"✅ Ping successful to {host}")
        logging.info(f"PING SUCCESS - {host}")
    else:
        print(f"❌ Ping failed to {host}")
        logging.error(f"PING FAILED - {host}")
    return success