from scapy.layers.inet import *


def Trace(ip: object):
    ans, unans = sr(IP(dst=ip, ttl=(1, 30)) / ICMP(), timeout=3)
    res = []
    for i in ans[IP]:
        res.append(i.answer.src)

    res = sorted(set(res), key=res.index)
    res.remove(ip)

    if len(res) != 0:
        return {
            "protocol": "Trace-ICMP",
            "state": True,
            "msg": "OK",
            "ip": res
        }
    else:
        return {
            "protocol": "Trace-ICMP",
            "state": False,
            "msg": "Timeout",
            "ip": res
        }
