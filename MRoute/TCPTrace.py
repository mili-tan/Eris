from scapy.layers.inet import *


def Trace(ip: object, port):
    ans, unans = traceroute(ip, port, maxttl=30, timeout=3)
    res = {}
    for i in ans.get_trace()[ip]:
        if ans.get_trace()[ip][i][0] != ip:
            # print(str(i) + ":" + ans.get_trace()[ip][i][0])
            res[ans.get_trace()[ip][i][0]] = i

    res = sorted(res.items(), key=lambda kv: (kv[1], kv[0]))
    res = [x[0] for x in res]

    if len(res) != 0:
        return {
            "protocol": "Trace-TCP",
            "state": True,
            "msg": "OK",
            "ip": res
        }
    else:
        return {
            "protocol": "Trace-TCP",
            "state": False,
            "msg": "Timeout",
            "ip": res
        }
