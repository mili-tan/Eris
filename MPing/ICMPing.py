from scapy.layers.inet import *


def Ping(ip):
    ans, unans = sr(IP(dst=ip) / ICMP(), timeout=5)

    if len(ans) != 0:
        rx = ans[0][1]
        tx = ans[0][0]
        delta = rx.time - tx.sent_time
        ans.summary(lambda s, r: r.sprintf("%IP.src% is alive:" + str(delta * 1000)))
    else:
        print("timeout")

