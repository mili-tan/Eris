from scapy.layers.inet import *


def Trace(ip: object):
    ans, unans = sr(IP(dst=ip, ttl=(1, 30)) / ICMP(), timeout=3)
    res = {}
    for i in ans[IP]:
        if i.answer.src != ip:
            # print(i)
            res[i.answer.src] = i.query.ttl

    # res = sorted(set(res), key=res.values)
    res = sorted(res.items(), key=lambda kv: (kv[1], kv[0]))
    res = [x[0] for x in res]

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
