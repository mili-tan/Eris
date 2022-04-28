from scapy.layers.inet import *


def Ping(ip, port):
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
                "msg": "Incorrect IP",
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
        # print("timeout")
        return {
            "protocol": "TCP",
            "state": True,
            "latency": 0,
            "msg": "Timeout",
            "ip": ip,
            "ttl": 0
        }
