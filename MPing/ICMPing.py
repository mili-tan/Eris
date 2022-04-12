from scapy.layers.inet import *


def Ping(ip):
    ans, unans = sr(IP(dst=ip) / ICMP(), timeout=2)

    if len(ans) != 0:
        rx = ans[0][1]
        tx = ans[0][0]
        delta = rx.time - tx.sent_time
        # ans.summary(lambda s, r: r.sprintf("%IP.src% is alive:" + str(delta * 1000)))
        return {
            "protocol": "TCP",
            "state": True,
            "latency": int(delta * 1000),
            "msg": "OK"
        }
    else:
        # print("timeout")
        return {
            "protocol": "TCP",
            "state": True,
            "latency": 0,
            "msg": "timeout"
        }
