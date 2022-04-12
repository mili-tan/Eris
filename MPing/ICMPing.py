from scapy.layers.inet import *


def Ping(ip: object):
    ans, unans = sr(IP(dst=ip) / ICMP(), timeout=2)

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
                "msg": "Incorrect IP",
                "ip": str(rx.src)
            }
        else:
            return {
                "protocol": "ICMP",
                "state": True,
                "latency": int(delta * 1000),
                "msg": "OK",
                "ip": str(rx.src)
            }
    else:
        # print("timeout")
        return {
            "protocol": "ICMP",
            "state": True,
            "latency": 0,
            "msg": "Timeout",
            "ip": ip
        }
