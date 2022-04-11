from scapy.layers.inet import *


def Ping(ip, port):
    ans, unans = sr(IP(dst=ip) / TCP(dport=port, flags="S"), timeout=5)
    rx = ans[0][1]
    tx = ans[0][0]
    delta = rx.time - tx.sent_time
    ans.summary(lambda s, r: r.sprintf("%IP.src% is alive:" + str(delta * 1000)))
