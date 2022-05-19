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
                return __getJson__("ICMP", False, int(delta * 1000), "Incorrect", ip, 0)
            else:
                return __getJson__("TCP", True, int(delta * 1000), "OK", str(rx.src), int(rx.ttl))

        else:
            return __getJson__("ICMP", False, 0, "Timeout", ip, 0)

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
                return __getJson__("TCP", False, int(delta * 1000), "Incorrect", ip, 0)
            else:
                return __getJson__("TCP", True, int(delta * 1000), "OK", str(rx.src), int(rx.ttl))
        else:
            return __getJson__("TCP", False, 0, "Timeout", ip, 0)


def __getJson__(protocol, state, latency, msg, ip, ttl):
    return {
        "protocol": protocol,
        "state": state,
        "latency": latency,
        "msg": msg,
        "ip": ip,
        "ttl": ttl
    }
