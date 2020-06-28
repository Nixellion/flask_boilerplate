from platform import system as system_name  # Returns the system/OS name
from os import system as system_call  # Execute a shell command
import time

test_ips = ['duckduckgo.com',
            'cloudflare.com',
            'google.com',
            'ya.ru']


try_delay = 0.5

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that some hosts may not respond to a ping request even if the host name is valid.
    """

    # Ping parameters as function of OS
    parameters = "-n 1 -w 1000" if system_name().lower().strip() == "windows" else "-c 1 -W 1000"

    # Pinging
    return system_call("ping " + parameters + " " + host) == 0


def wait_for_internet_connection():
    while True:
        for ip in test_ips:
            if ping(ip):
                return
            else:
                print("Could not reach internet. Trying again...")
                time.sleep(try_delay)


def test_intertnet_connection():
    for ip in test_ips:
        if ping(ip):
            return True
        else:
            print("Could not reach internet. Trying another IP...")
            time.sleep(try_delay)
    return False

