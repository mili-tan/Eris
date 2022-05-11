from scapy.layers.inet import *

from MNetwork import MHost


class Ping:
    def __init__(self, ip, *, port=80):
        self.ip = MHost.Host(str(ip)).GetHost()
        self.port = port

    def ICMP(self):
        ip = str(self.ip)

        print(ip)

        ans, unans = sr(IP(dst=ip) / ICMP(), timeout=2)

        print(ans)

        if len(ans) != 0:
            rx = ans[0][1]
            tx = ans[0][0]
            delta = rx.time - tx.sent_time
            # ans.summary(lambda s, r: r.sprintf("%IP.src% is alive:" + str(delta * 1000)))
            if rx.src != ip:
                return {
                    "protocol": "ICMP",
                    "state": False,
                    "latency": int(delta * 1000),
                    "msg": "Incorrect",
                    "ip": str(rx.src),
                    "ttl": int(rx.ttl)
                }
            else:
                return {
                    "protocol": "ICMP",
                    "state": True,
                    "latency": int(delta * 1000),
                    "msg": "OK",
                    "ip": str(rx.src),
                    "ttl": int(rx.ttl)
                }
        else:
            return {
                "protocol": "ICMP",
                "state": False,
                "latency": 0,
                "msg": "Timeout",
                "ip": ip,
                "ttl": 0
            }

    def TCP(self):
        ip = str(self.ip)
        port = int(self.port)

        ans, unans = sr(IP(dst=ip) / TCP(dport=port, flags="S"), timeout=2)

        if len(ans) != 0:
            rx = ans[0][1]
            tx = ans[0][0]
            delta = rx.time - tx.sent_time
            # ans.summary(lambda s, r: r.sprintf("%IP.src% is alive:" + str(int(delta * 1000))))
            if rx.src != ip:
                return {
                    "protocol": "TCP",
                    "state": False,
                    "latency": int(delta * 1000),
                    "msg": "Incorrect",
                    "ip": str(rx.src),
                    "ttl": int(rx.ttl)
                }
            else:
                return {
                    "protocol": "TCP",
                    "state": True,
                    "latency": int(delta * 1000),
                    "msg": "OK",
                    "ip": str(rx.src),
                    "ttl": int(rx.ttl)
                }
        else:
            return {
                "protocol": "TCP",
                "state": False,
                "latency": 0,
                "msg": "Timeout",
                "ip": ip,
                "ttl": 0
            }
