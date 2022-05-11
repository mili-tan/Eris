import ipaddress
import socket


class Host:
    def __init__(self, host):
        self.host = host

    def GetHost(self):
        if Host.isIp(self):
            return self.host
        else:
            res = socket.getaddrinfo(self.host, None)
            print(res)
            return res[0][4][0]

    def isIp(self):
        try:
            ipaddress.ip_address(self.host.strip())
            return True
        except Exception as e:
            return False