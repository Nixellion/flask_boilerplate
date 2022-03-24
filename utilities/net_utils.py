from platform import system as system_name  # Returns the system/OS name
from os import system as system_call  # Execute a shell command
import time

from flask import Request

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
    """
    Tests internet connection by pinging a number of hosts. If none of the pings works then there's no internet.
    """
    for ip in test_ips:
        if ping(ip):
            return True
        else:
            print("Could not reach internet. Trying another IP...")
            time.sleep(try_delay)
    return False


def get_real_ip(request):
    try:
        if request.headers.getlist("X-Forwarded-For"):
            ip = request.headers.getlist("X-Forwarded-For")[0]
        elif request.headers.getlist("X-Real-Ip"):
            ip = request.headers.getlist("X-Real-Ip")[0]
        else:
            ip = request.remote_addr
        return ip
    except:
        return "0.0.0.0"


class ProxiedRequest(Request):
    def __init__(self, environ, populate_request=True, shallow=False):
        super(Request, self).__init__(environ, populate_request, shallow)
        # Support SSL termination. Mutate the host_url within Flask to use https://
        # if the SSL was terminated.
        x_forwarded_proto = self.headers.get('X-Forwarded-Proto')
        if x_forwarded_proto == 'https':
            self.url = self.url.replace('http://', 'https://')
            self.host_url = self.host_url.replace('http://', 'https://')
            self.base_url = self.base_url.replace('http://', 'https://')
            self.url_root = self.url_root.replace('http://', 'https://')