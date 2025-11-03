import os
import platform

'''Ping Google DNS to check connectivity.'''

def ping(host="8.8.8.8"):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "4", host]
    response = os.system(" ".join(command))
    return response == 0